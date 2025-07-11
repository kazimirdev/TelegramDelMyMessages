import asyncio
from datetime import datetime, timezone

from telethon import TelegramClient, errors


async def delete_own_messages(client: TelegramClient,
                              chat_ids: list[int],
                              mps: float,
                              max_scan: int):
    """Iterate over user's own messages and delete at the desired speed."""
    delay = 1.0 / mps if mps > 0 else 0.0
    local_tz = datetime.now().astimezone().tzinfo or timezone.utc

    for chat_id in chat_ids:
        print(f"\n>>> Cleaning chat {chat_id} (limit {max_scan} messages) ...")
        async for msg in client.iter_messages(chat_id,
                                              from_user="me",
                                              limit=max_scan):
            # Compose flags
            flags: list[str] = []
            if msg.voice:
                flags.append("[Voice]")
            elif msg.media:
                flags.append("[M]")
            if msg.reply_to_msg_id:
                flags.append("[R]")

            # Timestamp in local tz
            ts = msg.date.astimezone(local_tz).strftime("%Y-%m-%d %H:%M:%S")
            # Safe preview
            text_preview = (msg.text or "").replace("\n", " ")[:80]
            log_line = f"{ts} | {text_preview} {' '.join(flags)}"
            print(log_line)

            # Delete and respect flood‑waits / speed limit
            try:
                await client.delete_messages(chat_id, msg.id)
            except errors.FloodWaitError as e:
                print(f"⚠️ Flood wait {e.seconds}s -> sleeping …")
                await asyncio.sleep(e.seconds)
            await asyncio.sleep(delay)