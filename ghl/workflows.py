from .client import GHLClient
from config import GHL_LOCATION_ID


class Workflows:
    def __init__(self, client: GHLClient):
        self.client = client
        self.location_id = GHL_LOCATION_ID

    def list(self) -> dict:
        return self.client.get("/workflows/", params={"locationId": self.location_id})
