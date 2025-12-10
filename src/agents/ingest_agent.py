from typing import Dict, Any
from ..models import ProductModel
from ..utils import read_json
import logging


logger = logging.getLogger("IngestAgent")


def ingest_from_file(path: str) -> ProductModel:
    """
    Read input JSON and convert to ProductModel. No external facts are introduced.
    """
    logger.info("Ingesting file: %s", path)
    data = read_json(path)
    # if input is top-level dict with product key, allow that
    if isinstance(data, dict) and "product" in data and isinstance(data["product"], dict):
        data = data["product"]
    pm = ProductModel.from_dict(data)
    logger.info("Ingested product: %s (id=%s)", pm.name, pm.id)
    return pm
