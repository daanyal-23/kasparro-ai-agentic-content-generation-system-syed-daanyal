from typing import Tuple, List
from ..models import ProductModel
import logging

logger = logging.getLogger("SanityCheckAgent")


def run_sanity_checks(product: ProductModel) -> Tuple[ProductModel, List[str]]:
    issues = []
    if not product.name:
        issues.append("missing_name")
    if product.price is None:
        issues.append("missing_price")
    if not isinstance(product.ingredients, list):
        issues.append("ingredients_not_list")
    if not product.benefits:
        issues.append("no_benefits_listed")
    # simple numeric check
    if product.price < 0:
        issues.append("negative_price")
    logger.info("Sanity check completed: %d issues", len(issues))
    return product, issues
