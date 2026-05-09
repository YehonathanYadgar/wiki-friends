#!/usr/bin/env python3
"""Build a simple static HTML site from the Markdown wiki."""

from __future__ import annotations

import html
import json
import posixpath
import re
import shutil
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WIKI = ROOT / "wiki"
SITE = ROOT / "site"
ASSETS = SITE / "assets"
STATIC_ASSETS = ROOT / "site_static" / "assets"

SKIP_PARTS = {"inbox"}
SKIP_FILES = {WIKI / "log.md"}
SECTION_ORDER = ["people", "groups", "events", "topics", "places", "sources", "answers"]


@dataclass
class Page:
    src: Path
    rel: Path
    out: Path
    url: str
    title: str
    section: str
    summary: str
    body_html: str = ""


def slug_url(rel: Path) -> str:
    if rel == Path("overview.md"):
        return "index.html"
    if rel == Path("index.md"):
        return "wiki-index.html"
    if rel.name == "README.md":
        return f"{rel.parent.as_posix()}/index.html"
    return rel.with_suffix(".html").as_posix()


def should_include(path: Path) -> bool:
    rel = path.relative_to(WIKI)
    if any(part in SKIP_PARTS for part in rel.parts):
        return False
    if path in SKIP_FILES:
        return False
    return True


def strip_frontmatter(text: str) -> str:
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            return text[end + 5 :].lstrip()
    return text


def title_from_markdown(text: str, fallback: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fallback.replace("-", " ").replace("_", " ").title()


def summary_from_markdown(text: str) -> str:
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line.strip() == "> [!summary]":
            collected: list[str] = []
            for next_line in lines[i + 1 :]:
                if not next_line.startswith(">"):
                    break
                collected.append(next_line.lstrip("> ").strip())
            return " ".join(collected).strip()
    for line in lines:
        stripped = line.strip()
        if stripped and not stripped.startswith("#") and not stripped.startswith(">") and stripped != "---":
            return re.sub(r"[*_`]", "", stripped)
    return ""


def section_for(rel: Path) -> str:
    if len(rel.parts) > 1 and rel.parts[0] in SECTION_ORDER:
        return rel.parts[0]
    return "main"


def convert_inline(text: str, current_rel: Path, url_map: dict[Path, str]) -> str:
    code_tokens: list[str] = []
    link_tokens: list[str] = []

    def stash_code(match: re.Match[str]) -> str:
        code_tokens.append(f"<code>{html.escape(match.group(1))}</code>")
        return f"\x00CODE{len(code_tokens)-1}\x00"

    text = re.sub(r"`([^`]+)`", stash_code, text)

    def link_repl(match: re.Match[str]) -> str:
        label = convert_inline(match.group(1), current_rel, url_map)
        target = match.group(2)
        if target.startswith(("http://", "https://", "mailto:")):
            href = target
        else:
            clean_target = target.split("#", 1)[0]
            anchor = "#" + target.split("#", 1)[1] if "#" in target else ""
            resolved = posixpath.normpath((current_rel.parent / clean_target).as_posix())
            normalized = Path(resolved)
            href = url_map.get(normalized, target)
            if href != target:
                href = "/" + href + anchor
            elif clean_target.endswith(".md"):
                return f"<code>{html.escape(target)}</code>"
        link_tokens.append(f'<a href="{html.escape(href)}">{label}</a>')
        return f"\x00LINK{len(link_tokens)-1}\x00"

    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", link_repl, text)
    text = html.escape(text, quote=False)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", text)
    for i, token in enumerate(code_tokens):
        text = text.replace(html.escape(f"\x00CODE{i}\x00"), token)
    for i, token in enumerate(link_tokens):
        text = text.replace(html.escape(f"\x00LINK{i}\x00"), token)
    return text


def markdown_to_html(markdown: str, current_rel: Path, url_map: dict[Path, str]) -> str:
    lines = strip_frontmatter(markdown).splitlines()
    out: list[str] = []
    paragraph: list[str] = []
    list_stack = False
    in_code = False
    code_lines: list[str] = []
    in_callout = False
    callout_lines: list[str] = []

    def flush_paragraph() -> None:
        nonlocal paragraph
        if paragraph:
            text = " ".join(paragraph).strip()
            out.append(f"<p>{convert_inline(text, current_rel, url_map)}</p>")
            paragraph = []

    def flush_list() -> None:
        nonlocal list_stack
        if list_stack:
            out.append("</ul>")
            list_stack = False

    def flush_callout() -> None:
        nonlocal in_callout, callout_lines
        if in_callout:
            body = " ".join(callout_lines).strip()
            out.append(f'<aside class="callout">{convert_inline(body, current_rel, url_map)}</aside>')
            in_callout = False
            callout_lines = []

    for raw in lines:
        line = raw.rstrip()
        if line.startswith("```"):
            flush_paragraph()
            flush_list()
            flush_callout()
            if in_code:
                out.append(f"<pre><code>{html.escape(chr(10).join(code_lines))}</code></pre>")
                code_lines = []
                in_code = False
            else:
                in_code = True
            continue
        if in_code:
            code_lines.append(line)
            continue

        if line.strip() == "":
            flush_paragraph()
            flush_list()
            flush_callout()
            continue

        if line.strip() == "> [!summary]":
            flush_paragraph()
            flush_list()
            flush_callout()
            in_callout = True
            continue
        if in_callout and line.startswith(">"):
            callout_lines.append(line.lstrip("> ").strip())
            continue
        if in_callout:
            flush_callout()

        heading = re.match(r"^(#{1,6})\s+(.*)$", line)
        if heading:
            flush_paragraph()
            flush_list()
            level = len(heading.group(1))
            text = convert_inline(heading.group(2), current_rel, url_map)
            anchor = re.sub(r"[^a-z0-9]+", "-", heading.group(2).lower()).strip("-")
            out.append(f'<h{level} id="{anchor}">{text}</h{level}>')
            continue

        bullet = re.match(r"^[-*]\s+(.*)$", line)
        if bullet:
            flush_paragraph()
            if not list_stack:
                out.append("<ul>")
                list_stack = True
            out.append(f"<li>{convert_inline(bullet.group(1), current_rel, url_map)}</li>")
            continue

        paragraph.append(line)

    flush_paragraph()
    flush_list()
    flush_callout()
    return "\n".join(out)


def load_pages() -> list[Page]:
    pages: list[Page] = []
    for src in sorted(WIKI.rglob("*.md")):
        if not should_include(src):
            continue
        rel = src.relative_to(WIKI)
        text = strip_frontmatter(src.read_text(encoding="utf-8"))
        url = slug_url(rel)
        pages.append(
            Page(
                src=src,
                rel=rel,
                out=SITE / url,
                url=url,
                title=title_from_markdown(text, rel.stem),
                section=section_for(rel),
                summary=summary_from_markdown(text),
            )
        )
    return pages


def render_page(page: Page, pages: list[Page]) -> str:
    nav_items = "\n".join(
        f'<li><a href="/{html.escape(p.url)}">{html.escape(p.title)}</a></li>'
        for p in pages
        if p.section in {"main", "people", "groups", "events", "topics", "places"}
    )
    data = {
        "title": page.title,
        "section": page.section,
        "url": page.url,
    }
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(page.title)} - Friend Group Wiki</title>
  <link rel="stylesheet" href="/assets/style.css">
