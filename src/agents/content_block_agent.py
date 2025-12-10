from typing import Dict, Any, List
import logging

logger = logging.getLogger("ContentBlockAgent")


def generate_summary_block(facts: Dict) -> Dict[str, Any]:
    name = facts.get("name", "")
    desc = facts.get("description", "")
    benefits = facts.get("benefits", [])
    summary = desc or (f"{name} — {" + ", ".join(benefits[:3]) + "}" if benefits else name)
    # Keep summary short (max 2 sentences)
    return {"type": "summary", "text": (summary if len(summary) < 280 else summary[:277] + "...")}


def generate_ingredients_block(facts: Dict) -> Dict[str, Any]:
    ing = facts.get("ingredients", [])
    return {"type": "ingredients", "items": ing}


def generate_benefits_block(facts: Dict) -> Dict[str, Any]:
    benefits = facts.get("benefits", [])
    bullets = [{"id": f"b{i+1}", "text": b} for i, b in enumerate(benefits)]
    return {"type": "benefits", "items": bullets}


def generate_usage_block(facts: Dict) -> Dict[str, Any]:
    usage = facts.get("how_to_use", "") or "Follow product label instructions."
    return {"type": "usage", "text": usage}


def generate_safety_block(facts: Dict) -> Dict[str, Any]:
    s = facts.get("side_effects", "") or "No common side effects listed; patch test recommended."
    return {"type": "safety", "text": s}


def generate_price_block(facts: Dict) -> Dict[str, Any]:
    price = facts.get("price", {})
    return {"type": "price", "amount": price.get("amount"), "currency": price.get("currency", "INR")}
