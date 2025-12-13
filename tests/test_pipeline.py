from pathlib import Path
from src.graph import run_graph

def test_full_pipeline(tmp_path):
    input_path = "examples/sample_product.json"
    outdir = tmp_path / "out"

    state = run_graph(input_path=str(input_path), outdir=str(outdir))

    assert (outdir / "product_page.json").exists()
    assert (outdir / "faq.json").exists()
    assert (outdir / "comparison_page.json").exists()

    # Optional sanity checks
    assert state.product_page is not None
    assert len(state.faq) >= 15
    assert state.comparison is not None
