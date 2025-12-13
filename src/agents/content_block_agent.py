from typing import Dict, Any, List
import logging

logger = logging.getLogger("ContentBlockAgent")


def generate_summary_block(facts: Dict) -> Dict[str, Any]:
    name = facts.get("name", "")
    desc = facts.get("description", "")
    benefits = facts.get("benefits", [])
    summary = desc or (f"{name} — {" + ", ".join(benefits[:3]) + "}" if benefits else name)
    # Keep summary short (max 2 sentences)
    # Match expected schema: {"title": "Summary", "text": "..."}
    return {"title": "Summary", "text": (summary if len(summary) < 280 else summary[:277] + "...")}


def generate_ingredients_block(facts: Dict) -> List[Dict[str, Any]]:
    # Match expected schema: List[{"name": "...", "description": "..."}]
    ing = facts.get("ingredients", [])
    return [{"name": item, "description": ""} for item in ing]


def generate_benefits_block(facts: Dict) -> List[Dict[str, Any]]:
    # Match expected schema: List[{"benefit": "...", "details": "..."}]
    benefits = facts.get("benefits", [])
    return [{"benefit": b, "details": ""} for b in benefits]


def generate_usage_block(facts: Dict) -> Dict[str, Any]:
    # Match expected schema: {"title": "Usage Instructions", "text": "..."}
    usage = facts.get("how_to_use", "") or "Follow product label instructions."
    return {"title": "Usage Instructions", "text": usage}


def generate_safety_block(facts: Dict) -> Dict[str, Any]:
    # Match expected schema: {"title": "Safety Information", "text": "..."}
    s = facts.get("side_effects", "") or "No common side effects listed; patch test recommended."
    return {"title": "Safety Information", "text": s}


def generate_price_block(facts: Dict) -> Dict[str, Any]:
    # Match expected schema: {"amount": number, "currency": string}
    price = facts.get("price", {})
    return {"amount": price.get("amount", 0), "currency": price.get("currency", "INR")}
