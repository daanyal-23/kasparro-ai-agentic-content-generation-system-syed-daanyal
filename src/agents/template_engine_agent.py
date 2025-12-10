from typing import Dict, Any, List
from .content_block_agent import (
    generate_summary_block,
    generate_ingredients_block,
    generate_benefits_block,
    generate_usage_block,
    generate_safety_block,
    generate_price_block,
)
import logging

logger = logging.getLogger("TemplateEngineAgent")


def render_product_page(facts: Dict[str, Any], template: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Compose content blocks per a simple template definition.
    Template is optional: if not provided we use a default ordering.
    """
    # Default template ordering
    page = {
        "product_id": facts.get("product_id"),
        "title": facts.get("name"),
        "metadata": facts.get("metadata", {}),
    }

    # Blocks
    page["summary_block"] = generate_summary_block(facts)
    page["ingredients_block"] = generate_ingredients_block(facts)
    page["benefits_block"] = generate_benefits_block(facts)
    page["usage_block"] = generate_usage_block(facts)
    page["safety_block"] = generate_safety_block(facts)
    page["price_block"] = generate_price_block(facts)
    return page


def render_faq(questions: List[Dict[str, Any]], facts: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    For each generated question, produce an answer using rule-driven templating.
    Answers only use facts; if no direct fact exists we produce a conservative, safe answer.
    """
    answers = []
    name = facts.get("name", "the product")
    for q in questions:
        qid = q.get("id")
        qtext = q.get("question", "")
        cat = q.get("category", "General")
        # Very small deterministic answer heuristics:
        if "price" in qtext.lower():
            ans = f"The listed price is {facts.get('price', {}).get('amount')} {facts.get('price', {}).get('currency','INR')}."
        elif "how do i use" in qtext.lower() or "how often" in qtext.lower():
            ans = facts.get("how_to_use", "Follow product label instructions.")
        elif "contain" in qtext.lower() or "ingredients" in qtext.lower():
            ing = facts.get("ingredients", [])
            ans = f"{name} contains: {', '.join(ing) if ing else 'No ingredient list available.'}"
        elif "safe" in qtext.lower() or "irritation" in qtext.lower():
            se = facts.get("side_effects", "")
            ans = se or "Patch test recommended for sensitive skin."
        else:
            # fallback short summary
            ans = facts.get("description") or f"{name} is a product for {', '.join(facts.get('benefits', [])[:2])}."
        answers.append({"id": qid, "category": cat, "question": qtext, "answer": ans})
    return answers
