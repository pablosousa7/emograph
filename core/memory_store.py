import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from datetime import datetime
from typing import List, Dict
import uuid

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
                "emotions": str(emotions),  # salvo como string (fácil de ler)
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
                "emotions": eval(meta["emotions"]),  # volta pra lista
                "timestamp": meta["timestamp"],
                "similarity": results["distances"][0][i]
            })
        return memories