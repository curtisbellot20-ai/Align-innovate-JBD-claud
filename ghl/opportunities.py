from .client import GHLClient
from config import GHL_LOCATION_ID


class Opportunities:
    def __init__(self, client: GHLClient):
        self.client = client
        self.location_id = GHL_LOCATION_ID

    def search(self, pipeline_id: str = None, status: str = None, limit: int = 20, skip: int = 0, **kwargs) -> dict:
        params = {"location_id": self.location_id, "limit": limit, "skip": skip}
        if pipeline_id:
            params["pipeline_id"] = pipeline_id
        if status:
            params["status"] = status
        params.update(kwargs)
        return self.client.get("/opportunities/search", params=params)

    def get(self, opportunity_id: str) -> dict:
        return self.client.get(f"/opportunities/{opportunity_id}")

    def create(self, data: dict) -> dict:
        data.setdefault("locationId", self.location_id)
        return self.client.post("/opportunities/", data)

    def update(self, opportunity_id: str, data: dict) -> dict:
        return self.client.put(f"/opportunities/{opportunity_id}", data)

    def update_status(self, opportunity_id: str, status: str) -> dict:
        return self.client.patch(f"/opportunities/{opportunity_id}/status", {"status": status})

    def delete(self, opportunity_id: str) -> dict:
        return self.client.delete(f"/opportunities/{opportunity_id}")

    def get_pipelines(self) -> dict:
        return self.client.get("/opportunities/pipelines", params={"locationId": self.location_id})
