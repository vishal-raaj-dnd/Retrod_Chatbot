import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Add project root directory to sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'retrod_backend.settings')
django.setup()

from apps.core.chat_manager import process_incoming_message

def run_test():
    test_queries = [
        "hi",
        "1",
        "2",
        "3",
        "4"
    ]

    for query in test_queries:
        print(f"\n==========================================")
        print(f"USER QUERY: {query}")
        print(f"==========================================")
        reply = process_incoming_message("whatsapp:+12345", query, "Staff User")
        print(f"BOT RESPONSE:\n{reply}\n")

if __name__ == "__main__":
    run_test()
