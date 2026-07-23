# Retrod PMS AI Chatbot 🤖🏨

An intelligent AI WhatsApp assistant for **Property Management Systems (Retrod PMS)**. Built with Django, Groq (`llama-3.3-70b-versatile`), Twilio WhatsApp API, and RAG vector search over official PMS Specification documents and frontend route directories.

---

## 🌟 Key Features

1. **WhatsApp Twilio Webhook Integration:** Real-time bi-directional WhatsApp messaging with TwiML responses.
2. **Internal Staff Assistance:** Real-time AI guidance for room operations, reservations, check-ins, folios, and PMS workflows.
3. **Website & CRM Navigation Helper:** Returns direct live links (`https://pms-ui-ten.vercel.app/...`) formatted as prominent WhatsApp CTA link buttons along with required permissions (`reservations.create`, `frontdesk.checkin`, etc.).
4. **RAG Architecture:** Operates on 224 Knowledge Base chunks extracted from the official Retrod PMS Specification `.docx` document and System Route Directory.
5. **Groq LLM Acceleration:** Powered by Groq's `llama-3.3-70b-versatile` model for ultra-fast, 2-3 bullet point responses.

---

## 📂 Project Architecture

```text
retrod_Chatbot/
├── apps/
│   ├── ai_engine/           # Knowledge Base models, vector search & RAG ingestion
│   │   ├── management/
│   │   │   └── commands/
│   │   │       └── ingest_knowledge.py   # python manage.py ingest_knowledge
│   │   ├── models.py        # KnowledgeChunk model
│   │   ├── ingest_srs.py    # SRS document parser
│   │   └── ingest_routes.py # Website route directory parser
│   ├── core/                # Intent classification & Chat Manager
│   │   ├── chat_manager.py  # RAG search & Groq LLM prompt engine
│   ├── integrations/        # Channel Webhooks
│   │   ├── views.py         # WhatsApp Twilio Webhook endpoint
│   │   └── urls.py          # /api/v1/integrations/whatsapp/webhook/
├── retrod_backend/          # Main Django settings & URLs
│   ├── settings.py
│   └── urls.py
├── .env                     # API keys & Twilio credentials
├── .gitignore
├── manage.py
└── test_chat.py             # Local CLI chat test script
```

---

## 🚀 Getting Started

### 1. Environment Setup
```powershell
python -m venv venv
.\venv\Scripts\activate
pip install django djangorestframework python-dotenv twilio redis celery openai groq python-docx
```

### 2. Database & Knowledge Ingestion
```powershell
python manage.py migrate
python manage.py ingest_knowledge
```

### 3. Running local server
```powershell
python manage.py runserver 8000
```

### 4. Live WhatsApp Testing via Ngrok
Expose port 8000 using Ngrok:
```powershell
npx ngrok http 8000
```
Set your **Twilio WhatsApp Sandbox Webhook URL** to:
`https://<your-ngrok-url>.ngrok-free.app/api/v1/integrations/whatsapp/webhook/` (HTTP POST).

---

## 🔑 Environment Variables (`.env`)

| Variable | Description |
| :--- | :--- |
| `TWILIO_ACCOUNT_SID` | Twilio Account SID |
| `TWILIO_AUTH_TOKEN` | Twilio Auth Token |
| `TWILIO_WHATSAPP_NUMBER` | Twilio WhatsApp Number (`whatsapp:+14155238886`) |
| `GROQ_API_KEY` | Groq API Key (`gsk_...`) |
| `OPENAI_API_KEY` | OpenAI API Key (Optional Fallback) |
