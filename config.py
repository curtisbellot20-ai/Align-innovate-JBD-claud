import os
from dotenv import load_dotenv
from security import validate_credentials, mask

load_dotenv()

GHL_API_KEY: str = os.getenv("GHL_API_KEY", "")
GHL_LOCATION_ID: str = os.getenv("GHL_LOCATION_ID", "")
WEBHOOK_SECRET: str = os.getenv("WEBHOOK_SECRET", "")
PORT: int = int(os.getenv("PORT", 8000))

GHL_BASE_URL = "https://services.leadconnectorhq.com"
GHL_API_VERSION = "2021-07-28"

# Fail fast on startup — log masked values only
validate_credentials(GHL_API_KEY, GHL_LOCATION_ID)

if __name__ != "__main__":
    import logging
    logging.getLogger(__name__).info(
        "GHL config loaded | key=%s | location=%s",
        mask(GHL_API_KEY),
        mask(GHL_LOCATION_ID),
    )
