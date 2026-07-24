import logging
import os
import requests

logger = logging.getLogger(__name__)

PMS_BASE_URL = os.getenv("PMS_BACKEND_URL", "https://pms-backend-wp9b.onrender.com")

def get_auth_headers():
    """
    Returns authorization headers with JWT Bearer Token if PMS_API_TOKEN is set.
    Bypasses auto-login endpoint to prevent backend rate-limiting/lockouts.
    """
    token = os.getenv("PMS_API_TOKEN", "").strip()
    headers = {"Content-Type": "application/json"}

    if token:
        headers["Authorization"] = f"Bearer {token}"
        return headers, None

    # Do not auto-login with unverified credentials to prevent lockout re-triggers
    return headers, "JWT Token not set. Please add PMS_API_TOKEN to Environment Variables."

def fetch_today_revenue():
    """
    Calls live PMS API for Today's Revenue.
    Returns real backend data on 200 OK, or detailed API status.
    """
    headers, auth_error = get_auth_headers()
    url = f"{PMS_BASE_URL}/api/admin/tenant-dashboard/"

    if auth_error:
        return (
            "⚠️ *Live Revenue Data Access*\n\n"
            f"• *Status:* {auth_error}\n"
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
                "⚠️ *Live Revenue Data Access*\n\n"
                f"• *API Status Code:* HTTP {response.status_code}\n"
                f"• *Backend Response:* {response.text[:150]}\n"
                f"• *Target Endpoint:* `{url}`\n\n"
                "🔘 *OPEN REVENUE DASHBOARD:*\nhttps://pms-ui-ten.vercel.app/revenue"
            )
    except requests.exceptions.Timeout:
        return (
            "⚠️ *Live Revenue Data Access*\n\n"
            "• *Issue:* Request Timed Out (5.0s limit)\n"
            "• *Detail:* Backend server is slow or starting up on Render.\n"
            f"• *Target Endpoint:* `{url}`\n\n"
            "🔘 *OPEN REVENUE DASHBOARD:*\nhttps://pms-ui-ten.vercel.app/revenue"
        )
    except requests.exceptions.RequestException as e:
        return (
            "⚠️ *Live Revenue Data Access*\n\n"
            f"• *Issue:* Network Error ({str(e)})\n"
            f"• *Target Endpoint:* `{url}`\n\n"
            "🔘 *OPEN REVENUE DASHBOARD:*\nhttps://pms-ui-ten.vercel.app/revenue"
        )

def fetch_room_occupancy():
    """
    Calls live PMS API for Room Occupancy & Inventory status.
    """
    headers, auth_error = get_auth_headers()
    url = f"{PMS_BASE_URL}/api/assets/"

    if auth_error:
        return (
            "⚠️ *Live Room Occupancy Access*\n\n"
            f"• *Status:* {auth_error}\n"
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
                "⚠️ *Live Room Occupancy Access*\n\n"
                f"• *API Status Code:* HTTP {response.status_code}\n"
                f"• *Backend Response:* {response.text[:150]}\n"
                f"• *Target Endpoint:* `{url}`\n\n"
                "🔘 *OPEN AVAILABILITY MATRIX:*\nhttps://pms-ui-ten.vercel.app/availability"
            )
    except requests.exceptions.Timeout:
        return (
            "⚠️ *Live Room Occupancy Access*\n\n"
            "• *Issue:* Request Timed Out (5.0s limit)\n"
            "• *Detail:* Backend server is slow or starting up on Render.\n"
            f"• *Target Endpoint:* `{url}`\n\n"
            "🔘 *OPEN AVAILABILITY MATRIX:*\nhttps://pms-ui-ten.vercel.app/availability"
        )
    except requests.exceptions.RequestException as e:
        return (
            "⚠️ *Live Room Occupancy Access*\n\n"
            f"• *Issue:* Network Error ({str(e)})\n"
            f"• *Target Endpoint:* `{url}`\n\n"
            "🔘 *OPEN AVAILABILITY MATRIX:*\nhttps://pms-ui-ten.vercel.app/availability"
        )

def fetch_today_checkins():
    """
    Calls live PMS API for Today's Check-ins.
    """
    headers, auth_error = get_auth_headers()
    url = f"{PMS_BASE_URL}/api/admin/system-usage/"

    if auth_error:
        return (
            "⚠️ *Today's Check-Ins Access*\n\n"
            f"• *Status:* {auth_error}\n"
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
                "⚠️ *Today's Check-Ins Access*\n\n"
                f"• *API Status Code:* HTTP {response.status_code}\n"
                f"• *Backend Response:* {response.text[:150]}\n"
                f"• *Target Endpoint:* `{url}`\n\n"
                "🔘 *OPEN FRONT DESK CHECK-IN:*\nhttps://pms-ui-ten.vercel.app/check-in"
            )
    except requests.exceptions.Timeout:
        return (
            "⚠️ *Today's Check-Ins Access*\n\n"
            "• *Issue:* Request Timed Out (5.0s limit)\n"
            "• *Detail:* Backend server is slow or starting up on Render.\n"
            f"• *Target Endpoint:* `{url}`\n\n"
            "🔘 *OPEN FRONT DESK CHECK-IN:*\nhttps://pms-ui-ten.vercel.app/check-in"
        )
    except requests.exceptions.RequestException as e:
        return (
            "⚠️ *Today's Check-Ins Access*\n\n"
            f"• *Issue:* Network Error ({str(e)})\n"
            f"• *Target Endpoint:* `{url}`\n\n"
            "🔘 *OPEN FRONT DESK CHECK-IN:*\nhttps://pms-ui-ten.vercel.app/check-in"
        )

def fetch_system_health():
    """
    Calls live PMS backend system health endpoint.
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
