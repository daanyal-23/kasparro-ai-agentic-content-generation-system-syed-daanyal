import argparse
import logging
from src.orchestrator import run_pipeline

logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s:%(message)s")


def main():
    parser = argparse.ArgumentParser(description="Run Agentic Content Generation Pipeline (local)")
    parser.add_argument("--input", "-i", required=True, help="Path to product JSON input")
    parser.add_argument("--outdir", "-o", default="out", help="Output directory")
    args = parser.parse_args()
    artifacts = run_pipeline(args.input, args.outdir)
    print("Pipeline finished. Outputs written to", args.outdir)
    # Print small summary
    print("Product title:", artifacts["product_page"].get("title"))
    print("FAQ count:", len(artifacts["faq"]))
    print("Comparison verdict:", artifacts["comparison"].get("verdict"))


if __name__ == "__main__":
    main()
