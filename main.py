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


def verify_connection():
    ghl = AlignInnovateGHL()
    print("Verifying GoHighLevel connection...")
    location = ghl.locations.get()
    print(f"Connected to location: {location.get('location', {}).get('name', 'Unknown')}")
    print(f"Location ID: {GHL_LOCATION_ID}")
    print("Connection verified.")
    return ghl


if __name__ == "__main__":
    verify_connection()
