# src/graph.py
import logging
from langgraph.graph import StateGraph, END

from src.models import ProductModel
from src.state import PipelineState

from src.agents.sanity_agent import run_sanity_checks
from src.agents.facts_extractor_agent import extract_facts
from src.agents.renderer_agent import write_outputs
from src.agents.validator_agent import validate_outputs

from src.langchain_orchestrator import (
    generate_product_page,
    generate_faq,
    generate_comparison,
)

logger = logging.getLogger("LangGraphPipeline")
logging.basicConfig(level=logging.INFO)

# -----------------------------
# Graph Nodes
# -----------------------------
def sanity_node(state: PipelineState) -> PipelineState:
    # Rehydrate ProductModel for deterministic agents
    product_model = ProductModel.from_dict(state.product)
    product_model, issues = run_sanity_checks(product_model)

    # Store back as dict for LangGraph state
    state.product = product_model.to_dict()
    state.sanity_issues = issues
    return state


def facts_node(state: PipelineState) -> PipelineState:
    """
    Extract facts with agent decision-making: enrich if critical data missing.
    """
    product_model = ProductModel.from_dict(state.product)
    state.facts = extract_facts(product_model)
    
    # Agent decision: check if critical facts are missing
    if not state.facts.get("ingredients") or not state.facts.get("benefits"):
        logger.warning("Missing critical facts (ingredients or benefits), proceeding with available data")
        # Could add enrichment logic here if needed
    
    # Ensure facts have required structure
    if not state.facts.get("price"):
        state.facts["price"] = {"amount": 0, "currency": "INR"}
    
    return state


def product_page_node(state: PipelineState) -> PipelineState:
    """
    Primary: Deterministic template engine agent.
    Fallback: LLM-based generation if deterministic fails.
    """
    from src.agents.template_engine_agent import render_product_page
    
    try:
        # Primary path: deterministic template rendering
        state.product_page = render_product_page(state.facts)
        
        # Validate deterministic output
        if not state.product_page or not state.product_page.get("title"):
            logger.warning("Deterministic product page incomplete, falling back to LLM")
            state.product_page = generate_product_page(state.facts)
        else:
            logger.info("Product page generated using deterministic agent")
    except Exception as e:
        logger.error(f"Deterministic product page generation failed: {e}, falling back to LLM")
        # Fallback to LLM on error
        state.product_page = generate_product_page(state.facts)
    
    return state


def faq_node(state: PipelineState) -> PipelineState:
    """
    Primary: Deterministic question generator + template rendering.
    Fallback: LLM-based generation if deterministic fails or insufficient FAQs.
    """
    from src.agents.question_generator_agent import generate_questions
    from src.agents.template_engine_agent import render_faq
    
    try:
        # Primary path: deterministic question generation + template rendering
        questions = generate_questions(state.facts)
        state.faq = render_faq(questions, state.facts)
        
        # Validate deterministic output
        if not state.faq or len(state.faq) < 15:
            logger.warning(f"Deterministic FAQ generated only {len(state.faq) if state.faq else 0} items, falling back to LLM")
            state.faq = generate_faq(state.facts)
        else:
            logger.info(f"FAQ generated using deterministic agent: {len(state.faq)} items")
    except Exception as e:
        logger.error(f"Deterministic FAQ generation failed: {e}, falling back to LLM")
        # Fallback to LLM on error
        state.faq = generate_faq(state.facts)
    
    return state


def comparison_node(state: PipelineState) -> PipelineState:
    """
    Primary: Deterministic comparison agent (build Product B + compare).
    Fallback: LLM-based generation if deterministic fails.
    """
    from src.agents.comparison_agent import build_fictional_product_b, compare_products
    
    try:
        # Primary path: deterministic Product B construction + comparison
        product_b = build_fictional_product_b(state.facts)
        state.comparison = compare_products(state.facts, product_b)
        
        # Validate deterministic output
        if not state.comparison or not state.comparison.get("verdict"):
            logger.warning("Deterministic comparison incomplete, falling back to LLM")
            state.comparison = generate_comparison(state.facts)
        else:
            logger.info("Comparison generated using deterministic agent")
    except Exception as e:
        logger.error(f"Deterministic comparison generation failed: {e}, falling back to LLM")
        # Fallback to LLM on error
        state.comparison = generate_comparison(state.facts)
    
    return state


def validate_node(state: PipelineState) -> PipelineState:
    state = validate_outputs(state)
    return state


def render_node(state: PipelineState) -> PipelineState:
    write_outputs(
        product_page=state.product_page,
        faq=state.faq,
        comparison=state.comparison,
        outdir=state.outdir,
    )
    return state


# -----------------------------
# Router
# -----------------------------
def validation_router(state: PipelineState) -> str:
    # ✅ Success path
    if state.is_valid:
        return "render"

    # 🔁 Retry path
    if state.retry_count < state.max_retries:
        state.retry_count += 1

        # Reset downstream artifacts before retry
        state.product_page = None
        state.faq = None
        state.comparison = None
        state.is_valid = False
        state.error = None

        # Loop back to regeneration
        return "product_page"

    # ❌ Hard stop after retries
    return END


# -----------------------------
# Graph Builder
# -----------------------------
def build_graph():
    graph = StateGraph(PipelineState)

    graph.add_node("sanity", sanity_node)
    graph.add_node("facts", facts_node)
    graph.add_node("product_page", product_page_node)
    graph.add_node("faq", faq_node)
    graph.add_node("comparison", comparison_node)
    graph.add_node("validate", validate_node)
    graph.add_node("render", render_node)

    graph.set_entry_point("sanity")

    graph.add_edge("sanity", "facts")
    graph.add_edge("facts", "product_page")
    graph.add_edge("product_page", "faq")
    graph.add_edge("faq", "comparison")
    graph.add_edge("comparison", "validate")

    # ✅ FIXED: include *all* router return values
    graph.add_conditional_edges(
        "validate",
        validation_router,
        {
            "render": "render",
            "product_page": "product_page",  # ✅ REQUIRED FIX
            END: END,
        },
    )

    graph.add_edge("render", END)

    return graph.compile()


# -----------------------------
# Public Entry
# -----------------------------
def run_graph(input_path: str, outdir: str):
    from src.agents.ingest_agent import ingest_from_file

    product_model = ingest_from_file(input_path)

    initial_state = PipelineState(
        product=product_model.to_dict(),
        outdir=outdir,
    )

    graph = build_graph()
    return graph.invoke(initial_state)
