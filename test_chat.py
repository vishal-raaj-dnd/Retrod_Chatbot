import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)


import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'retrod_backend.settings')
django.setup()

from apps.core.chat_manager import process_incoming_message

test_queries = [
    "where can I create a new reservation?",
    "give me the link for check in"
]

for query in test_queries:
    print(f"\n==========================================")
    print(f"USER QUERY: {query}")
    print(f"==========================================")
    reply = process_incoming_message("whatsapp:+12345", query, "Staff User")
    print(f"BOT RESPONSE:\n{reply}\n")

