# Log

Append one entry after every meaningful wiki operation. Keep entries chronological and never rewrite old entries except to fix typos.

Use this format:

```md
## [YYYY-MM-DD] ingest | Source title

- Raw source: `raw/...`
- Wiki pages changed: `wiki/...`, `wiki/...`
- Notes: short summary of what changed and what still needs review.
```

## [2026-05-09] setup | Personal wiki scaffold

- Raw source: none
- Wiki pages changed: `wiki/index.md`, `wiki/log.md`, `wiki/overview.md`, `wiki/synthesis.md`
- Notes: Created the initial raw/wiki structure for a personal friends-and-family wiki, including staging folders for WhatsApp imports.

## [2026-05-09] ingest | WhatsApp Chat 001

- Raw source: `raw/whatsapp/2026-05-09-chat-001/_chat.txt`
- Inbox transcript: `wiki/inbox/whatsapp/2026-05-09-chat-001.md`
- Wiki pages changed: `wiki/sources/2026-05-09-whatsapp-chat-001.md`, `wiki/groups/chat-001.md`, `wiki/index.md`, `wiki/overview.md`, `wiki/synthesis.md`, `wiki/log.md`
- Notes: Moved the root WhatsApp export into `raw/whatsapp/`, converted it to a Markdown inbox transcript, and created first-pass durable source and group summaries. Deeper person, event, topic, and media extraction remains pending.

## [2026-05-09] ingest | WhatsApp Chat 001 second pass

- Raw source: `raw/whatsapp/2026-05-09-chat-001/_chat.txt`
- Inbox transcript: `wiki/inbox/whatsapp/2026-05-09-chat-001.md`
- Wiki pages changed: `wiki/people/*`, `wiki/events/*`, `wiki/topics/*`, `wiki/places/*`, `wiki/groups/chat-001.md`, `wiki/sources/2026-05-09-whatsapp-chat-001.md`, `wiki/index.md`, `wiki/overview.md`, `wiki/synthesis.md`, `wiki/log.md`
- Notes: Filled the wiki from the chat with participant pages, major event pages, recurring topic pages, place pages, and cross-links. Updated project policy so raw exports and converted transcripts are kept as part of the private source trail rather than ignored.

## [2026-05-09] ingest | WhatsApp Chat 002 and style pass

- Raw source: `raw/whatsapp/2026-05-09-chat-002/_chat.txt`
- Inbox transcript: `wiki/inbox/whatsapp/2026-05-09-chat-002.md`
- Wiki pages changed: `wiki/sources/2026-05-09-whatsapp-chat-002.md`, `wiki/groups/agi-vegas.md`, `wiki/people/*`, `wiki/events/*`, `wiki/topics/*`, `wiki/index.md`, `wiki/overview.md`, `wiki/synthesis.md`, `wiki/log.md`
- Notes: Imported the older AGI/Vegas WhatsApp group, created source/group/event/topic pages, added Alon and Omri, and rewrote people pages into a more Obsidian-friendly profile style with vibes, speaking style, recurring bits, and questions.

## [2026-05-09] ingest | Etamar and Yoav direct chats

- Raw sources: `raw/whatsapp/2026-05-09-etamar-zukin/WhatsApp Chat - Etamar Zukin.zip`, `raw/whatsapp/2026-05-09-yoav-hashriri/WhatsApp Chat - יואב השרירי💪.zip`
- Inbox transcripts: `wiki/inbox/whatsapp/whatsapp-chat-etamar-zukin.md`, `wiki/inbox/whatsapp/whatsapp-chat-yoav-hashriri.md`
- Wiki pages changed: `wiki/sources/2026-05-09-direct-chat-etamar-zukin.md`, `wiki/sources/2026-05-09-direct-chat-yoav-hashriri.md`, `wiki/groups/direct-chats.md`, `wiki/topics/direct-message-dynamics.md`, `wiki/people/etamar-zukin.md`, `wiki/people/yoav-hashriri.md`, `wiki/people/itamarush.md`, `wiki/index.md`, `wiki/overview.md`, `wiki/synthesis.md`, `wiki/log.md`
- Notes: Imported direct-message exports for Etamar and Yoav, confirmed Etamar Zukin is not Itamarush, and enriched Etamar/Yoav pages with one-on-one friendship texture.

