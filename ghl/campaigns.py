from .client import GHLClient
from config import GHL_LOCATION_ID


class Campaigns:
    def __init__(self, client: GHLClient):
        self.client = client
        self.location_id = GHL_LOCATION_ID

    def list(self, status: str = None) -> dict:
        params = {"locationId": self.location_id}
        if status:
            params["status"] = status
        return self.client.get("/campaigns/", params=params)
