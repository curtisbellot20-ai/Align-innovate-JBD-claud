import logging
import time
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from config import GHL_API_KEY, GHL_BASE_URL, GHL_API_VERSION
from security import scrub_dict

logger = logging.getLogger(__name__)

_RETRY_STRATEGY = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
)


class GHLClient:
    def __init__(self):
        self.base_url = GHL_BASE_URL
        self.session = requests.Session()
        adapter = HTTPAdapter(max_retries=_RETRY_STRATEGY)
        self.session.mount("https://", adapter)
        self.session.headers.update({
            "Authorization": f"Bearer {GHL_API_KEY}",
            "Version": GHL_API_VERSION,
            "Content-Type": "application/json",
            "Accept": "application/json",
        })

    def _request(self, method: str, endpoint: str, **kwargs) -> dict:
        url = f"{self.base_url}{endpoint}"
        response = self.session.request(method, url, timeout=30, **kwargs)
        if response.status_code == 429:
            retry_after = int(response.headers.get("Retry-After", 5))
            logger.warning("Rate limited by GHL — waiting %ds", retry_after)
            time.sleep(retry_after)
            response = self.session.request(method, url, timeout=30, **kwargs)
        response.raise_for_status()
        return response.json()

    def get(self, endpoint: str, params: dict = None) -> dict:
        return self._request("GET", endpoint, params=params)

    def post(self, endpoint: str, data: dict = None) -> dict:
        return self._request("POST", endpoint, json=data)

    def put(self, endpoint: str, data: dict = None) -> dict:
        return self._request("PUT", endpoint, json=data)

    def patch(self, endpoint: str, data: dict = None) -> dict:
        return self._request("PATCH", endpoint, json=data)

    def delete(self, endpoint: str) -> dict:
        return self._request("DELETE", endpoint)
