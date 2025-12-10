import pytest
from src.orchestrator import run_pipeline
from pathlib import Path


def test_pipeline_end_to_end(tmp_path):
    # Prepare temporary product file
    product_json = tmp_path / "product.json"
    product_json.write_text(
        """
        {
            "name": "GlowBoost Vitamin C Serum",
            "description": "Brightening serum.",
            "price": { "amount": 699, "currency": "INR" },
            "ingredients": ["Vitamin C"],
            "benefits": ["Brightening"],
            "how_to_use": "Morning use.",
            "side_effects": "None."
        }
        """
    )

    outdir = tmp_path / "out"

    artifacts = run_pipeline(str(product_json), str(outdir))

    # Assertions
    assert "product_page" in artifacts
    assert "faq" in artifacts
    assert len(artifacts["faq"]) >= 5
    assert "comparison" in artifacts

    # Check output files created
    assert (outdir / "product_page.json").exists()
    assert (outdir / "faq.json").exists()
    assert (outdir / "comparison_page.json").exists()
