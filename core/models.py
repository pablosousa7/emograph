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