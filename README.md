# EmoGraph – Infinite Emotional Memory for AIs

**The first Brazilian API for persistent emotional memory for any LLM.**

Inspired by Supermemory.ai, but 100% focused on **emotions** (the biggest missing piece in AI today).

### What it does
- Detects **27 emotions** in Portuguese (and any language) using open-source 2026 models
- Stores everything in a **persistent vector database** (never loses data)
- Lets any AI remember the user’s emotional state forever
- Simple, fast, production-ready API

### Real-world examples
- Emotional companion: “I remember you were anxious about the exam last week…”
- Customer support: responds with real empathy based on past interactions
- AI tutor: adapts lessons to the student’s mood
- Digital therapy: tracks emotional progress over months

### Current status (March 2026)
✅ MVP v0.1 live  
✅ Multilingual emotion detection  
✅ Persistent vector memory (ChromaDB)  
✅ /ingest and /recall endpoints  
✅ Automatic Swagger UI  
🔄 Next: public deployment + Telegram/WhatsApp + Neo4j graph

### Tech stack
- Python + FastAPI
- Hugging Face (model: AnasAlokla/multilingual_go_emotions_V1.2)
- ChromaDB + SentenceTransformers (multilingual embeddings)
- Pydantic + CORS

### How to run locally (2 minutes)

```bash
pip install -r requirements.txt
python main.py
