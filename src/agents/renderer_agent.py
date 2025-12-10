from typing import Dict, Any, List
from ..utils import write_json
import logging
from pathlib import Path

logger = logging.getLogger("RendererAgent")


def write_outputs(product_page: Dict[str, Any], faq: List[Dict[str, Any]], comparison: Dict[str, Any], outdir: str) -> None:
    outp = Path(outdir)
    outp.mkdir(parents=True, exist_ok=True)
    write_json(product_page, str(outp / "product_page.json"))
    write_json(faq, str(outp / "faq.json"))
    write_json(comparison, str(outp / "comparison_page.json"))
    logger.info("Wrote outputs to %s", outp)
