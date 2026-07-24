import logging
import os
import time
import requests

logger = logging.getLogger(__name__)

PMS_BASE_URL = os.getenv("PMS_BACKEND_URL", "https://pms-backend-wp9b.onrender.com")
_CACHED_TOKEN = None
_LOCKOUT_UNTIL_TS = 0
_LOCKOUT_REASON = ""

def get_jwt_token():
    """
    Authenticates against PMS Backend API with lockout backoff safety.
    Prioritizes static PMS_API_TOKEN if set in environment.
    """
    global _CACHED_TOKEN, _LOCKOUT_UNTIL_TS, _LOCKOUT_REASON

    # 1. Use static JWT token if provided
    static_token = os.getenv("PMS_API_TOKEN", "").strip()
    if static_token:
        return static_token, None

    # 2. Return cached token if valid
    if _CACHED_TOKEN:
        return _CACHED_TOKEN, None

    # 3. Check if server lockout window is active
    current_time = time.time()
    if current_time < _LOCKOUT_UNTIL_TS:
        remaining_mins = int((_LOCKOUT_UNTIL_TS - current_time) / 60) + 1
        return None, f"Account Lockout in Progress: Try again in {remaining_mins} minutes."

    username = os.getenv("PMS_USERNAME", "aarav@grandpalace.in")
    password = os.getenv("PMS_PASSWORD", "123456")

    endpoint = f"{PMS_BASE_URL}/api/auth/login/"
    payload = {"email_or_username": username, "password": password}

    try:
        response = requests.post(
            endpoint,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=5.0
        )
        if response.status_code == 200:
            data = response.json()
            token = (
                data.get("access") or 
                data.get("token") or 
                data.get("access_token") or 
                data.get("tokens", {}).get("access")
            )
            if token:
                _CACHED_TOKEN = token
                _LOCKOUT_UNTIL_TS = 0
                return _CACHED_TOKEN, None
            return None, f"HTTP {response.status_code}: Token missing in login response body."
        else:
            resp_text = response.text[:150]
            if "locked" in resp_text.lower():
                # Back off for 10 minutes so lockout timer can count down to 0
                _LOCKOUT_UNTIL_TS = time.time() + 600
                _LOCKOUT_REASON = resp_text
            return None, f"HTTP {response.status_code}: {resp_text}"
    except requests.exceptions.Timeout:
        return None, "Connection Timeout (5.0s limit exceeded while reaching auth server)."
    except requests.exceptions.RequestException as e:
        return None, f"Network Connection Error: {str(e)}"

def get_auth_headers():
    """
    Returns authorization headers with JWT Bearer Token, or tuple with error message.
    """
    token, error_msg = get_jwt_token()
    if token:
        return {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}, None
    return {"Content-Type": "application/json"}, error_msg

def fetch_today_revenue():
    """
    Calls live PMS API for Today's Revenue.
    Returns real backend data on 200 OK, or detailed API error diagnostic if failed.
    """
    headers, auth_error = get_auth_headers()
    url = f"{PMS_BASE_URL}/api/admin/tenant-dashboard/"

    if auth_error:
        return (
            "⚠️ *Unable to retrieve Live Revenue Data*\n\n"
            "• *Issue:* Authentication Failed\n"
            f"• *Detail:* {auth_error}\n"
            f"• *Target Endpoint:* `{url}`\n\n"
            "🔘 *OPEN REVENUE DASHBOARD:*\nhttps://pms-ui-ten.vercel.app/revenue"
        )

    try:
        response = requests.get(url, headers=headers, timeout=5.0)
        if response.status_code == 200:
            data = response.json()
            revenue = data.get("today_revenue") or data.get("revenue") or data.get("total_revenue")
            occupancy = data.get("occupancy_rate") or data.get("occupancy")
            return (
                f"📊 *Live Retrod PMS Revenue Summary*\n\n"
                f"• *Today's Revenue:* {revenue if revenue is not None else 'N/A'}\n"
                f"• *Occupancy Rate:* {occupancy if occupancy is not None else 'N/A'}\n\n"
                "🔘 *OPEN REVENUE DASHBOARD:*\nhttps://pms-ui-ten.vercel.app/revenue"
            )
        else:
            return (
                "⚠️ *Unable to retrieve Live Revenue Data*\n\n"
                f"• *API Status Code:* HTTP {response.status_code}\n"
                f"• *Backend Response:* {response.text[:150]}\n"
                f"• *Target Endpoint:* `{url}`\n\n"
                "🔘 *OPEN REVENUE DASHBOARD:*\nhttps://pms-ui-ten.vercel.app/revenue"
            )
    except requests.exceptions.Timeout:
        return (
            "⚠️ *Unable to retrieve Live Revenue Data*\n\n"
            "• *Issue:* Request Timed Out (5.0s limit)\n"
            "• *Detail:* Backend server is slow or starting up on Render.\n"
            f"• *Target Endpoint:* `{url}`\n\n"
            "🔘 *OPEN REVENUE DASHBOARD:*\nhttps://pms-ui-ten.vercel.app/revenue"
        )
    except requests.exceptions.RequestException as e:
        return (
            "⚠️ *Unable to retrieve Live Revenue Data*\n\n"
            f"• *Issue:* Network Error ({str(e)})\n"
            f"• *Target Endpoint:* `{url}`\n\n"
            "🔘 *OPEN REVENUE DASHBOARD:*\nhttps://pms-ui-ten.vercel.app/revenue"
        )

