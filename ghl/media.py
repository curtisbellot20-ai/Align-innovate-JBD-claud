from .client import GHLClient
from config import GHL_LOCATION_ID


class Media:
    def __init__(self, client: GHLClient):
        self.client = client
        self.location_id = GHL_LOCATION_ID

    def list(self, sort_by: str = None, sort_order: str = None, skip: int = 0, limit: int = 20) -> dict:
        params = {"locationId": self.location_id, "skip": skip, "limit": limit}
        if sort_by:
            params["sortBy"] = sort_by
        if sort_order:
            params["sortOrder"] = sort_order
        return self.client.get("/medias/", params=params)

    def delete(self, media_id: str) -> dict:
        return self.client.delete(f"/medias/{media_id}")
