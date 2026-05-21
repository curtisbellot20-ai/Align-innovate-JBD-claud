import re
import hmac
import hashlib
import logging
from typing import Any

logger = logging.getLogger(__name__)

_TOKEN_RE = re.compile(r"(pit-|Bearer\s+)[A-Za-z0-9\-]{8,}", re.IGNORECASE)
_LOCATION_RE = re.compile(r"[A-Za-z0-9]{15,}")


def mask(value: str, visible: int = 4) -> str:
    """Return a safely masked version of a secret for logging."""
    if not value or len(value) <= visible:
        return "***"
    return value[:visible] + "*" * (len(value) - visible)


def scrub_dict(data: dict) -> dict:
    """Return a copy of data with secret-looking values masked."""
    sensitive = {"api_key", "apikey", "token", "secret", "password", "authorization"}
    result = {}
    for k, v in data.items():
        if any(s in k.lower() for s in sensitive):
            result[k] = mask(str(v))
        elif isinstance(v, dict):
            result[k] = scrub_dict(v)
        else:
            result[k] = v
    return result


def scrub_log_record(record: logging.LogRecord) -> logging.LogRecord:
    """Strip raw tokens from log messages."""
    record.msg = _TOKEN_RE.sub(lambda m: m.group(1) + "***", str(record.msg))
    return record


class ScrubFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        scrub_log_record(record)
        return True


def configure_logging(level: int = logging.INFO) -> None:
    handler = logging.StreamHandler()
    handler.addFilter(ScrubFilter())
    logging.basicConfig(level=level, handlers=[handler])


def verify_webhook_signature(payload: bytes, header_signature: str, secret: str) -> bool:
    if not secret:
        return True
    expected = hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, header_signature or "")


def validate_credentials(api_key: str, location_id: str) -> None:
    """Raise on startup if credentials look wrong — without logging their values."""
    if not api_key:
        raise EnvironmentError("GHL_API_KEY is missing. Set it in your .env file.")
    if not api_key.startswith("pit-"):
        raise EnvironmentError("GHL_API_KEY does not look like a valid Private Integration Token (expected 'pit-' prefix).")
    if not location_id:
        raise EnvironmentError("GHL_LOCATION_ID is missing. Set it in your .env file.")
    if len(location_id) < 10:
        raise EnvironmentError("GHL_LOCATION_ID appears too short to be valid.")


def sanitize_string(value: Any, max_length: int = 1000) -> str:
    """Strip control characters and enforce length limits on user-supplied strings."""
    if not isinstance(value, str):
        value = str(value)
    value = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", value)
    return value[:max_length]


def sanitize_dict(data: dict, max_depth: int = 5) -> dict:
    """Recursively sanitize string values in a dict."""
    if max_depth <= 0:
        return {}
    result = {}
    for k, v in data.items():
        safe_key = sanitize_string(str(k), 100)
        if isinstance(v, dict):
            result[safe_key] = sanitize_dict(v, max_depth - 1)
        elif isinstance(v, list):
            result[safe_key] = [sanitize_string(i) if isinstance(i, str) else i for i in v[:50]]
        elif isinstance(v, str):
            result[safe_key] = sanitize_string(v)
        else:
            result[safe_key] = v
    return result
