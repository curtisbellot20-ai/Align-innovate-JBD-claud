from .client import GHLClient
from config import GHL_LOCATION_ID


class CustomFields:
    def __init__(self, client: GHLClient):
        self.client = client
        self.location_id = GHL_LOCATION_ID

    def list(self, model: str = "contact") -> dict:
        return self.client.get(
            f"/locations/{self.location_id}/customFields",
            params={"model": model}
        )

    def get(self, field_id: str) -> dict:
        return self.client.get(f"/locations/{self.location_id}/customFields/{field_id}")

    def create(self, data: dict) -> dict:
        return self.client.post(f"/locations/{self.location_id}/customFields", data)

    def update(self, field_id: str, data: dict) -> dict:
        return self.client.put(f"/locations/{self.location_id}/customFields/{field_id}", data)

    def delete(self, field_id: str) -> dict:
        return self.client.delete(f"/locations/{self.location_id}/customFields/{field_id}")
