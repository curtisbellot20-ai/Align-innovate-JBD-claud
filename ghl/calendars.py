from .client import GHLClient
from config import GHL_LOCATION_ID


class Calendars:
    def __init__(self, client: GHLClient):
        self.client = client
        self.location_id = GHL_LOCATION_ID

    # --- Calendars ---

    def list(self) -> dict:
        return self.client.get("/calendars/", params={"locationId": self.location_id})

    def get(self, calendar_id: str) -> dict:
        return self.client.get(f"/calendars/{calendar_id}")

    def create(self, data: dict) -> dict:
        data.setdefault("locationId", self.location_id)
        return self.client.post("/calendars/", data)

    def update(self, calendar_id: str, data: dict) -> dict:
        return self.client.put(f"/calendars/{calendar_id}", data)

    def delete(self, calendar_id: str) -> dict:
        return self.client.delete(f"/calendars/{calendar_id}")

    # --- Appointments ---

    def get_appointments(self, calendar_id: str = None, start_time: str = None, end_time: str = None, **kwargs) -> dict:
        params = {"locationId": self.location_id}
        if calendar_id:
            params["calendarId"] = calendar_id
        if start_time:
            params["startTime"] = start_time
        if end_time:
            params["endTime"] = end_time
        params.update(kwargs)
        return self.client.get("/calendars/events/appointments", params=params)

    def get_appointment(self, event_id: str) -> dict:
        return self.client.get(f"/calendars/events/appointments/{event_id}")

    def create_appointment(self, data: dict) -> dict:
        return self.client.post("/calendars/events/appointments", data)

    def update_appointment(self, event_id: str, data: dict) -> dict:
        return self.client.put(f"/calendars/events/appointments/{event_id}", data)

    def delete_appointment(self, event_id: str) -> dict:
        return self.client.delete(f"/calendars/events/appointments/{event_id}")

    # --- Free Slots ---

    def get_free_slots(self, calendar_id: str, start_date: str, end_date: str, timezone: str = None) -> dict:
        params = {"calendarId": calendar_id, "startDate": start_date, "endDate": end_date}
        if timezone:
            params["timezone"] = timezone
        return self.client.get(f"/calendars/{calendar_id}/free-slots", params=params)

    # --- Calendar Groups ---

    def list_groups(self) -> dict:
        return self.client.get("/calendars/groups", params={"locationId": self.location_id})

    def create_group(self, data: dict) -> dict:
        data.setdefault("locationId", self.location_id)
        return self.client.post("/calendars/groups", data)

    def delete_group(self, group_id: str) -> dict:
        return self.client.delete(f"/calendars/groups/{group_id}")
