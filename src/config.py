import os

from dotenv import load_dotenv


class APIError(RuntimeError):
    """Raised when required Telegram API credentials are missing."""


def load_credentials():
    """Load API_ID and API_HASH from .env and return them.

    Raises
    ------
    APIError
        If the .env file is missing or does not contain the keys.
    """
    load_dotenv()
    api_id = os.getenv("API_ID")
    api_hash = os.getenv("API_HASH")

    if not all((api_id, api_hash)) or len((api_id, api_hash)) != 2:
        raise APIError(
            "APIError: check .env file; should contain API_ID and API_HASH.\n"
            "Check README.md and https://my.telegram.org/apps for details."
        )

    try:
        api_id = int(api_id)
    except ValueError as exc:
        raise APIError("API_ID must be an integer") from exc

    return api_id, api_hash