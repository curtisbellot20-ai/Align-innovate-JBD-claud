import hashlib
import hmac
from fastapi import FastAPI, Request, HTTPException, Header
from fastapi.responses import JSONResponse
from config import WEBHOOK_SECRET, PORT
import uvicorn
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="GHL Webhook Server")


def verify_signature(payload: bytes, signature: str, secret: str) -> bool:
    if not secret:
        return True
    expected = hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)


@app.post("/webhook")
async def handle_webhook(request: Request, x_ghl_signature: str = Header(None)):
    payload = await request.body()
    if WEBHOOK_SECRET and not verify_signature(payload, x_ghl_signature or "", WEBHOOK_SECRET):
        raise HTTPException(status_code=401, detail="Invalid signature")

    event = await request.json()
    event_type = event.get("type", "unknown")
    logger.info(f"Received GHL event: {event_type}")

    handlers = {
        "ContactCreate": on_contact_create,
        "ContactUpdate": on_contact_update,
        "ContactDelete": on_contact_delete,
        "OpportunityCreate": on_opportunity_create,
        "OpportunityUpdate": on_opportunity_update,
        "OpportunityDelete": on_opportunity_delete,
        "OpportunityStageUpdate": on_opportunity_stage_update,
        "OpportunityStatusUpdate": on_opportunity_status_update,
        "AppointmentCreate": on_appointment_create,
        "AppointmentUpdate": on_appointment_update,
        "AppointmentDelete": on_appointment_delete,
        "FormSubmission": on_form_submission,
        "SurveySubmission": on_survey_submission,
        "InboundMessage": on_inbound_message,
        "OutboundMessage": on_outbound_message,
        "NoteCreate": on_note_create,
        "TaskCreate": on_task_create,
        "TaskComplete": on_task_complete,
    }

    handler = handlers.get(event_type)
    if handler:
        await handler(event)
    else:
        logger.warning(f"Unhandled event type: {event_type}")

    return JSONResponse({"status": "ok"})


# --- Event handlers — add your business logic here ---

async def on_contact_create(event: dict):
    logger.info(f"Contact created: {event.get('id')}")

async def on_contact_update(event: dict):
    logger.info(f"Contact updated: {event.get('id')}")

async def on_contact_delete(event: dict):
    logger.info(f"Contact deleted: {event.get('id')}")

async def on_opportunity_create(event: dict):
    logger.info(f"Opportunity created: {event.get('id')}")

async def on_opportunity_update(event: dict):
    logger.info(f"Opportunity updated: {event.get('id')}")

async def on_opportunity_delete(event: dict):
    logger.info(f"Opportunity deleted: {event.get('id')}")

async def on_opportunity_stage_update(event: dict):
    logger.info(f"Opportunity stage updated: {event.get('id')} -> {event.get('stage')}")

async def on_opportunity_status_update(event: dict):
    logger.info(f"Opportunity status updated: {event.get('id')} -> {event.get('status')}")

async def on_appointment_create(event: dict):
    logger.info(f"Appointment created: {event.get('id')}")

async def on_appointment_update(event: dict):
    logger.info(f"Appointment updated: {event.get('id')}")

async def on_appointment_delete(event: dict):
    logger.info(f"Appointment deleted: {event.get('id')}")

async def on_form_submission(event: dict):
    logger.info(f"Form submitted: {event.get('formId')}")

async def on_survey_submission(event: dict):
    logger.info(f"Survey submitted: {event.get('surveyId')}")

async def on_inbound_message(event: dict):
    logger.info(f"Inbound message from: {event.get('contactId')}")

async def on_outbound_message(event: dict):
    logger.info(f"Outbound message to: {event.get('contactId')}")

async def on_note_create(event: dict):
    logger.info(f"Note created on contact: {event.get('contactId')}")

async def on_task_create(event: dict):
    logger.info(f"Task created on contact: {event.get('contactId')}")

async def on_task_complete(event: dict):
    logger.info(f"Task completed on contact: {event.get('contactId')}")


if __name__ == "__main__":
    uvicorn.run("webhook_server:app", host="0.0.0.0", port=PORT, reload=True)
