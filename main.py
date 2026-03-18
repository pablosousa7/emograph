from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from datetime import datetime
import logging
from core.models import IngestRequest, RecallRequest, RecallResponse
from core.emotion_detector import detect_emotions
from core.memory_store import MemoryStore
from core.advice_engine import get_adaptive_advice

app = FastAPI(title="EmoGraph API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

memory = MemoryStore()

logging.basicConfig(level=logging.INFO)

@app.post("/ingest", response_model=dict)
async def ingest(request: IngestRequest):
    try:
        emotions = detect_emotions(request.text)
        memory.add_memory(
            user_id=request.user_id,
            text=request.text,
            emotions=emotions,
            metadata={"source": request.metadata.get("source", "api")}
        )
        return {"status": "success", "emotions_detected": emotions, "message": "Emotional memory saved!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/recall", response_model=RecallResponse)
async def recall(request: RecallRequest):
    try:
        results = memory.recall(user_id=request.user_id, query=request.query, limit=request.limit)
        return RecallResponse(memories=results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

@app.post("/smart_recall")
async def smart_recall(request: RecallRequest):
    try:
        memories = memory.recall(user_id=request.user_id, query=request.query, limit=5)
        trends = memory.get_emotional_trends(request.user_id)
        
        latest_text = memories[0]["text"] if memories else request.query
        latest_emotions = memories[0]["emotions"] if memories else []
        
        personality = memory.get_or_update_profile(request.user_id, latest_text, latest_emotions)
        
        safe_advice = get_adaptive_advice(
            latest_emotions[0]["emotion"] if latest_emotions else "neutral",
            personality,
            latest_text
        )
        
        return {
            "memories": memories,
            "emotional_trends": trends,
            "personality_profile": personality,
            "safe_advice": safe_advice,
            "summary": f"Current state: {latest_emotions[0]['emotion'] if latest_emotions else 'neutral'} | Profile: {max(personality, key=personality.get)}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))