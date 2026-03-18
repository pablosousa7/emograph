from typing import Dict, List

def infer_personality(text: str, emotions: List[Dict]) -> Dict[str, float]:
    """Infer user personality traits from text and emotions (lightweight, no extra models)."""
    text_lower = text.lower()
    traits = {
        "action_oriented": 0.0,
        "reflective": 0.0,
        "stoic": 0.0,
        "creative": 0.0
    }

    # Action-oriented / tough guy keywords (projects, career, goals)
    if any(word in text_lower for word in ["project", "career", "business", "startup", "goal", "plan", "work", "build", "launch"]):
        traits["action_oriented"] += 1.0
    if any(e["emotion"].lower() in ["anger", "rage"] for e in emotions):
        traits["stoic"] += 0.5 

    # Reflective / emotional keywords
    if any(word in text_lower for word in ["feel", "sad", "think", "emotion", "why", "life"]):
        traits["reflective"] += 1.0

    # Creative
    if any(word in text_lower for word in ["idea", "create", "design", "art", "story"]):
        traits["creative"] += 1.0

    # Normalize
    total = sum(traits.values()) or 1
    return {k: round(v / total, 2) for k, v in traits.items()}

def get_adaptive_advice(top_emotion: str, personality: Dict[str, float], text: str) -> Dict:
    """Generate personalized, non-generic advice based on personality."""
    emotion = top_emotion.lower()
    advice = {"validation": "", "actionable_step": "", "professional_flag": False}

    # Action-oriented / tough guy profile (priority)
    if personality.get("action_oriented", 0) > 0.4 or personality.get("stoic", 0) > 0.3:
        advice["validation"] = f"I see you're feeling {emotion}. That's valid energy."
        if "anger" in emotion or "rage" in emotion:
            advice["actionable_step"] = "Channel this fire into your next project or career move. What big goal have you been delaying? Let's turn this into momentum."
        elif "sadness" in emotion:
            advice["actionable_step"] = "Use this feeling as fuel to build something meaningful. What's one step toward your next startup or promotion?"
        return advice

    # Reflective profile
    if personality.get("reflective", 0) > 0.4:
        advice["validation"] = f"I understand you're feeling {emotion} right now."
        advice["actionable_step"] = "Take 5 minutes to journal why this hit you. Patterns like this often reveal what needs to change."
        return advice

    # Default safe fallback
    advice["validation"] = f"Your feeling of {emotion} is completely valid."
    advice["actionable_step"] = "Let's focus on one actionable step toward your goals."
    return advice