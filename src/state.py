# src/state.py
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field


class PipelineState(BaseModel):
    # --------------------
    # Core input
    # --------------------
    product: Dict[str, Any]

    # --------------------
    # Derived artifacts
    # --------------------
    facts: Optional[Dict[str, Any]] = None
    product_page: Optional[Dict[str, Any]] = None
    faq: Optional[List[Dict[str, Any]]] = None
    comparison: Optional[Dict[str, Any]] = None

    # --------------------
    # Validation & control
    # --------------------
    sanity_issues: List[str] = Field(default_factory=list)
    is_valid: bool = False
    error: Optional[str] = None
    errors: List[str] = Field(default_factory=list)

    # 🔁 Retry control (KEY FIX)
    retry_count: int = 0
    max_retries: int = 2

    # --------------------
    # IO
    # --------------------
    outdir: Optional[str] = None
