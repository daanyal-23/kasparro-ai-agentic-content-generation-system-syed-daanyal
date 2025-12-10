from typing import Dict, Any, List
from ..models import ProductModel
import logging

logger = logging.getLogger("FactsExtractorAgent")


def extract_facts(product: ProductModel) -> Dict[str, Any]:
    """
    Turn ProductModel into a facts bag: atomic facts suitable for rule-driven generation.
    """
    facts = {
        "product_id": product.id,
        "name": product.name,
        "description": product.description,
        "price": {"amount": product.price, "currency": product.currency},
        "ingredients": product.ingredients[:],  # copy
        "benefits": product.benefits[:],
        "how_to_use": product.how_to_use,
        "side_effects": product.side_effects,
        "metadata": product.metadata,
    }
    # Atomicize some facts
    facts["ingredient_count"] = len(facts["ingredients"])
    facts["benefit_count"] = len(facts["benefits"])
    logger.debug("Extracted %d atomic facts", facts["ingredient_count"])
    return facts
