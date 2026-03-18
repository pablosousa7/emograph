import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from datetime import datetime
from typing import List, Dict
import uuid
from core.advice_engine import infer_personality  # <-- novo import

class MemoryStore:
    def __init__(self):
        self.client = chromadb.PersistentClient(path="./chroma_db")
        self.embedding_function = SentenceTransformerEmbeddingFunction(
            model_name="paraphrase-multilingual-MiniLM-L12-v2"
        )
        self.collection = self.client.get_or_create_collection(
            name="emograph_memories",
            embedding_function=self.embedding_function
        )

    def add_memory(self, user_id: str, text: str, emotions: List[Dict], metadata: Dict):
        doc_id = str(uuid.uuid4())
        self.collection.add(
            documents=[text],
            ids=[doc_id],
            metadatas=[{
                "user_id": user_id,
                "timestamp": datetime.utcnow().isoformat(),
                "emotions": str(emotions),
                **metadata
            }]
        )

    def recall(self, user_id: str, query: str, limit: int = 5) -> List[Dict]:
        results = self.collection.query(
            query_texts=[query],
            n_results=limit,
            where={"user_id": user_id}
        )
        
        memories = []
        for i in range(len(results["documents"][0])):
            meta = results["metadatas"][0][i]
            memories.append({
                "text": results["documents"][0][i],
                "emotions": eval(meta["emotions"]),
                "timestamp": meta["timestamp"],
                "similarity": results["distances"][0][i]
            })
        return memories

    def get_emotional_trends(self, user_id: str, days: int = 30) -> dict:
        results = self.collection.query(query_texts=[""], n_results=50, where={"user_id": user_id})
        trends = {"sadness_trend": 0, "anger_recurrence": 0, "total_memories": 0}
        if not results["documents"][0]:
            return trends
        for meta in results["metadatas"][0]:
            emotions = eval(meta["emotions"])
            for e in emotions:
                if e["emotion"].lower() in ["sadness", "grief"] and e["score"] > 0.4:
                    trends["sadness_trend"] += 1
                if e["emotion"].lower() in ["anger", "rage"] and e["score"] > 0.5:
                    trends["anger_recurrence"] += 1
            trends["total_memories"] += 1
        return trends

    def get_or_update_profile(self, user_id: str, text: str, emotions: List[Dict]) -> Dict:
        profile_collection = self.client.get_or_create_collection(name="user_profiles")
        new_traits = infer_personality(text, emotions)
        profile_collection.add(
            documents=["profile"],
            ids=[user_id],
            metadatas=[{"user_id": user_id, **new_traits}]
        )
        return new_traits