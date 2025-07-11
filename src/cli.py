import argparse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Delete your sent messages from selected Telegram chats."
    )
    parser.add_argument(
        "--chat",
        "-c",
        type=int,
        action="append",
        required=True,
        help="Chat ID (repeatable)."
    )
    parser.add_argument(
        "--speed",
        "-s",
        type=float,
        default=1.0,
        help="Messages per second (default 1). Use >1 for faster, <1 for slower."
    )
    parser.add_argument(
        "--limit",
        "-l",
        type=int,
        default=1000,
        help="Messages to scan per chat (default 1000)."
    )
    return parser