import os
import sys
import django

# Setup Django Environment
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'retrod_backend.settings')
django.setup()

from apps.ai_engine.models import KnowledgeChunk

BASE_URL = "https://pms-ui-ten.vercel.app"

ROUTES_DATA = [
    # 1. Operations & Front Office
    {"route": "/", "feature": "Dashboard", "perm": "dashboard.view", "desc": "Real-time command center: live occupancy, dynamic room type breakdown, revenue KPIs today vs budget, open work orders, in-house guest metrics."},
    {"route": "/leads", "feature": "Leads & Pipeline", "perm": "dashboard.view", "desc": "Inbound guest inquiries, corporate sales leads, reservation conversion pipeline, and follow-up tracking."},
    {"route": "/front-desk", "feature": "Front Desk Operations", "perm": "frontdesk.view", "desc": "Quick room status overview, expected arrivals/departures, in-house guest roster, and room key assignments."},
    {"route": "/check-in", "feature": "Check-In / Check-Out", "perm": "frontdesk.checkin", "desc": "Guest check-in workflow, express check-out processing, folio settlement check, and room status updates."},
    {"route": "/reservations", "feature": "Reservations List & Timeline", "perm": "reservations.view", "desc": "Interactive timeline view of room bookings, status filters, and daily occupancy percentage headers."},
    {"route": "/reservations/new", "feature": "New Reservation", "perm": "reservations.create", "desc": "Multi-step booking engine with OCR guest document extraction, room allocation, and payment method selection."},
    {"route": "/groups", "feature": "Group Bookings", "perm": "reservations.view", "desc": "Corporate and tour group block reservations, room allocation matrices, master folio setup, and group payments."},
    {"route": "/events", "feature": "Event Bookings", "perm": "reservations.view", "desc": "Banquet, conference hall, and event space reservations, setup timing, catering details, and billing."},
    {"route": "/housekeeping", "feature": "Housekeeping & Room Ops", "perm": "housekeeping.view", "desc": "Live room cleaning status matrix, staff assignment, and maintenance reporting."},
    {"route": "/housekeeping/mobile", "feature": "Housekeeping Mobile View", "perm": "housekeeping.view", "desc": "Optimized mobile interface for cleaning staff to update room status on-the-go."},
    {"route": "/lost-found", "feature": "Lost & Found", "perm": "housekeeping.view", "desc": "Item logging, guest inquiry matching, storage location tracking, and claim verification."},
    {"route": "/maintenance", "feature": "Work Orders & Maintenance", "perm": "maintenance.view", "desc": "Property maintenance ticket console, issue priority, room blocking for maintenance, and repair status tracking."},
    {"route": "/laundry", "feature": "Laundry & Linen Management", "perm": "dashboard.view", "desc": "Guest laundry request submission with room-first guest lookup, service lead time validation, linen stock tracking."},
    {"route": "/dashboard/multi-property", "feature": "Multi-Property Dashboard", "perm": "dashboard.view", "desc": "Executive view aggregating performance metrics, occupancy, and revenue across all group properties."},

    # 2. Guests & CRM
    {"route": "/guests", "feature": "Guest Profiles Directory", "perm": "guests.view", "desc": "Complete guest database with stay history, total spend, preferences, VIP tags, and contact details."},
    {"route": "/notifications", "feature": "Notification Center", "perm": "dashboard.view", "desc": "Real-time system alerts, guest request notifications, stock low alerts, and operational updates."},
    {"route": "/loyalty", "feature": "Loyalty Program", "perm": "guests.view", "desc": "Guest reward points, tier progression (Silver, Gold, Platinum), points redemption, and member benefits."},
    {"route": "/communications", "feature": "Guest Communications", "perm": "guests.view", "desc": "Automated SMS, WhatsApp, and email messaging for pre-arrival greetings, check-in instructions."},
    {"route": "/guest-requests", "feature": "Guest Requests Console", "perm": "guests.view", "desc": "Room service, housekeeping, amenities, and extra luggage request tracking with response timers."},
    {"route": "/feedback", "feature": "Guest Feedback & Reviews", "perm": "guests.view", "desc": "Post-stay survey responses, NPS scores, review sentiment analysis, and staff response logging."},

    # 3. Commercial, Billing & Revenue
    {"route": "/billing", "feature": "Billing & Invoicing", "perm": "billing.view", "desc": "Full folio management, official GST Tax Invoice generator with A4 print layout, PDF download, email template preview."},
    {"route": "/payments", "feature": "Payments Console", "perm": "billing.view", "desc": "Payment transactions log, multi-tender payment splits, and refund logs."},
    {"route": "/taxes-fees", "feature": "Taxes & Fees Setup", "perm": "billing.view", "desc": "GST tax rates setup (CGST 9%, SGST 9%, IGST 18%), service charges, and luxury tax rules."},
    {"route": "/revenue", "feature": "Revenue Management", "perm": "rates.view", "desc": "ADR, RevPAR, Occupancy trend analytics, rate optimization suggestions, and yield management rules."},
    {"route": "/rate-plans", "feature": "Rate Plans", "perm": "rates.view", "desc": "BAR, Corporate, EP/CP/MAP/AP meal plans, promotional rates, and cancellation policies."},
    {"route": "/availability", "feature": "Availability Matrix", "perm": "rates.view", "desc": "Room inventory availability calendar across all room types with stop-sell and minimum stay restrictions."},
    {"route": "/add-ons", "feature": "Add-On Services", "perm": "packages.view", "desc": "Upsell catalog for airport transfers, spa packages, room decoration, and late check-out fees."},
    {"route": "/concierge", "feature": "Concierge Services", "perm": "services.view", "desc": "Tour bookings, restaurant reservations, local attraction ticketing, and guest assistance requests."},
    {"route": "/transport", "feature": "Transportation Management", "perm": "services.view", "desc": "Airport pickup/drop scheduling, driver assignment, vehicle roster, and transport billing."},

    # 4. Channel Manager & Direct Booking
    {"route": "/channel-manager", "feature": "Channel Manager Overview", "perm": "rates.view", "desc": "Live synchronization status with OTAs (Booking.com, Agoda, MakeMyTrip, Expedia, Airbnb)."},
    {"route": "/booking-engine", "feature": "Direct Booking Engine", "perm": "settings.view", "desc": "Guest-facing online reservation widget, room availability search, and instant payment integration."},

    # 5. Point of Sale (POS)
    {"route": "/pos", "feature": "POS Dashboard", "perm": "pos.view", "desc": "Outlet selection (Restaurant, Bar, Room Service, Spa), live table status, and sales summary."},
    {"route": "/pos/new", "feature": "New POS Order", "perm": "pos.create", "desc": "Interactive touch order screen, item search, variant modifiers, table selection, and guest room charge linking."},
    {"route": "/pos/billing", "feature": "POS Billing & Settlement", "perm": "pos.view", "desc": "Settlement terminal for cash, card, UPI, or room charge posting (Room Folio)."},
    {"route": "/pos/kot", "feature": "Kitchen Order Ticket (KOT)", "perm": "pos.view", "desc": "Live KOT kitchen display screen and printer dispatcher for food prep stations."},

    # 6. Intelligence & System Setup
    {"route": "/search", "feature": "Global Search", "perm": "dashboard.view", "desc": "Fast universal search across guests, reservations, rooms, invoices, and work orders."},
    {"route": "/reports", "feature": "Reports & Analytics", "perm": "reports.view", "desc": "Comprehensive library of operational reports (Manager Flash, Police Inquiry, Housekeeping Summary, Tax Return)."},
    {"route": "/rooms", "feature": "Rooms & Inventory Setup", "perm": "rooms.view", "desc": "Room category creation, amenities setup, base occupancy limits, and individual room number inventory."},
    {"route": "/staff", "feature": "Staff Management", "perm": "staff.view", "desc": "Employee directory, department assignments, contact details, and account status."},
    {"route": "/settings", "feature": "System Setup", "perm": "settings.view", "desc": "General property settings, currency formatting, check-in/out default times, logo upload, and invoice headers."}
]

def ingest_routes():
    print("Ingesting website routing details...")
    KnowledgeChunk.objects.filter(source_doc="Website_Routes").delete()

    created_count = 0
    for item in ROUTES_DATA:
        full_url = f"{BASE_URL}{item['route']}"
        title = f"Route: {item['feature']} ({item['route']})"
        content = (
            f"Page Name: {item['feature']}\n"
            f"Direct Page URL: {full_url}\n"
            f"Relative Route: {item['route']}\n"
            f"Required Permission: {item['perm']}\n"
            f"Description: {item['desc']}"
        )

        KnowledgeChunk.objects.create(
            title=title,
            content=content,
            category="website_navigation",
            source_doc="Website_Routes"
        )
        created_count += 1

    print(f"Successfully ingested {created_count} Website Navigation Routes into database!")

if __name__ == "__main__":
    ingest_routes()
