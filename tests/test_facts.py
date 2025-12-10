import pytest
from src.models import ProductModel
from src.agents.facts_extractor_agent import extract_facts


@pytest.fixture
def product():
    return ProductModel(
        id="p1",
        name="GlowBoost Vitamin C Serum",
        description="Brightening Vitamin C serum.",
        price=699,
        currency="INR",
        ingredients=["Vitamin C", "Hyaluronic Acid"],
        benefits=["Brightening", "Hydration"],
        how_to_use="Apply 2–3 drops daily.",
        side_effects="Mild tingling.",
        metadata={"source": "test"}
    )


def test_extract_facts_basic(product):
    facts = extract_facts(product)
    assert facts["name"] == "GlowBoost Vitamin C Serum"
    assert facts["price"]["amount"] == 699
    assert len(facts["ingredients"]) == 2
    assert len(facts["benefits"]) == 2
    assert "how_to_use" in facts
    assert "side_effects" in facts


def test_extract_facts_counts(product):
    facts = extract_facts(product)
    assert facts["ingredient_count"] == 2
    assert facts["benefit_count"] == 2