</head>
<body data-page='{html.escape(json.dumps(data))}'>
  <header class="topbar">
    <button class="menu-button" aria-label="Open navigation">☰</button>
    <a class="brand" href="/index.html">Friend Group Wiki</a>
    <input id="search" class="search" type="search" placeholder="Search the wiki">
  </header>
  <div class="layout">
    <aside class="sidebar">
      <div class="sidebar-title">Contents</div>
      <nav><ul>{nav_items}</ul></nav>
    </aside>
    <main class="article">
      <div class="crumb">{html.escape(page.section.title())}</div>
      {page.body_html}
    </main>
  </div>
  <div id="searchResults" class="search-results" hidden></div>
  <script src="/assets/search-index.js"></script>
  <script src="/assets/app.js"></script>
</body>
</html>
"""


def write_assets(pages: list[Page]) -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    for asset in STATIC_ASSETS.glob("*"):
        if asset.is_file():
            shutil.copy2(asset, ASSETS / asset.name)
    search_data = [
        {"title": p.title, "url": "/" + p.url, "section": p.section, "summary": p.summary}
        for p in pages
    ]
    (ASSETS / "search-index.js").write_text(
        "window.SEARCH_INDEX = " + json.dumps(search_data, ensure_ascii=False, indent=2) + ";\n",
        encoding="utf-8",
    )


def main() -> int:
    if SITE.exists():
        for item in SITE.iterdir():
            if item.name == "README.md":
                continue
            if item.is_dir():
                shutil.rmtree(item)
            else:
                item.unlink()
    SITE.mkdir(exist_ok=True)

    pages = load_pages()
    url_map = {page.rel: page.url for page in pages}
    for page in pages:
        markdown = page.src.read_text(encoding="utf-8")
        page.body_html = markdown_to_html(markdown, page.rel, url_map)

    for page in pages:
        page.out.parent.mkdir(parents=True, exist_ok=True)
        page.out.write_text(render_page(page, pages), encoding="utf-8")

    write_assets(pages)
    (SITE / "_redirects").write_text("/ /index.html 200\n", encoding="utf-8")
    print(f"Built {len(pages)} pages into {SITE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
