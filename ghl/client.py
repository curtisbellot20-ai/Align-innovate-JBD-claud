import requests
from config import GHL_API_KEY, GHL_BASE_URL, GHL_API_VERSION


class GHLClient:
    def __init__(self):
        self.base_url = GHL_BASE_URL
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {GHL_API_KEY}",
            "Version": GHL_API_VERSION,
            "Content-Type": "application/json",
            "Accept": "application/json",
        })

    def get(self, endpoint: str, params: dict = None) -> dict:
        r = self.session.get(f"{self.base_url}{endpoint}", params=params)
        r.raise_for_status()
        return r.json()

    def post(self, endpoint: str, data: dict = None) -> dict:
        r = self.session.post(f"{self.base_url}{endpoint}", json=data)
        r.raise_for_status()
        return r.json()

    def put(self, endpoint: str, data: dict = None) -> dict:
        r = self.session.put(f"{self.base_url}{endpoint}", json=data)
        r.raise_for_status()
        return r.json()

    def patch(self, endpoint: str, data: dict = None) -> dict:
        r = self.session.patch(f"{self.base_url}{endpoint}", json=data)
        r.raise_for_status()
        return r.json()

    def delete(self, endpoint: str) -> dict:
        r = self.session.delete(f"{self.base_url}{endpoint}")
        r.raise_for_status()
        return r.json()
