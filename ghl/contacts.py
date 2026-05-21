from .client import GHLClient
from config import GHL_LOCATION_ID


class Contacts:
    def __init__(self, client: GHLClient):
        self.client = client
        self.location_id = GHL_LOCATION_ID

    # --- Core CRUD ---

    def get(self, contact_id: str) -> dict:
        return self.client.get(f"/contacts/{contact_id}")

    def create(self, data: dict) -> dict:
        data.setdefault("locationId", self.location_id)
        return self.client.post("/contacts/", data)

    def update(self, contact_id: str, data: dict) -> dict:
        return self.client.put(f"/contacts/{contact_id}", data)

    def delete(self, contact_id: str) -> dict:
        return self.client.delete(f"/contacts/{contact_id}")

    def upsert(self, data: dict) -> dict:
        data.setdefault("locationId", self.location_id)
        return self.client.post("/contacts/upsert", data)

    def search(self, query: str = None, limit: int = 20, skip: int = 0, **kwargs) -> dict:
        params = {"locationId": self.location_id, "limit": limit, "skip": skip}
        if query:
            params["query"] = query
        params.update(kwargs)
        return self.client.get("/contacts/", params=params)

    # --- Tags ---

    def add_tags(self, contact_id: str, tags: list) -> dict:
        return self.client.post(f"/contacts/{contact_id}/tags", {"tags": tags})

    def remove_tags(self, contact_id: str, tags: list) -> dict:
        return self.client.delete(f"/contacts/{contact_id}/tags")  # body via session if needed

    # --- Tasks ---

    def get_tasks(self, contact_id: str) -> dict:
        return self.client.get(f"/contacts/{contact_id}/tasks")

    def add_task(self, contact_id: str, data: dict) -> dict:
        return self.client.post(f"/contacts/{contact_id}/tasks", data)

    def update_task(self, contact_id: str, task_id: str, data: dict) -> dict:
        return self.client.put(f"/contacts/{contact_id}/tasks/{task_id}", data)

    def delete_task(self, contact_id: str, task_id: str) -> dict:
        return self.client.delete(f"/contacts/{contact_id}/tasks/{task_id}")

    # --- Notes ---

    def get_notes(self, contact_id: str) -> dict:
        return self.client.get(f"/contacts/{contact_id}/notes")

    def add_note(self, contact_id: str, body: str, user_id: str = None) -> dict:
        data = {"body": body}
        if user_id:
            data["userId"] = user_id
        return self.client.post(f"/contacts/{contact_id}/notes", data)

    def update_note(self, contact_id: str, note_id: str, body: str) -> dict:
        return self.client.put(f"/contacts/{contact_id}/notes/{note_id}", {"body": body})

    def delete_note(self, contact_id: str, note_id: str) -> dict:
        return self.client.delete(f"/contacts/{contact_id}/notes/{note_id}")

    # --- Appointments ---

    def get_appointments(self, contact_id: str) -> dict:
        return self.client.get(f"/contacts/{contact_id}/appointments")

    # --- Campaigns ---

    def add_to_campaign(self, contact_id: str, campaign_id: str) -> dict:
        return self.client.post(f"/contacts/{contact_id}/campaigns/{campaign_id}")

    def remove_from_campaign(self, contact_id: str, campaign_id: str) -> dict:
        return self.client.delete(f"/contacts/{contact_id}/campaigns/{campaign_id}")

    def remove_from_all_campaigns(self, contact_id: str) -> dict:
        return self.client.delete(f"/contacts/{contact_id}/campaigns/removeAll")

    # --- Workflows ---

    def add_to_workflow(self, contact_id: str, workflow_id: str) -> dict:
        return self.client.post(f"/contacts/{contact_id}/workflow/{workflow_id}")

    def remove_from_workflow(self, contact_id: str, workflow_id: str) -> dict:
        return self.client.delete(f"/contacts/{contact_id}/workflow/{workflow_id}")
