from typing import List, Dict
import logging

logger = logging.getLogger("QuestionGeneratorAgent")


def generate_questions(facts: Dict) -> List[Dict]:
    """
    Deterministic rule-based question generation.
    Produces many Qs using the available facts only.
    """
    qs = []
    name = facts.get("name", "the product")
    ingredients = facts.get("ingredients", [])
    benefits = facts.get("benefits", [])
    price = facts.get("price", {}).get("amount")

    # Usage and basic info questions
    qs.append({
        "id": "q-info-1",
        "category": "Informational",
        "question": f"What is {name}?",
        "rationale": "basic info"
    })

    if price is not None:
        qs.append({
            "id": "q-price",
            "category": "Purchase",
            "question": f"What is the price of {name}?",
            "rationale": "purchase decision"
        })

    # Benefit-based questions
    for i, b in enumerate(benefits[:10], start=1):
        qs.append({
            "id": f"q-benefit-{i}",
            "category": "Informational",
            "question": f"What does {name} do for {b}?",
            "rationale": "benefit clarification"
        })

    # Ingredient-based questions
    for i, ing in enumerate(ingredients[:10], start=1):
        qs.append({
            "id": f"q-ing-{i}",
            "category": "Informational",
            "question": f"Does {name} contain {ing}?",
            "rationale": "ingredient check"
        })

    # Usage & safety
    qs.append({
        "id": "q-usage",
        "category": "Usage",
        "question": f"How do I use {name}?",
        "rationale": "usage guidance"
    })
    qs.append({
        "id": "q-safety",
        "category": "Safety",
        "question": f"Is {name} safe for sensitive skin?",
        "rationale": "safety check"
    })

    # Ensure at least 15 questions → Add 7 template questions
    base_templates = [
        "When should I use {name}?",
        "How often should I use {name}?",
        "Can {name} be used with sunscreen?",
        "Can {name} be used with retinol?",
        "Will {name} cause irritation?",
        "Is {name} suitable for daily use?",
        "Does {name} work for all skin types?"
    ]

    idx = 100
    for t in base_templates:
        qs.append({
            "id": f"q-tpl-{idx}",
            "category": "Usage",
            "question": t.format(name=name),
            "rationale": "template"
        })
        idx += 1

    logger.info("Generated %d questions", len(qs))
    return qs
