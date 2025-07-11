import argparse


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="TelegramDelMyMessages",
        description="Delete *your own* Telegram messages from one or more chats.",
    )
    p.add_argument(
        "--chat",
        "-c",
        action="append",
        required=True,
        help=(
            "Chat identifier (repeatable). Accepts @username, t.me link, -100… or id, "
            "or 'id:access_hash' when you’ve left the chat."
        ),
    )
    p.add_argument("--speed", "-s", type=float, default=1.0, help="Msgs per second (default 1).")
    p.add_argument("--limit", "-l", type=int, default=1000, help="Max messages to scan.")
    p.add_argument("--dry-run", action="store_true", help="Preview deletions only.")
    return p
