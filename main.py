from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from datetime import datetime
import logging
from core.models import IngestRequest, RecallRequest, RecallResponse
from core.emotion_detector import detect_emotions
from core.memory_store import MemoryStore

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
        return {"status": "success", "emotions_detected": emotions, "message": "Memória emocional salva!"}
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