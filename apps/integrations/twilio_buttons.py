import logging
import os
import json
from twilio.rest import Client

logger = logging.getLogger(__name__)

def send_native_whatsapp_buttons(to_number: str, profile_name: str = "Staff Member"):
    """
    Sends native WhatsApp GUI Buttons using Twilio Content Template SID (HXffa2708ffafdb33293c7aa54fb8d02db).
    """
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    from_number = os.getenv("TWILIO_WHATSAPP_FROM", "whatsapp:+14155238886")
    content_sid = os.getenv("TWILIO_CONTENT_SID", "HXffa2708ffafdb33293c7aa54fb8d02db")

    if not account_sid or not auth_token:
        logger.warning("Twilio credentials missing for sending native buttons.")
        return False

    try:
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            from_=from_number,
            to=to_number,
            content_sid=content_sid,
            content_variables=json.dumps({"1": profile_name})
        )
        logger.info(f"Native WhatsApp GUI buttons sent to {to_number}. SID: {message.sid}")
        return True
    except Exception as e:
        logger.error(f"Error sending native WhatsApp buttons via Twilio Content API: {e}")
        return False

def get_whatsapp_main_menu(profile_name: str) -> str:
    """
    Fallback menu formatting for WhatsApp messaging.
    """
    return (
        f"👋 Hi *{profile_name}*! Welcome to *Retrod PMS Assistant*.\n\n"
        "Reply with a number or tap an action:\n\n"
        "1️⃣ 📊 *Today's Revenue*\n"
        "2️⃣ 🏨 *Room Occupancy*\n"
        "3️⃣ 🔑 *Today's Check-ins*\n"
        "4️⃣ 🟢 *PMS Backend Health*\n"
        "5️⃣ 🌐 *New Reservation Link*\n\n"
        "💡 _Or ask me any question about PMS workflows or page links!_"
    )
