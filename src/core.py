from __future__ import annotations

import asyncio
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Iterable, List, Sequence

from telethon import TelegramClient, errors
from telethon.sessions.sqlite import SQLiteSession
from telethon.tl.types import InputPeerChannel

# ---------------------------------------------------------------------------#
# Data containers
# ---------------------------------------------------------------------------#


@dataclass(slots=True)
class ChatTarget:
    raw: str  # original user-supplied string
    entity: InputPeerChannel  # resolved Telethon entity

    def __str__(self):
        return self.raw


# ---------------------------------------------------------------------------#
# Entity-resolution helpers
# ---------------------------------------------------------------------------#

_auth_pair_re = re.compile(r"^-?(\d+):(\d+)$")  # id:access_hash  (id may be -100…)


def _normalize_numeric_id(raw: str) -> int | None:
    """
    Strip any leading '-' or '-100' and return int id, or None if not numeric.
    """
    s = raw.lstrip("-")
    if s.startswith("100"):
        s = s[3:]
    return int(s) if s.isdigit() else None


def _lookup_access_hash(session: SQLiteSession, channel_id: int) -> int | None:
    """
    Try to pull an access-hash for *channel_id* from whatever cache Telethon exposes.

    Telethon ≤1.28  →  session.entity_cache (dict)
    Telethon ≥1.29  →  session._entities     (dict, private)
    """
    # Newer Telethon
    cache = getattr(session, "_entities", None)
    if isinstance(cache, dict):
        for (cid, ah), _ in cache.items():
            if cid == channel_id:
                return ah

    # Older Telethon
    cache = getattr(session, "entity_cache", None)
    if isinstance(cache, dict):
        for (cid, ah), _ in cache.items():
            if cid == channel_id:
                return ah

    # Not cached
    return None


async def resolve_targets(client: TelegramClient, raw_chats: Sequence[str]) -> List[ChatTarget]:
    out: list[ChatTarget] = []

    for raw in raw_chats:
        raw = raw.strip()

        # 1) id:access_hash
        if m := _auth_pair_re.match(raw):
            cid, ah = map(int, m.groups())
            out.append(ChatTarget(raw, InputPeerChannel(abs(cid), ah)))
            continue

        # 2) Telethon tries with raw
        try:
            ent = await client.get_input_entity(raw)
            out.append(ChatTarget(raw, ent))
            continue
        except (ValueError, errors.UsernameInvalidError, errors.UsernameNotOccupiedError):
            pass  # we’ll try other strategies

        # 2b) If raw looks numeric, try again with int (works when you’re still a member)
        if (num := _normalize_numeric_id(raw)) is not None:
            try:
                ent = await client.get_input_entity(int(raw))  # int → triggers server query
                out.append(ChatTarget(raw, ent))
                continue
            except (ValueError, errors.RPCError):
                pass  # fall through to cache lookup

        # 3) Numeric id but not member → look for cached access-hash
        if num is not None:
            if isinstance(client.session, SQLiteSession):
                if ah := _lookup_access_hash(client.session, num):
                    out.append(ChatTarget(raw, InputPeerChannel(num, ah)))
                    continue
            print(
                f"⚠️  ID '{raw}' needs an access-hash. Re-join the chat "
                "or supply 'id:access_hash'."
            )
        else:
            print(f"⚠️  Could not resolve '{raw}'. Skipping.")

    return out


# ---------------------------------------------------------------------------#
# Deletion loop
# ---------------------------------------------------------------------------#


async def delete_own_messages(
    client: TelegramClient,
    targets: Iterable[ChatTarget],
    mps: float,
    max_scan: int,
    dry_run: bool,
) -> None:
    delay = 0 if mps <= 0 else 1 / mps
    local_tz = datetime.now().astimezone().tzinfo or timezone.utc

    for tgt in targets:
        print(f"\n>>> Cleaning chat {tgt.raw} (limit {max_scan}) …")
        try:
            async for msg in client.iter_messages(tgt.entity, from_user="me", limit=max_scan):
                # Flags
                flags = []
                if msg.voice:
                    flags.append("[Voice]")
                elif msg.media:
                    flags.append("[M]")
                if msg.reply_to_msg_id:
                    flags.append("[R]")

                ts = msg.date.astimezone(local_tz).strftime("%Y-%m-%d %H:%M:%S")
                preview = (msg.text or "").replace("\n", " ")[:80]
                print(f"{ts} | {preview} {' '.join(flags)}")

                if not dry_run:
                    try:
                        await client.delete_messages(tgt.entity, msg.id)
                    except errors.FloodWaitError as e:
                        print(f"⏳ Flood-wait {e.seconds}s – sleeping …")
                        await asyncio.sleep(e.seconds)

                await asyncio.sleep(delay)
        except (ValueError, errors.RPCError) as e:
            print(f"⚠️  Failed on chat '{tgt.raw}': {e}")
