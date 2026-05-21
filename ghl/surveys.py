from .client import GHLClient
from config import GHL_LOCATION_ID


class Surveys:
    def __init__(self, client: GHLClient):
        self.client = client
        self.location_id = GHL_LOCATION_ID

    def list(self, skip: int = 0, limit: int = 20) -> dict:
        return self.client.get("/surveys/", params={"locationId": self.location_id, "skip": skip, "limit": limit})

    def get_submissions(self, survey_id: str = None, contact_id: str = None, skip: int = 0, limit: int = 20) -> dict:
        params = {"locationId": self.location_id, "skip": skip, "limit": limit}
        if survey_id:
            params["surveyId"] = survey_id
        if contact_id:
            params["contactId"] = contact_id
        return self.client.get("/surveys/submissions", params=params)
