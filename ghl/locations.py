from .client import GHLClient
from config import GHL_LOCATION_ID


class Locations:
    def __init__(self, client: GHLClient):
        self.client = client
        self.location_id = GHL_LOCATION_ID

    def get(self) -> dict:
        return self.client.get(f"/locations/{self.location_id}")

    def update(self, data: dict) -> dict:
        return self.client.put(f"/locations/{self.location_id}", data)

    # --- Tags ---

    def get_tags(self) -> dict:
        return self.client.get(f"/locations/{self.location_id}/tags")

    def create_tag(self, name: str) -> dict:
        return self.client.post(f"/locations/{self.location_id}/tags", {"name": name})

    def update_tag(self, tag_id: str, name: str) -> dict:
        return self.client.put(f"/locations/{self.location_id}/tags/{tag_id}", {"name": name})

    def delete_tag(self, tag_id: str) -> dict:
        return self.client.delete(f"/locations/{self.location_id}/tags/{tag_id}")

    # --- Custom Values ---

    def get_custom_values(self) -> dict:
        return self.client.get(f"/locations/{self.location_id}/customValues")

    def create_custom_value(self, name: str, value: str) -> dict:
        return self.client.post(f"/locations/{self.location_id}/customValues", {"name": name, "value": value})

    def update_custom_value(self, custom_value_id: str, name: str, value: str) -> dict:
        return self.client.put(
            f"/locations/{self.location_id}/customValues/{custom_value_id}",
            {"name": name, "value": value}
        )

    def delete_custom_value(self, custom_value_id: str) -> dict:
        return self.client.delete(f"/locations/{self.location_id}/customValues/{custom_value_id}")

    # --- Templates ---

    def get_templates(self, template_type: str = None) -> dict:
        params = {}
        if template_type:
            params["type"] = template_type
        return self.client.get(f"/locations/{self.location_id}/templates", params=params)
