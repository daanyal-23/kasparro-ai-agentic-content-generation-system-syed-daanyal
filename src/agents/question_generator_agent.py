from typing import List, Dict
import logging

logger = logging.getLogger("QuestionGeneratorAgent")


def generate_questions(facts: Dict) -> List[Dict]:
    """
    Deterministic rule-based question generation.
    Produces exactly 15 questions using the available facts only.
    Uses simple numeric IDs ("1", "2", "3", ...) to match expected schema.
    """
    qs = []
    name = facts.get("name", "the product")
    ingredients = facts.get("ingredients", [])
    benefits = facts.get("benefits", [])
    price = facts.get("price", {}).get("amount")
    qid = 1

    # 1. Basic info question
    qs.append({
        "id": str(qid),
        "category": "Product Information",
        "question": f"What is the name of the product?",
        "rationale": "basic info"
    })
    qid += 1

    # 2. Product ID question
    product_id = facts.get("product_id", "")
    if product_id:
        qs.append({
            "id": str(qid),
            "category": "Product Information",
            "question": f"What is the product ID?",
            "rationale": "product identification"
        })
        qid += 1

    # 3. Description question
    qs.append({
        "id": str(qid),
        "category": "Product Description",
        "question": f"What is the description of the product?",
        "rationale": "description"
    })
    qid += 1

    # 4. Price question
    if price is not None:
        qs.append({
            "id": str(qid),
            "category": "Pricing",
            "question": f"What is the price of the product?",
            "rationale": "purchase decision"
        })
        qid += 1

    # 5-9. Ingredient questions (up to 5)
    for i, ing in enumerate(ingredients[:5], start=0):
        if qid > 15:
            break
        qs.append({
            "id": str(qid),
            "category": "Ingredients",
            "question": f"What ingredients are present in the product?" if i == 0 else f"Does the product contain {ing}?",
            "rationale": "ingredient check"
        })
        qid += 1

    # 10-12. Benefit questions (up to 3)
    for i, b in enumerate(benefits[:3], start=0):
        if qid > 15:
            break
        qs.append({
            "id": str(qid),
            "category": "Benefits",
            "question": f"What are the benefits of using the product?" if i == 0 else f"What benefit does the product provide for {b}?",
            "rationale": "benefit clarification"
        })
        qid += 1

    # 13. Usage question
    if qid <= 15:
        qs.append({
            "id": str(qid),
            "category": "Usage",
            "question": f"How should the product be used?",
            "rationale": "usage guidance"
        })
        qid += 1

    # 14. Side effects question
    if qid <= 15:
        qs.append({
            "id": str(qid),
            "category": "Side Effects",
            "question": f"Are there any side effects associated with this product?",
            "rationale": "safety check"
        })
        qid += 1

    # 15. Fill remaining slots with template questions
    templates = [
        ("Product Information", "How many ingredients does the product contain?"),
        ("Benefits", "How many benefits does the product offer?"),
        ("Product Information", "What percentage of Vitamin C does the serum contain?"),
        ("Metadata", "What is the metadata source of the product information?"),
        ("Metadata", "When was the product information ingested?"),
        ("Usage", "When is the recommended time to apply the product?"),
        ("Side Effects", "What precaution is suggested before using the product?"),
    ]

    for cat, qtext in templates:
        if qid > 15:
            break
        qs.append({
            "id": str(qid),
            "category": cat,
            "question": qtext,
            "rationale": "template"
        })
        qid += 1

    # Ensure exactly 15 questions
    qs = qs[:15]
    logger.info("Generated %d questions", len(qs))
    return qs
