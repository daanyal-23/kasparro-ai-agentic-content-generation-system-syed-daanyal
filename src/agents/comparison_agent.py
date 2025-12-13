from typing import Dict, Any
import logging

logger = logging.getLogger("ComparisonAgent")


def build_fictional_product_b(facts: Dict[str, Any]) -> Dict[str, Any]:
    """
    Construct a fictional Product B derived from Product A facts only.
    """
    A = facts
    ingredients_A = A.get("ingredients", [])

    B = {
        "name": f"{A.get('name', 'Product A')} (Fictional B)",
        # Subset of ingredients: drop the last ingredient if >1
        "ingredients": ingredients_A[: max(1, len(ingredients_A) - 1)],
        "benefits": A.get("benefits", [])[:],
        "price": {}
    }

    base_price = float(A.get("price", {}).get("amount", 0) or 0)
    B["price"]["amount"] = round(base_price * 1.15, 2) if base_price else 0.0
    B["price"]["currency"] = A.get("price", {}).get("currency", "INR")

    logger.info(
        "Built fictional Product B derived from A (price %.2f -> %.2f)",
        base_price,
        B["price"]["amount"],
    )
    return B


def compare_products(A: Dict[str, Any], B: Dict[str, Any]) -> Dict[str, Any]:
    """
    Comparison logic preserving the original casing of ingredients.
    """
    ingredients_A = A.get("ingredients", [])
    ingredients_B = B.get("ingredients", [])

    # Lowercase sets for comparison
    setA = {i.lower() for i in ingredients_A}
    setB = {i.lower() for i in ingredients_B}

    # Identify matches using lowercase
    common_lower = setA & setB
    A_only_lower = setA - setB
    B_only_lower = setB - setA

    # Restore original casing
    common = [i for i in ingredients_A if i.lower() in common_lower]
    A_only = [i for i in ingredients_A if i.lower() in A_only_lower]
    B_only = [i for i in ingredients_B if i.lower() in B_only_lower]

    priceA = A.get("price", {}).get("amount")
    priceB = B.get("price", {}).get("amount")

    if priceA and priceB:
        if priceA < priceB:
            verdict = "Product A is cheaper"
        elif priceA > priceB:
            verdict = "Product B is cheaper"
        else:
            verdict = "Both priced equally"
    else:
        verdict = "Price comparison unavailable"

    # Get currency for price formatting
    currency = A.get("price", {}).get("currency", "INR")
    
    # Format price comparison as strings (matching LLM schema)
    price_A_only = [f"A price: {priceA} {currency}"] if priceA is not None else []
    price_B_only = [f"B price: {priceB} {currency}"] if priceB is not None else []
    price_common = [f"currency: {currency}"]
    
    return {
        "product_A": {
            "name": A.get("name"),
            "price": {"amount": priceA, "currency": currency} if priceA is not None else {"amount": 0, "currency": currency},
            "ingredients": ingredients_A,
            "benefits": A.get("benefits"),
        },
        "product_B": {
            "name": B.get("name"),
            "price": {"amount": priceB, "currency": currency} if priceB is not None else {"amount": 0, "currency": currency},
            "ingredients": ingredients_B,
            "benefits": B.get("benefits"),
        },
        "comparisons": [
            {
                "aspect": "ingredients",
                "A_only": A_only,
                "B_only": B_only,
                "common": common,
            },
            {
                "aspect": "price",
                "A_only": price_A_only,
                "B_only": price_B_only,
                "common": price_common,
            },
            {
                "aspect": "benefits",
                "A_only": [
                    b for b in A.get("benefits", [])
                    if b not in B.get("benefits", [])
                ],
                "B_only": [
                    b for b in B.get("benefits", [])
                    if b not in A.get("benefits", [])
                ],
                "common": [
                    b for b in A.get("benefits", [])
                    if b in B.get("benefits", [])
                ],
            },
        ],
        "verdict": verdict,
    }
