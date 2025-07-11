import asyncio
import sys

from telethon import TelegramClient

from src import (
    build_parser,
    delete_own_messages,
    load_credentials,
    APIError
)


async def main():
    parser = build_parser()
    args = parser.parse_args()

    try:
        api_id, api_hash = load_credentials()
    except APIError as e:
        print(e)
        sys.exit(1)

    session = "auto_delete_session"
    async with TelegramClient(session,
                              api_id,
                              api_hash) as client:
        # Login flow if first run
        if not await client.is_user_authorized():
            print("⚠️  First run: follow the login prompts …")
            await client.send_code_request(phone=input("Phone number (+countrycode): "))
            await client.sign_in(code=input("Code from Telegram: "))
        await delete_own_messages(client, args.chat, args.speed, args.limit)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Interrupted by user ☠️")
