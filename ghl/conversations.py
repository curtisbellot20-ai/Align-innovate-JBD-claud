from .client import GHLClient
from config import GHL_LOCATION_ID


class Conversations:
    def __init__(self, client: GHLClient):
        self.client = client
        self.location_id = GHL_LOCATION_ID

    def get(self, conversation_id: str) -> dict:
        return self.client.get(f"/conversations/{conversation_id}")

    def create(self, contact_id: str, **kwargs) -> dict:
        data = {"locationId": self.location_id, "contactId": contact_id, **kwargs}
        return self.client.post("/conversations/", data)

    def update(self, conversation_id: str, data: dict) -> dict:
        return self.client.put(f"/conversations/{conversation_id}", data)

    def delete(self, conversation_id: str) -> dict:
        return self.client.delete(f"/conversations/{conversation_id}")

    def search(self, contact_id: str = None, limit: int = 20, **kwargs) -> dict:
        params = {"locationId": self.location_id, "limit": limit}
        if contact_id:
            params["contactId"] = contact_id
        params.update(kwargs)
        return self.client.get("/conversations/search", params=params)

    # --- Messages ---

    def get_messages(self, conversation_id: str, limit: int = 20) -> dict:
        return self.client.get(
            f"/conversations/{conversation_id}/messages",
            params={"limit": limit}
        )

    def send_message(self, conversation_id: str, msg_type: str, message: str, **kwargs) -> dict:
        """
        msg_type: SMS | Email | WhatsApp | GMB | IG | FB | Custom | Live_Chat
        """
        data = {"type": msg_type, "message": message, "conversationId": conversation_id, **kwargs}
        return self.client.post("/conversations/messages", data)

    def send_sms(self, conversation_id: str, message: str) -> dict:
        return self.send_message(conversation_id, "SMS", message)

    def send_email(self, conversation_id: str, subject: str, html: str, **kwargs) -> dict:
        return self.send_message(conversation_id, "Email", html, subject=subject, **kwargs)

    def add_inbound_message(self, data: dict) -> dict:
        return self.client.post("/conversations/messages/inbound", data)

    def upload_file_attachments(self, conversation_id: str, file_urls: list) -> dict:
        return self.client.post(
            f"/conversations/{conversation_id}/attachments",
            {"fileUrls": file_urls}
        )

    def update_message_status(self, message_id: str, status: str) -> dict:
        return self.client.put(f"/conversations/messages/{message_id}/status", {"status": status})
