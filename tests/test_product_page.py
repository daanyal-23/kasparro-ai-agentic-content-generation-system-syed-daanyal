import pytest
from src.agents.template_engine_agent import render_product_page


@pytest.fixture
def facts():
    return {
        "product_id": "p1",
        "name": "GlowBoost Vitamin C Serum",
        "description": "Brightening serum.",
        "ingredients": ["Vitamin C"],
        "benefits": ["Brightening"],
        "how_to_use": "Apply daily.",
        "side_effects": "None.",
        "price": {"amount": 699, "currency": "INR"},
        "metadata": {}
    }


def test_product_page_structure(facts):
    page = render_product_page(facts)
    assert "summary_block" in page
    assert "ingredients_block" in page
    assert "benefits_block" in page
    assert "usage_block" in page
    assert "safety_block" in page
    assert "price_block" in page


def test_product_page_title(facts):
    page = render_product_page(facts)
    assert page["title"] == "GlowBoost Vitamin C Serum"
