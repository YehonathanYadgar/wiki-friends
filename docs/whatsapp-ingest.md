# WhatsApp Ingest Workflow

This workflow uses WhatsApp's built-in export feature as the source of truth. It does not decrypt phone backups or scrape WhatsApp Web.

Official references:

- WhatsApp Help Center: [How to export your chat history](https://faq.whatsapp.com/1180414079177245)
- WhatsApp Help Center: [How to transfer your chat history](https://faq.whatsapp.com/209942271778103)
- WhatsApp Help Center: [How to restore your chat history](https://faq.whatsapp.com/618575946635920)

## Project Boundary

WhatsApp exports can contain private messages, phone numbers, photos, documents, voice notes, and deleted-context conversations. This repository is intended as a private group project, so raw exports and converted transcripts are kept inside the project as source evidence.

## Export From WhatsApp

Export each important chat or group separately.

On iPhone:

1. Open WhatsApp.
2. Open the chat or group.
3. Tap the contact or group name.
4. Tap **Export Chat**.
5. Choose **Without Media** first for the most complete text export.
6. Save the `.zip` or `.txt` into `raw/whatsapp/YYYY-MM-DD-chat-name/`.

On Android:

1. Open WhatsApp.
2. Open the chat or group.
3. Tap the three-dot menu.
4. Tap **More**.
5. Tap **Export chat**.
6. Choose **Without media** first, then repeat with media only for chats where attachments matter.
7. Save the export into `raw/whatsapp/YYYY-MM-DD-chat-name/`.

## Why Text First

Text-only exports are easier to search, parse, and summarize. Media exports can hit share-size limits faster and may include fewer messages. For this wiki, start with text history, then add selected photos, videos, documents, or voice notes as separate raw assets when they are important.

## Convert To Wiki Inbox

From the repository root, run:

```sh
python3 tools/whatsapp_export_to_markdown.py raw/whatsapp/2026-05-09-family-group/_chat.txt
```

For month/day/year exports, use:

```sh
python3 tools/whatsapp_export_to_markdown.py raw/whatsapp/2026-05-09-family-group/_chat.txt --date-order mdy
```

The converter writes a normalized transcript to `wiki/inbox/whatsapp/`. This transcript is a staging file, not the final wiki.

## Ingest Into Durable Pages

After conversion:

1. Create or update a source summary in `wiki/sources/`.
2. Update relevant people pages in `wiki/people/`.
3. Update group pages in `wiki/groups/`.
4. Extract dated moments into `wiki/events/`.
5. Add recurring places and topics to `wiki/places/` and `wiki/topics/`.
6. Update `wiki/index.md`.
7. Append an entry to `wiki/log.md`.

Preserve uncertainty. If a message suggests but does not prove something, write "may have", "appears to", or add a note that it needs confirmation.
