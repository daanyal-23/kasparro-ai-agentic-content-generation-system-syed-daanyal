import pytest
from src.agents.comparison_agent import build_fictional_product_b, compare_products


@pytest.fixture
def A():
    return {
        "name": "GlowBoost Vitamin C Serum",
        "ingredients": ["Vitamin C", "Hyaluronic Acid"],
        "benefits": ["Brightening", "Hydration"],
        "price": {"amount": 699, "currency": "INR"}
    }


def test_product_b_price_increase(A):
    B = build_fictional_product_b(A)
    assert B["price"]["amount"] > A["price"]["amount"]


def test_compare_common_ingredients(A):
    B = {
        "name": "Fictional B",
        "ingredients": ["Vitamin C"],
        "benefits": ["Brightening"],
        "price": {"amount": 750, "currency": "INR"}
    }
    comparison = compare_products(A, B)
    assert "Vitamin C" in comparison["comparisons"][0]["common"]
