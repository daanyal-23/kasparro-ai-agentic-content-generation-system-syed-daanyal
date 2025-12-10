import pytest
from src.agents.question_generator_agent import generate_questions


@pytest.fixture
def facts():
    return {
        "name": "GlowBoost Vitamin C Serum",
        "ingredients": ["Vitamin C", "Hyaluronic Acid"],
        "benefits": ["Brightening", "Hydration"],
        "price": {"amount": 699, "currency": "INR"},
        "how_to_use": "Apply 2–3 drops daily.",
        "side_effects": "Mild tingling."
    }


def test_generate_questions_count(facts):
    qs = generate_questions(facts)
    assert len(qs) >= 15, "Should generate at least 15 questions"


def test_generate_questions_categories(facts):
    qs = generate_questions(facts)
    cats = {q["category"] for q in qs}
    assert "Informational" in cats
    assert "Usage" in cats
    assert "Safety" in cats


def test_generate_questions_ingredient_related(facts):
    qs = generate_questions(facts)
    ing_qs = [q for q in qs if "contain" in q["question"].lower()]
    assert len(ing_qs) >= 1
