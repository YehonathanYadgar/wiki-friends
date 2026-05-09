#!/usr/bin/env python3
"""Convert WhatsApp exported chats into Markdown inbox pages.

Use WhatsApp's built-in "Export chat" feature, then pass the exported .txt
file or .zip archive to this script. The output is a staging transcript for
review and later synthesis into durable wiki pages.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
import zipfile
from collections import Counter
from pathlib import Path


ANDROID_LINE = re.compile(
    r"^(?P<stamp>\d{1,4}[./-]\d{1,2}[./-]\d{1,4},?\s+"
    r"\d{1,2}:\d{2}(?::\d{2})?(?:\s?(?:AM|PM|am|pm))?)\s+-\s+"
    r"(?P<body>.*)$"
)
IOS_LINE = re.compile(r"^\[(?P<stamp>[^\]]+)\]\s+(?P<body>.*)$")
LEADING_MARKS = "\ufeff\u200e\u200f"


def read_export(path: Path) -> tuple[str, str]:
    if path.suffix.lower() == ".zip":
        with zipfile.ZipFile(path) as archive:
            names = [name for name in archive.namelist() if name.lower().endswith(".txt")]
            if not names:
                raise ValueError(f"No .txt chat file found in {path}")
            preferred = [name for name in names if Path(name).name.lower() in {"_chat.txt", "chat.txt"}]
            member = preferred[0] if preferred else names[0]
            data = archive.read(member).decode("utf-8-sig", errors="replace")
            return data, member

    return path.read_text(encoding="utf-8-sig", errors="replace"), path.name


def split_sender(body: str) -> tuple[str | None, str]:
    if ": " not in body:
        return None, body

    sender, text = body.split(": ", 1)
    if 0 < len(sender) <= 80 and "\n" not in sender:
        return sender, text
    return None, body


def parse_timestamp(raw: str, date_order: str) -> dt.datetime | None:
    cleaned = raw.replace("\u202f", " ").replace("\xa0", " ")
    cleaned = cleaned.replace(" at ", ", ")
    cleaned = re.sub(r"\s+", " ", cleaned.strip())
    cleaned = re.sub(
        r"\s*(am|pm)$",
        lambda match: " " + match.group(1).upper(),
        cleaned,
        flags=re.IGNORECASE,
    )

    orders = ["dmy", "mdy", "ymd"] if date_order == "auto" else [date_order]
    separators = [", ", " "]
    times = ["%H:%M:%S", "%H:%M", "%I:%M:%S %p", "%I:%M %p"]
    date_parts = {
        "dmy": ["%d/%m/%y", "%d/%m/%Y", "%d-%m-%y", "%d-%m-%Y", "%d.%m.%y", "%d.%m.%Y"],
        "mdy": ["%m/%d/%y", "%m/%d/%Y", "%m-%d-%y", "%m-%d-%Y", "%m.%d.%y", "%m.%d.%Y"],
        "ymd": ["%Y/%m/%d", "%y/%m/%d", "%Y-%m-%d", "%y-%m-%d", "%Y.%m.%d", "%y.%m.%d"],
    }

    for order in orders:
        for date_part in date_parts[order]:
            for separator in separators:
                for time_part in times:
                    try:
                        return dt.datetime.strptime(cleaned, f"{date_part}{separator}{time_part}")
                    except ValueError:
                        pass
    return None


def parse_messages(text: str, date_order: str) -> list[dict[str, object]]:
    messages: list[dict[str, object]] = []
    current: dict[str, object] | None = None

    for line in text.splitlines():
        normalized_line = line.lstrip(LEADING_MARKS)
        match = IOS_LINE.match(normalized_line) or ANDROID_LINE.match(normalized_line)
        if match:
            if current:
                messages.append(current)

            sender, body = split_sender(match.group("body"))
            stamp_raw = match.group("stamp").strip()
            stamp = parse_timestamp(stamp_raw, date_order)
            current = {
                "timestamp_raw": stamp_raw,
                "timestamp": stamp,
                "sender": sender,
                "text": body,
            }
            continue

        if current:
            current["text"] = str(current["text"]) + "\n" + line
        elif line.strip():
            messages.append(
                {
                    "timestamp_raw": "",
                    "timestamp": None,
                    "sender": None,
                    "text": line,
                }
            )

    if current:
        messages.append(current)

    return messages


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.lower()).strip("-")
    return slug or "whatsapp-chat"


def derive_chat_name(path: Path, archive_member: str, explicit_name: str | None) -> str:
    if explicit_name:
        return explicit_name
    if path.suffix.lower() == ".zip":
        return path.stem
    if path.name.lower() in {"_chat.txt", "chat.txt"} and path.parent.name:
        return path.parent.name
    return Path(archive_member).stem


def md_escape(value: object) -> str:
    text = str(value).strip()
    text = text.replace("\\", "\\\\")
    text = text.replace("*", "\\*").replace("_", "\\_")
    text = text.replace("`", "\\`")
    return text


def message_date(message: dict[str, object]) -> str:
    stamp = message["timestamp"]
    if isinstance(stamp, dt.datetime):
        return stamp.date().isoformat()
    raw = str(message["timestamp_raw"])
    return raw.split(",")[0] if raw else "undated"


def message_time(message: dict[str, object]) -> str:
    stamp = message["timestamp"]
    if isinstance(stamp, dt.datetime):
        return stamp.strftime("%H:%M")
    return str(message["timestamp_raw"]) or "unknown time"


def render_markdown(
    messages: list[dict[str, object]],
    chat_name: str,
    source_path: Path,
    archive_member: str,
) -> str:
    participants = Counter(
        str(message["sender"]) for message in messages if message.get("sender")
    )
    parsed_stamps = [
        message["timestamp"] for message in messages if isinstance(message["timestamp"], dt.datetime)
    ]
    imported_at = dt.datetime.now().astimezone().isoformat(timespec="seconds")

    lines = [
        "---",
        "source_type: whatsapp_export",
        f"chat_name: {json.dumps(chat_name, ensure_ascii=False)}",
        f"source_path: {json.dumps(str(source_path), ensure_ascii=False)}",
        f"archive_member: {json.dumps(archive_member, ensure_ascii=False)}",
        f"imported_at: {json.dumps(imported_at)}",
        f"message_count: {len(messages)}",
        f"participant_count: {len(participants)}",
    ]

    if parsed_stamps:
        lines.append(f"first_message_at: {json.dumps(min(parsed_stamps).isoformat(timespec='minutes'))}")
        lines.append(f"last_message_at: {json.dumps(max(parsed_stamps).isoformat(timespec='minutes'))}")

    lines.extend(
        [
            "---",
            "",
            f"# WhatsApp Import: {chat_name}",
            "",
            "> Staging transcript generated from a WhatsApp export. Review before using it to update durable wiki pages.",
            "",
            "## Participants",
            "",
        ]
    )

    if participants:
        for sender, count in participants.most_common():
            lines.append(f"- {md_escape(sender)} ({count})")
    else:
        lines.append("- No named participants detected.")

    lines.extend(["", "## Transcript", ""])
    current_date = None
    for message in messages:
        date_label = message_date(message)
        if date_label != current_date:
            current_date = date_label
            lines.extend(["", f"### {md_escape(date_label)}", ""])

        sender = md_escape(message["sender"] or "System")
        body = md_escape(message["text"]).replace("\n", "<br>")
        lines.append(f"- `{md_escape(message_time(message))}` **{sender}:** {body}")

    lines.append("")
    return "\n".join(lines)


def output_path_for(input_path: Path, out_dir: Path, chat_name: str) -> Path:
    suffix = slugify(chat_name)
    return out_dir / f"{suffix}.md"


def convert_one(
    input_path: Path,
    out_path: Path,
    chat_name: str | None,
    date_order: str,
    overwrite: bool,
) -> Path:
    text, archive_member = read_export(input_path)
    name = derive_chat_name(input_path, archive_member, chat_name)
    messages = parse_messages(text, date_order)
    rendered = render_markdown(messages, name, input_path, archive_member)

    if out_path.exists() and not overwrite:
        raise FileExistsError(f"{out_path} already exists; use --overwrite to replace it")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(rendered, encoding="utf-8")
    return out_path


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Convert WhatsApp exported .txt or .zip chats into Markdown inbox pages."
    )
    parser.add_argument("exports", nargs="+", type=Path, help="WhatsApp .txt or .zip export files")
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("wiki/inbox/whatsapp"),
        help="Output directory for generated Markdown files",
    )
    parser.add_argument("--out", type=Path, help="Output file; only valid with one export")
    parser.add_argument("--chat-name", help="Override detected chat name; only valid with one export")
    parser.add_argument(
        "--date-order",
        choices=["auto", "dmy", "mdy", "ymd"],
        default="auto",
        help="Date order used by the export; auto tries dmy, then mdy, then ymd",
    )
    parser.add_argument("--overwrite", action="store_true", help="Replace existing output files")
    args = parser.parse_args()

    if args.out and len(args.exports) != 1:
        parser.error("--out can only be used with one export")
    if args.chat_name and len(args.exports) != 1:
        parser.error("--chat-name can only be used with one export")

    try:
        written: list[Path] = []
        for export in args.exports:
            export = export.expanduser()
            if not export.exists():
                raise FileNotFoundError(export)

            if args.out:
                text, archive_member = read_export(export)
                name = derive_chat_name(export, archive_member, args.chat_name)
                messages = parse_messages(text, args.date_order)
                rendered = render_markdown(messages, name, export, archive_member)
                out_path = args.out
                if out_path.exists() and not args.overwrite:
                    raise FileExistsError(f"{out_path} already exists; use --overwrite to replace it")
                out_path.parent.mkdir(parents=True, exist_ok=True)
                out_path.write_text(rendered, encoding="utf-8")
                written.append(out_path)
                continue

            text, archive_member = read_export(export)
            name = derive_chat_name(export, archive_member, args.chat_name)
            out_path = output_path_for(export, args.out_dir, name)
            messages = parse_messages(text, args.date_order)
            rendered = render_markdown(messages, name, export, archive_member)
            if out_path.exists() and not args.overwrite:
                raise FileExistsError(f"{out_path} already exists; use --overwrite to replace it")
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(rendered, encoding="utf-8")
            written.append(out_path)

    except Exception as error:
        print(f"error: {error}", file=sys.stderr)
        return 1

    for path in written:
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
