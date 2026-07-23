import logging
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from twilio.twiml.messaging_response import MessagingResponse
from apps.core.chat_manager import process_incoming_message
from apps.integrations.tasks import send_whatsapp_async

logger = logging.getLogger(__name__)

@csrf_exempt
def whatsapp_webhook(request):
    """
    Twilio WhatsApp Webhook Endpoint.
    Dispatches task asynchronously to Redis & Celery worker queue.
    Falls back to synchronous TwiML if Redis is offline.
    """
    if request.method != "POST":
        return HttpResponse("Method Not Allowed", status=405)

    sender = request.POST.get("From", "")
    message_body = request.POST.get("Body", "").strip()
    profile_name = request.POST.get("ProfileName", "Staff Member")

    logger.info(f"Incoming WhatsApp webhook from {sender} ({profile_name}): '{message_body}'")

    # 1. Attempt Async dispatch to Redis & Celery
    try:
        send_whatsapp_async.delay(sender, message_body, profile_name)
        logger.info(f"Dispatched task to Redis/Celery queue for {sender}")
        return HttpResponse("OK", status=200)
    except Exception as e:
        logger.warning(f"Redis queue unavailable ({e}). Falling back to synchronous processing...")

    # 2. Synchronous Fallback via TwiML Response
    bot_reply = process_incoming_message(
        sender_id=sender,
        message=message_body,
        profile_name=profile_name,
        channel="whatsapp"
    )

    twiml_resp = MessagingResponse()
    twiml_resp.message(bot_reply)

    return HttpResponse(str(twiml_resp), content_type="text/xml")
