# run.py
import argparse
import logging
import os

# -----------------------------------------
# FORCE LOAD .env BEFORE ANYTHING ELSE
# -----------------------------------------
from dotenv import load_dotenv
load_dotenv(".env")   # required for GROQ_API_KEY, OPENAI_API_KEY, etc.

from src.orchestrator import run_pipeline as run_local_pipeline

logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s:%(message)s")

OUTDIR = "out"  # Always use a single output folder


def main():
    parser = argparse.ArgumentParser(description="Run pipeline (local or langchain)")
    parser.add_argument("--input", "-i", required=True, help="Path to product JSON input")
    parser.add_argument(
        "--mode", "-m",
        choices=["local", "langchain"],
        default="local",
        help="Execution mode: local deterministic pipeline or LangChain agentic pipeline"
    )
    args = parser.parse_args()

    # Ensure output directory exists
    os.makedirs(OUTDIR, exist_ok=True)

    if args.mode == "local":
        artifacts = run_local_pipeline(args.input, OUTDIR)
    else:
        from src.langchain_orchestrator import run_langchain_pipeline
        artifacts = run_langchain_pipeline(args.input, OUTDIR)

    print("\nPipeline finished.")
    print("Output Directory:", OUTDIR)
    print("Product Title:", artifacts['product_page'].get('title'))
    print("FAQ Count:", len(artifacts['faq']))
    print("Comparison Verdict:", artifacts['comparison'].get('verdict'))


if __name__ == "__main__":
    main()
