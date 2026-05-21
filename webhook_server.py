import logging
import time
from collections import defaultdict
from fastapi import FastAPI, Request, HTTPException, Header
from fastapi.responses import JSONResponse
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from config import WEBHOOK_SECRET, PORT
from security import verify_webhook_signature, sanitize_dict, configure_logging
import uvicorn

configure_logging()
logger = logging.getLogger(__name__)

app = FastAPI(title="GHL Webhook Server", docs_url=None, redoc_url=None, openapi_url=None)

# --- Simple in-memory rate limiter ---
_rate_store: dict = defaultdict(list)
_RATE_LIMIT = 60   # max requests
_RATE_WINDOW = 60  # per seconds


def _check_rate_limit(ip: str) -> bool:
    now = time.time()
    window = _rate_store[ip]
    _rate_store[ip] = [t for t in window if now - t < _RATE_WINDOW]
    if len(_rate_store[ip]) >= _RATE_LIMIT:
        return False
    _rate_store[ip].append(now)
    return True


@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    ip = request.client.host if request.client else "unknown"
    if not _check_rate_limit(ip):
        logger.warning("Rate limit exceeded for IP: %s", ip)
        return JSONResponse(status_code=429, content={"detail": "Too many requests"})
    return await call_next(request)


@app.post("/webhook")
async def handle_webhook(
    request: Request,
    x_ghl_signature: str = Header(None, alias="x-ghl-signature"),
):
    payload = await request.body()

    if WEBHOOK_SECRET and not verify_webhook_signature(payload, x_ghl_signature or "", WEBHOOK_SECRET):
        logger.warning("Webhook signature verification failed")
        raise HTTPException(status_code=401, detail="Invalid signature")

    try:
        raw = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON payload")

    event = sanitize_dict(raw)
    event_type = event.get("type", "unknown")
    logger.info("GHL event received: %s", event_type)

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
        logger.info("No handler registered for event type: %s", event_type)

    return JSONResponse({"status": "ok"})


@app.get("/health")
async def health():
    return {"status": "ok"}


# --- Event handlers ---

async def on_contact_create(event: dict):
    logger.info("Contact created: %s", event.get("id"))

async def on_contact_update(event: dict):
    logger.info("Contact updated: %s", event.get("id"))

async def on_contact_delete(event: dict):
    logger.info("Contact deleted: %s", event.get("id"))

async def on_opportunity_create(event: dict):
    logger.info("Opportunity created: %s", event.get("id"))

async def on_opportunity_update(event: dict):
    logger.info("Opportunity updated: %s", event.get("id"))

async def on_opportunity_delete(event: dict):
    logger.info("Opportunity deleted: %s", event.get("id"))

async def on_opportunity_stage_update(event: dict):
    logger.info("Opportunity stage update: %s -> %s", event.get("id"), event.get("stage"))

async def on_opportunity_status_update(event: dict):
    logger.info("Opportunity status update: %s -> %s", event.get("id"), event.get("status"))

async def on_appointment_create(event: dict):
    logger.info("Appointment created: %s", event.get("id"))

async def on_appointment_update(event: dict):
    logger.info("Appointment updated: %s", event.get("id"))

async def on_appointment_delete(event: dict):
    logger.info("Appointment deleted: %s", event.get("id"))

async def on_form_submission(event: dict):
    logger.info("Form submission: %s", event.get("formId"))

async def on_survey_submission(event: dict):
    logger.info("Survey submission: %s", event.get("surveyId"))

async def on_inbound_message(event: dict):
    logger.info("Inbound message from contact: %s", event.get("contactId"))

async def on_outbound_message(event: dict):
    logger.info("Outbound message to contact: %s", event.get("contactId"))

async def on_note_create(event: dict):
    logger.info("Note created on contact: %s", event.get("contactId"))

async def on_task_create(event: dict):
    logger.info("Task created on contact: %s", event.get("contactId"))

async def on_task_complete(event: dict):
    logger.info("Task completed on contact: %s", event.get("contactId"))


if __name__ == "__main__":
    uvicorn.run("webhook_server:app", host="0.0.0.0", port=PORT, reload=False)
