# src/agents/validator_agent.py
import logging
from src.state import PipelineState

logger = logging.getLogger("ValidatorAgent")


def validate_outputs(state: PipelineState) -> PipelineState:
    """
    LangGraph-compliant validation gate.
    Mutates and returns PipelineState.
    """

    errors = []

    if not state.product_page:
        errors.append("Missing product_page")

    if not state.faq or len(state.faq) < 15:
        errors.append("FAQ missing or < 15 items")

    if not state.comparison:
        errors.append("Missing comparison")

    if errors:
        state.is_valid = False
        state.error = "; ".join(errors)
        state.errors.extend(errors)
        logger.error("Validation failed: %s", state.error)
    else:
        state.is_valid = True
        logger.info("Validation passed")

    return state
