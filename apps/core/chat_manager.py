import logging
import os
from django.db.models import Q
from groq import Groq
from openai import OpenAI
from apps.ai_engine.models import KnowledgeChunk
from apps.core import pms_api_client
from apps.integrations.twilio_buttons import get_whatsapp_main_menu

logger = logging.getLogger(__name__)

def search_knowledge_base(query: str, limit: int = 5):
    """
    Searches the KnowledgeChunk database for relevant SRS sections and website routes.
    Prioritizes navigation routes if query asks for links/pages.
    """
    lowered = query.lower().strip()
    is_nav_query = any(k in lowered for k in ["link", "url", "where", "page", "route", "find", "open", "direct", "laundry", "pos", "check-in", "checkin", "billing", "reservations"])

    stopwords = {"where", "is", "the", "give", "me", "direct", "link", "for", "page", "open", "find", "can", "how", "do", "you", "what"}
    words = [w for w in lowered.split() if len(w) > 2 and w not in stopwords]
    if not words:
        words = [w for w in lowered.split() if len(w) > 2]

    q_object = Q()
    for word in words:
        q_object |= Q(title__icontains=word) | Q(content__icontains=word)

    if is_nav_query:
        nav_results = list(KnowledgeChunk.objects.filter(category="website_navigation").filter(q_object).distinct()[:4])
        other_results = list(KnowledgeChunk.objects.filter(q_object).exclude(category="website_navigation").distinct()[:2])
        combined = nav_results + other_results
        if not combined:
            combined = list(KnowledgeChunk.objects.filter(category="website_navigation")[:limit])
        return combined

    results = list(KnowledgeChunk.objects.filter(q_object).distinct()[:limit])
    if not results:
        results = list(KnowledgeChunk.objects.all()[:limit])
    return results

def process_incoming_message(sender_id: str, message: str, profile_name: str, channel: str = "whatsapp") -> str:
    """
    Processes incoming staff/user messages using live PMS API actions, stored SRS knowledge, & Groq LLM.
    """
    if not message:
        return get_whatsapp_main_menu(profile_name)

    lowered = message.lower().strip()

    # 1. Main Menu Trigger
    if lowered in ["hi", "hello", "hey", "start", "menu", "options", "0"]:
        return get_whatsapp_main_menu(profile_name)

    # 2. Action Handlers (Numbers & Action Triggers)
    if lowered in ["1", "revenue", "today revenue", "today's revenue", "check revenue"]:
        return pms_api_client.fetch_today_revenue()

    if lowered in ["2", "occupancy", "room occupancy", "check occupancy"]:
        return pms_api_client.fetch_room_occupancy()

    if lowered in ["3", "checkins", "today checkins", "today's checkins", "check-in status"]:
        return pms_api_client.fetch_today_checkins()

    if lowered in ["4", "health", "system health", "pms health", "api health"]:
        return pms_api_client.fetch_system_health()

    if lowered in ["5", "new reservation link", "new booking"]:
        return (
            "To create a new reservation, you need **reservations.create** permission:\n\n"
            "🔘 *OPEN PAGE:*\nhttps://pms-ui-ten.vercel.app/reservations/new"
        )

    # 3. RAG Retrieval & Groq LLM Synthesis
    relevant_chunks = search_knowledge_base(message, limit=5)
    context_text = "\n\n".join([f"--- [{c.title}] ---\n{c.content}" for c in relevant_chunks])

    groq_api_key = os.getenv("GROQ_API_KEY")
    openai_api_key = os.getenv("OPENAI_API_KEY")

    system_prompt = (
        "You are Retrod PMS Assistant, a WhatsApp bot for internal staff assistance and website navigation. "
        "Answer staff questions using ONLY the provided Retrod PMS context below.\n\n"
        "STRICT DOMAIN RULE:\n"
        "1. The ONLY valid domain for Retrod PMS is https://pms-ui-ten.vercel.app. NEVER output retrod-pms.com or any other placeholder domain.\n"
        "2. If a website link or route is involved, ALWAYS format the link as a prominent WhatsApp CTA Button block using https://pms-ui-ten.vercel.app:\n"
        "   🔘 *OPEN PAGE:* https://pms-ui-ten.vercel.app/<route>\n"
        "3. Keep the answer extremely brief and direct (2-3 bullet points max).\n"
        "4. Specify required permissions using *bold* text.\n\n"
        f"Retrod PMS Knowledge Context:\n{context_text}"
    )

    # Groq LLM (llama-3.3-70b-versatile)
    if groq_api_key:
        try:
            client = Groq(api_key=groq_api_key)
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": message}
                ],
                temperature=0.1,
                max_tokens=300
            )
            return completion.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Error calling Groq API: {e}")

    # OpenAI Fallback
    if openai_api_key:
        try:
            client = OpenAI(api_key=openai_api_key)
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": message}
                ],
                max_tokens=300
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Error calling OpenAI API: {e}")

    # Chunk Snippet Fallback
    top_chunk = relevant_chunks[0] if relevant_chunks else None
    if top_chunk:
        return (
            f"📖 *Retrod PMS Assistance: {top_chunk.title}*\n\n"
            f"{top_chunk.content[:300]}...\n\n"
            "💡 _Need more details? Ask away!_"
        )

    return f"Received: *\"{message}\"*\nHow can I help you navigate or operate Retrod PMS?"