## [2026-05-09] canon | Friend group Q&A batch 001

- Raw source: user-provided Q&A in chat
- Wiki pages changed: `wiki/people/*`, `wiki/topics/tomer-the-sofa-carpet.md`, `wiki/topics/battle-of-shalev.md`, `wiki/topics/jony-the-mad-scientist.md`, `wiki/topics/alon-and-yoav-beef.md`, `wiki/groups/*`, `wiki/index.md`, `wiki/overview.md`, `wiki/synthesis.md`, `wiki/log.md`
- Notes: Added confirmed identity canon, main-character canon, group-name explanations, Shalev lore, Tomer furniture lore, Jony AGI/mad-scientist lore, Alon/Yoav beef, Age of Empires/Apex context, and preferred mixed-language/fun profile style.

## [2026-05-09] canon | 2023 Great Battle Of Shalev event

- Raw source: user clarification that the Great Battle with Shalev happened in 2023
- Wiki pages changed: `wiki/events/2023-great-battle-of-shalev.md`, `wiki/topics/battle-of-shalev.md`, `wiki/topics/shalev-mythology.md`, `wiki/people/shalev-carmal-f.md`, `wiki/people/jony-yadgar.md`, `wiki/groups/agi-vegas.md`, `wiki/index.md`, `wiki/overview.md`, `wiki/synthesis.md`, `wiki/log.md`
- Notes: Promoted the Battle of Shalev from general lore topic into a proper 2023 event page and linked it through the Shalev/Jony/AGI Vegas navigation.

## [2026-05-09] canon | Friend group Q&A batch 002

- Raw source: user-provided extended lore Q&A in chat
- Wiki pages changed: `wiki/events/2023-great-battle-of-shalev.md`, `wiki/places/rishon-lezion-dunes.md`, `wiki/topics/tomer-the-sofa-carpet.md`, `wiki/topics/jony-the-mad-scientist.md`, `wiki/topics/turkey-plastic-surgery-arc.md`, `wiki/topics/animal-based-raw-meat-philosophy.md`, `wiki/people/gdud-matkali.md`, `wiki/people/jony-yadgar.md`, `wiki/people/shalev-carmal-f.md`, `wiki/index.md`, `wiki/overview.md`, `wiki/synthesis.md`, `wiki/log.md`
- Notes: Expanded the Great Battle of Shalev with the dune-fight sequence and Mustafar roles, clarified Shalev's presumed-dead-but-redeemable status, expanded Sofa Tomer and `גדוד מטכלי` fake-elite logistics lore, and added Jony's Turkey surgery and animal-based/raw-meat mad-scientist arcs.

## [2026-05-09] canon | Jony public friend profile

- Raw source: user-provided `Jony Wiki - Public Friend Edition`
- Wiki pages changed: `wiki/people/jony-yadgar.md`, `wiki/topics/jony-emperor-arc.md`, `wiki/topics/agi-robot-future-doctrine.md`, `wiki/topics/emuna-ai-app-builder-arc.md`, `wiki/topics/figma-struggle-arc.md`, `wiki/topics/exact-button-instructions-doctrine.md`, `wiki/topics/army-hardware-setup-arc.md`, `wiki/topics/jony-the-mad-scientist.md`, `wiki/topics/animal-based-raw-meat-philosophy.md`, `wiki/index.md`, `wiki/overview.md`, `wiki/synthesis.md`, `wiki/log.md`
- Notes: Rebuilt Jony's page as a friend-safe profile and added dedicated pages for emperor lore, AGI/robot doctrine, Emuna AI, Figma/design struggles, exact instruction style, and army/hardware setup.
