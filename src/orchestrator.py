from typing import Dict, Any
import logging

# Correct imports matching your folder structure
from .agents.ingest_agent import ingest_from_file
from .agents.sanity_agent import run_sanity_checks
from .agents.facts_extractor_agent import extract_facts
from .agents.question_generator_agent import generate_questions
from .agents.content_block_agent import generate_summary_block  # (kept for reference)
from .agents.template_engine_agent import render_product_page, render_faq
from .agents.comparison_agent import build_fictional_product_b, compare_products
from .agents.renderer_agent import write_outputs

logger = logging.getLogger("Orchestrator")


def run_pipeline(input_path: str, outdir: str) -> Dict[str, Any]:
    """
    Full pipeline execution:
    1. Ingest product JSON
    2. Validate & sanity-check
    3. Extract atomic facts
    4. Generate questions
    5. Render product page + FAQ
    6. Generate fictional Product B and comparison page
    7. Write structured outputs to disk
    """

    # 1. Ingest
    product = ingest_from_file(input_path)

    # 2. Sanity
    product, issues = run_sanity_checks(product)
    if issues:
        logger.warning("Sanity issues found: %s", issues)

    # 3. Facts extraction
    facts = extract_facts(product)

    # 4. Question generation
    questions = generate_questions(facts)

    # 5. Render product page & FAQ
    product_page = render_product_page(facts)
    faq = render_faq(questions, facts)

    # 6. Comparison
    product_b = build_fictional_product_b(facts)
    comparison = compare_products(facts, product_b)

    # 7. Renderer -> write outputs
    write_outputs(product_page, faq, comparison, outdir)

    # return key artifacts for inspection/testing
    return {
        "product_page": product_page,
        "faq": faq,
        "comparison": comparison,
        "issues": issues
    }
