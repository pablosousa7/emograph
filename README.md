# EmoGraph – Infinite Emotional Memory with Adaptive Personality Engine

**The ultimate emotional intelligence layer for any LLM.**

EmoGraph turns any AI into a truly empathetic companion by remembering emotions forever, detecting 27 emotions in real time (any language), learning the user’s personality profile, and delivering personalized, non-generic advice.

### Key Features
- Real-time detection of 27 emotions (joy, sadness, anger, fear, etc.) – works perfectly in Portuguese and English
- Persistent vector memory that never forgets
- Adaptive Personality Engine – automatically learns if the user is action-oriented, stoic, reflective or creative
- Personalized advice engine – no generic responses. Tough guys get career/project momentum suggestions. Reflective users get deep pattern analysis.
- Smart Recall – returns past memories + emotional trends + ready-to-use safe guidance

### Endpoints
- `POST /ingest` – save emotional memory
- `POST /recall` – basic memory search
- `POST /smart_recall` – full intelligence (memories + trends + personality + personalized advice)

### How to run locally
```bash
pip install -r requirements.txt
python main.py