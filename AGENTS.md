# Repository Guidelines

## Project Structure & Module Organization

This repository is a personal LLM-maintained wiki scaffold based on `llm-wiki.md`.

- `llm-wiki.md` explains the overall pattern and should remain the conceptual reference.
- `raw/` stores immutable source material, including WhatsApp exports, media, and family documents.
- `wiki/` stores the maintained knowledge base.
- `wiki/index.md` is the content map. Read it first and update it after every ingest or major query.
- `wiki/log.md` is the chronological activity record. Append to it after every meaningful operation.
- `wiki/overview.md` is the high-level map of the personal wiki.
- `wiki/synthesis.md` is the evolving cross-source interpretation.
- `wiki/inbox/` is staging for converted imports before synthesis.
- `docs/` contains human workflow notes.
- `tools/` contains local helper scripts.

The main wiki folders are `people/`, `groups/`, `events/`, `places/`, `topics/`, `sources/`, and `answers/`.

## Core Wiki Workflow

For every ingest:

1. Preserve the original source under `raw/`.
2. Convert or summarize into `wiki/inbox/` when needed.
3. Create a source summary in `wiki/sources/`.
4. Update affected people, groups, events, places, and topics.
5. Update `wiki/overview.md` or `wiki/synthesis.md` if the import changes the big picture.
6. Update `wiki/index.md`.
7. Append a dated entry to `wiki/log.md`.

For queries, read `wiki/index.md` and recent `wiki/log.md` entries first, then search relevant pages. If an answer creates durable knowledge, save it in `wiki/answers/` and update the index/log.

Periodically lint the wiki for contradictions, stale claims, orphan pages, missing links, and sensitive details that should be removed or softened.

## WhatsApp Ingest

Use WhatsApp's built-in export feature. Do not attempt to decrypt backups or scrape accounts.

Place exports in `raw/whatsapp/YYYY-MM-DD-chat-name/`, then convert text exports with:

```sh
python3 tools/whatsapp_export_to_markdown.py raw/whatsapp/2026-05-09-family-group/_chat.txt
```

See `docs/whatsapp-ingest.md` for phone export steps and privacy guidance.

## Source Handling

This is a private shared friends-and-family wiki. Keep raw exports, converted transcripts, and durable pages inside the repository so the group can inspect the source trail. Do not censor names or sender labels. Preserve uncertainty with wording like "appears to", "may have", or "needs confirmation" when the chat does not prove a claim.

## Style & Naming Conventions

Write Markdown in direct prose with clear headings, but keep this wiki fun to browse in Obsidian. People pages should include vibe, speaking style, recurring bits, links, and questions for the group. Light exaggeration is welcome when it matches the chat evidence.

Use lowercase hyphenated filenames, such as `family-trip-2024.md` or `friend-name.md`. Prefer wiki links or relative Markdown links when connecting pages.

Use dated event filenames when possible: `YYYY-MM-DD-short-title.md`.

## Local Commands

- `rg "term" wiki raw docs` searches the working material.
- `python3 tools/whatsapp_export_to_markdown.py --help` shows converter options.
- `python3 -m py_compile tools/whatsapp_export_to_markdown.py` checks the parser syntax.
- `git diff -- AGENTS.md docs tools wiki raw .gitignore` reviews repository changes.

No build step or automated test suite exists yet.

## Commit & Pull Request Guidelines

Use short, imperative commit messages, for example `Create personal wiki scaffold` or `Add WhatsApp ingest tool`.

Pull requests should summarize changed workflows, list added source types or tools, and call out major wiki-structure changes explicitly.
