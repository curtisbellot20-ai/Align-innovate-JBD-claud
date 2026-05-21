from .client import GHLClient
from config import GHL_LOCATION_ID


class Users:
    def __init__(self, client: GHLClient):
        self.client = client
        self.location_id = GHL_LOCATION_ID

    def get(self, user_id: str) -> dict:
        return self.client.get(f"/users/{user_id}")

    def search(self) -> dict:
        return self.client.get("/users/search", params={"locationId": self.location_id})

    def create(self, data: dict) -> dict:
        data.setdefault("locationId", self.location_id)
        return self.client.post("/users/", data)

    def update(self, user_id: str, data: dict) -> dict:
        return self.client.put(f"/users/{user_id}", data)

    def delete(self, user_id: str) -> dict:
        return self.client.delete(f"/users/{user_id}")
