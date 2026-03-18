from transformers import pipeline
from typing import List, Dict
import torch

emotion_pipeline = pipeline(
    "text-classification",
    model="AnasAlokla/multilingual_go_emotions_V1.2",
    top_k=None,
    device="cpu"
)

def detect_emotions(text: str) -> List[Dict]:
    results = emotion_pipeline(text)[0]

    emotions = [
        {"emotion": item["label"], "score": round(item["score"], 4)}
        for item in results if item["score"] > 0.25
    ]
    return emotions[:8] 