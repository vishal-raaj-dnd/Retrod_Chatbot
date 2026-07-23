import logging
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from twilio.twiml.messaging_response import MessagingResponse
from apps.core.chat_manager import process_incoming_message

logger = logging.getLogger(__name__)

@csrf_exempt
def whatsapp_webhook(request):
    """
    Twilio WhatsApp Webhook Endpoint.
    Receives incoming POST requests from Twilio WhatsApp Sandbox / Production.
    """
    if request.method != "POST":
        return HttpResponse("Method Not Allowed", status=405)

    sender = request.POST.get("From", "")
    message_body = request.POST.get("Body", "").strip()
    profile_name = request.POST.get("ProfileName", "Staff Member")

    logger.info(f"Incoming WhatsApp message from {sender} ({profile_name}): '{message_body}'")

    # Process message via Core Chat Manager (AI Engine & Intent Classifier)
    bot_reply = process_incoming_message(
        sender_id=sender,
        message=message_body,
        profile_name=profile_name,
        channel="whatsapp"
    )

    # Construct Twilio Messaging TwiML XML Response
    twiml_resp = MessagingResponse()
    twiml_resp.message(bot_reply)

    return HttpResponse(str(twiml_resp), content_type="text/xml")
