from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime

class IngestRequest(BaseModel):
    user_id: str
    text: str
    metadata: Dict = {}

class RecallRequest(BaseModel):
    user_id: str
    query: str
    limit: int = 5

class MemoryItem(BaseModel):
    text: str
    emotions: List[Dict]
    timestamp: str
    similarity: float

class RecallResponse(BaseModel):
    memories: List[MemoryItem]

class SmartRecallResponse(BaseModel):
    memories: List[MemoryItem]
    emotional_trends: dict
    safe_advice: dict
    summary: str