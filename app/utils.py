import secrets
import string
from datetime import datetime, timezone

ALPHABET = string.ascii_letters + string.digits

def generate_code(length: int = 6) -> str:
    return "".join(secrets.choice(ALPHABET) for _ in range(length))

def utcnow() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)