def fetch_room_occupancy():
    """
    Calls live PMS API for Room Occupancy & Inventory status.
    Returns real backend data on 200 OK, or detailed API error diagnostic if failed.
    """
    headers, auth_error = get_auth_headers()
    url = f"{PMS_BASE_URL}/api/assets/"

    if auth_error:
        return (
            "⚠️ *Unable to retrieve Live Room Occupancy*\n\n"
            "• *Issue:* Authentication Failed\n"
            f"• *Detail:* {auth_error}\n"
            f"• *Target Endpoint:* `{url}`\n\n"
            "🔘 *OPEN AVAILABILITY MATRIX:*\nhttps://pms-ui-ten.vercel.app/availability"
        )

    try:
        response = requests.get(url, headers=headers, timeout=5.0)
        if response.status_code == 200:
            data = response.json()
            total_assets = data.get("count") if isinstance(data, dict) else len(data)
            return (
                f"🏨 *Live Retrod PMS Room & Asset Occupancy*\n\n"
                f"• *Total Asset Count:* {total_assets}\n\n"
                "🔘 *OPEN AVAILABILITY MATRIX:*\nhttps://pms-ui-ten.vercel.app/availability"
            )
        else:
            return (
                "⚠️ *Unable to retrieve Live Room Occupancy*\n\n"
                f"• *API Status Code:* HTTP {response.status_code}\n"
                f"• *Backend Response:* {response.text[:150]}\n"
                f"• *Target Endpoint:* `{url}`\n\n"
                "🔘 *OPEN AVAILABILITY MATRIX:*\nhttps://pms-ui-ten.vercel.app/availability"
            )
    except requests.exceptions.Timeout:
        return (
            "⚠️ *Unable to retrieve Live Room Occupancy*\n\n"
            "• *Issue:* Request Timed Out (5.0s limit)\n"
            "• *Detail:* Backend server is slow or starting up on Render.\n"
            f"• *Target Endpoint:* `{url}`\n\n"
            "🔘 *OPEN AVAILABILITY MATRIX:*\nhttps://pms-ui-ten.vercel.app/availability"
        )
    except requests.exceptions.RequestException as e:
        return (
            "⚠️ *Unable to retrieve Live Room Occupancy*\n\n"
            f"• *Issue:* Network Error ({str(e)})\n"
            f"• *Target Endpoint:* `{url}`\n\n"
            "🔘 *OPEN AVAILABILITY MATRIX:*\nhttps://pms-ui-ten.vercel.app/availability"
        )

def fetch_today_checkins():
    """
    Calls live PMS API for Today's Check-ins.
    Returns real backend data on 200 OK, or detailed API error diagnostic if failed.
    """
    headers, auth_error = get_auth_headers()
    url = f"{PMS_BASE_URL}/api/admin/system-usage/"

    if auth_error:
        return (
            "⚠️ *Unable to retrieve Today's Check-Ins*\n\n"
            "• *Issue:* Authentication Failed\n"
            f"• *Detail:* {auth_error}\n"
            f"• *Target Endpoint:* `{url}`\n\n"
            "🔘 *OPEN FRONT DESK CHECK-IN:*\nhttps://pms-ui-ten.vercel.app/check-in"
        )

    try:
        response = requests.get(url, headers=headers, timeout=5.0)
        if response.status_code == 200:
            data = response.json()
            return (
                "🔑 *Live Retrod PMS Check-Ins Summary*\n\n"
                f"• *Backend Data:* {str(data)[:200]}\n\n"
                "🔘 *OPEN FRONT DESK CHECK-IN:*\nhttps://pms-ui-ten.vercel.app/check-in"
            )
        else:
            return (
                "⚠️ *Unable to retrieve Today's Check-Ins*\n\n"
                f"• *API Status Code:* HTTP {response.status_code}\n"
                f"• *Backend Response:* {response.text[:150]}\n"
                f"• *Target Endpoint:* `{url}`\n\n"
                "🔘 *OPEN FRONT DESK CHECK-IN:*\nhttps://pms-ui-ten.vercel.app/check-in"
            )
    except requests.exceptions.Timeout:
        return (
            "⚠️ *Unable to retrieve Today's Check-Ins*\n\n"
            "• *Issue:* Request Timed Out (5.0s limit)\n"
            "• *Detail:* Backend server is slow or starting up on Render.\n"
            f"• *Target Endpoint:* `{url}`\n\n"
            "🔘 *OPEN FRONT DESK CHECK-IN:*\nhttps://pms-ui-ten.vercel.app/check-in"
        )
    except requests.exceptions.RequestException as e:
        return (
            "⚠️ *Unable to retrieve Today's Check-Ins*\n\n"
            f"• *Issue:* Network Error ({str(e)})\n"
            f"• *Target Endpoint:* `{url}`\n\n"
            "🔘 *OPEN FRONT DESK CHECK-IN:*\nhttps://pms-ui-ten.vercel.app/check-in"
        )

def fetch_system_health():
    """
    Calls live PMS backend system health endpoint.
    Returns real status or exact error diagnostics.
    """
    url = f"{PMS_BASE_URL}/api/admin/system-health/"
    try:
        response = requests.get(url, timeout=5.0)
        if response.status_code == 200:
            return f"🟢 *Retrod PMS Backend API:* Operational (200 OK)\n\n• *Response Body:* {response.text[:200]}"
        else:
            return f"⚠️ *Retrod PMS Backend API Warning*\n\n• *Status:* HTTP {response.status_code}\n• *Target Endpoint:* `{url}`\n• *Response:* {response.text[:200]}"
    except Exception as e:
        return f"🔴 *Retrod PMS Backend API Offline / Unreachable*\n\n• *Error:* {str(e)}\n• *Target Endpoint:* `{url}`"
