from .client import GHLClient
from config import GHL_LOCATION_ID


class Snapshots:
    def __init__(self, client: GHLClient):
        self.client = client
        self.location_id = GHL_LOCATION_ID

    def list(self) -> dict:
        return self.client.get("/snapshots/", params={"companyId": self.location_id})
