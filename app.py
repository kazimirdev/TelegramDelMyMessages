#!/usr/bin/env python3
from __future__ import annotations

import asyncio
import sys

from telethon import TelegramClient

from src.cli import build_parser
from src.config import APIError, load_credentials
from src.core import delete_own_messages, resolve_targets


async def _async_main() -> None:
    args = build_parser().parse_args()

    try:
        api_id, api_hash = load_credentials()
    except APIError as e:
        print(e)
        sys.exit(1)

    session = "auto_delete_session"

    async with TelegramClient(session, api_id, api_hash) as client:
        # First-run login
        if not await client.is_user_authorized():
            print("⚠️  First run: follow the login prompts …")
            await client.send_code_request(phone=input("Phone number (+countrycode): "))
            await client.sign_in(code=input("Code from Telegram: "))

        targets = await resolve_targets(client, args.chat)
        if not targets:
            print("No valid chats resolved. Exiting.")
            return

        await delete_own_messages(client, targets, args.speed, args.limit, args.dry_run)


def main() -> None:  # small wrapper for sync entry point
    try:
        asyncio.run(_async_main())
    except KeyboardInterrupt:
        print("Interrupted by user ☠️")


if __name__ == "__main__":
    main()
