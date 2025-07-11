from __future__ import annotations

import os
from dotenv import load_dotenv


class APIError(RuntimeError):
    """Raised when required Telegram API credentials are missing."""


def load_credentials(dotenv_in_src: bool = True) -> tuple[int, str]:
    """
    Return (api_id, api_hash) from a .env file or environment variables.

    Priority:
    1. Environment variables already exported.
    2. `.env` in *src* package (your screenshot shows this).
    3. `.env` in project root.

    Raises
    ------
    APIError
        If either value is missing or invalid.
    """
    # 2️⃣ Explicitly look for .env inside src/ if requested
    if dotenv_in_src:
        load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"), override=False)
    # 3️⃣ Fallback to project root
    load_dotenv(override=False)

    api_id = os.getenv("API_ID")
    api_hash = os.getenv("API_HASH")

    if not api_id or not api_hash:
        raise APIError(
            "APIError: check .env file; should contain API_ID=<int> and API_HASH=<str>"
        )
    try:
        api_id = int(api_id)
    except ValueError as exc:
        raise APIError("API_ID must be an integer") from exc

    return api_id, api_hash
