# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A private friend-group wiki maintained by an LLM. Raw WhatsApp exports and other sources live in `raw/`; the LLM writes and maintains all files under `wiki/`. The repo also includes a static-site builder (`tools/build_site.py`) that renders the wiki to `site/` for deployment on Netlify.

## Commands

```sh
# Convert a WhatsApp export to a wiki inbox transcript
python3 tools/whatsapp_export_to_markdown.py raw/whatsapp/YYYY-MM-DD-chat-name/_chat.txt

# Also accepts .zip archives directly
python3 tools/whatsapp_export_to_markdown.py raw/whatsapp/2026-05-09-chat-name/export.zip

# Override date order when export uses month/day/year
python3 tools/whatsapp_export_to_markdown.py ... --date-order mdy

# Build the static site into site/
python3 tools/build_site.py

# Preview the site locally
python3 -m http.server 8080 -d site

# Search working material
rg "term" wiki raw docs

# Syntax-check a tool
python3 -m py_compile tools/whatsapp_export_to_markdown.py

# Review all pending changes
git diff -- AGENTS.md docs tools wiki raw .gitignore
```

There is no automated test suite.

## Architecture

### Three layers

1. **`raw/`** — immutable source files (WhatsApp exports, media). Never modified by the LLM.
2. **`wiki/`** — all LLM-maintained Markdown. The LLM owns this layer entirely.
3. **`tools/`** — helper scripts the LLM can run to convert sources or build the site.

### Wiki structure

```
wiki/
  index.md        ← content map; read first, update after every ingest
  log.md          ← append-only chronological record of operations
  overview.md     ← high-level map of the wiki
  synthesis.md    ← evolving cross-source interpretation
  inbox/          ← staging area for converted imports (not published to site)
  people/
  groups/
  events/         ← filenames: YYYY-MM-DD-short-title.md
  topics/
  places/
  sources/
  answers/
```

`wiki/inbox/` is excluded from the site build. `wiki/log.md` is also excluded.

### Static site builder (`tools/build_site.py`)

Converts all eligible `wiki/*.md` files to HTML in `site/`. The builder:
- Maps `wiki/overview.md` → `site/index.html` and `wiki/index.md` → `site/wiki-index.html`
- Extracts page titles from the first `# Heading` and summaries from `> [!summary]` callout blocks
- Resolves wiki-style relative Markdown links to their HTML equivalents
- Writes a `site/assets/search-index.js` used by the client-side search (`site_static/assets/app.js`)
- Copies static assets from `site_static/assets/` into `site/assets/`

The `site/` directory is what Netlify deploys. No build command is needed in Netlify if the site has been pre-built and committed; see `netlify.toml` for the configured publish directory.

## Core ingest workflow

For every new source:

1. Place the raw file under `raw/` (immutable — never modify it).
2. Convert with the WhatsApp tool (if applicable) → `wiki/inbox/`.
3. Create a source summary in `wiki/sources/`.
4. Update affected pages in `people/`, `groups/`, `events/`, `places/`, `topics/`.
5. Update `wiki/overview.md` or `wiki/synthesis.md` if the big picture changes.
6. Update `wiki/index.md`.
7. Append a dated entry to `wiki/log.md`.

For queries: read `wiki/index.md` and recent `wiki/log.md` first. File useful answers in `wiki/answers/` and update the index/log.

## Style conventions

- Filenames: lowercase hyphenated (`friend-name.md`, `YYYY-MM-DD-short-title.md`).
- Prose: direct Markdown with clear headings. People pages include vibe, speaking style, recurring bits, and open questions. Light exaggeration is welcome when it matches chat evidence.
- Uncertainty: use "appears to", "may have", or "needs confirmation" when a claim isn't proven by the source.
- Links: prefer relative Markdown links or wiki-style links.
- Commit messages: short imperative (`Add WhatsApp ingest tool`, `Update Jony people page`).
