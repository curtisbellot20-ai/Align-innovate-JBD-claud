from security import configure_logging, mask
configure_logging()

import logging
from ghl.client import GHLClient
from ghl.contacts import Contacts
from ghl.opportunities import Opportunities
from ghl.conversations import Conversations
from ghl.calendars import Calendars
from ghl.campaigns import Campaigns
from ghl.forms import Forms
from ghl.users import Users
from ghl.locations import Locations
from ghl.custom_fields import CustomFields
from ghl.workflows import Workflows
from ghl.surveys import Surveys
from config import GHL_LOCATION_ID

logger = logging.getLogger(__name__)


class AlignInnovateGHL:
    """Central access point for all GoHighLevel API modules."""

    def __init__(self):
        client = GHLClient()
        self.contacts = Contacts(client)
        self.opportunities = Opportunities(client)
        self.conversations = Conversations(client)
        self.calendars = Calendars(client)
        self.campaigns = Campaigns(client)
        self.forms = Forms(client)
        self.users = Users(client)
        self.locations = Locations(client)
        self.custom_fields = CustomFields(client)
        self.workflows = Workflows(client)
        self.surveys = Surveys(client)


def verify_connection() -> "AlignInnovateGHL":
    ghl = AlignInnovateGHL()
    logger.info("Verifying GoHighLevel connection...")
    try:
        location = ghl.locations.get()
        name = location.get("location", {}).get("name", "Unknown")
        logger.info("Connected | location_name=%s | location_id=%s", name, mask(GHL_LOCATION_ID))
        print(f"Connected to GHL location: {name}")
    except Exception as exc:
        logger.error("GHL connection failed: %s", exc)
        raise
    return ghl


if __name__ == "__main__":
    verify_connection()
