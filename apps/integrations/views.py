import logging
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from twilio.twiml.messaging_response import MessagingResponse
from apps.core.chat_manager import process_incoming_message
from apps.integrations.twilio_buttons import send_native_whatsapp_buttons

logger = logging.getLogger(__name__)

@csrf_exempt
def whatsapp_webhook(request):
    """
    Twilio WhatsApp Webhook Endpoint.
    Handles native WhatsApp GUI buttons and synchronous TwiML responses.
    """
    if request.method != "POST":
        return HttpResponse("Method Not Allowed", status=405)

    sender = request.POST.get("From", "")
    message_body = request.POST.get("Body", "").strip()
    profile_name = request.POST.get("ProfileName", "Staff Member")

    logger.info(f"Incoming WhatsApp message from {sender} ({profile_name}): '{message_body}'")

    lowered = message_body.lower()

    # Trigger Native WhatsApp GUI Buttons for main menu commands
    if lowered in ["hi", "hello", "hey", "start", "menu", "options"]:
        button_sent = send_native_whatsapp_buttons(to_number=sender, profile_name=profile_name)
        if button_sent:
            return HttpResponse("OK", status=200)

    # Process message via Core Chat Manager (AI RAG Engine & Groq LLM / Actions)
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
