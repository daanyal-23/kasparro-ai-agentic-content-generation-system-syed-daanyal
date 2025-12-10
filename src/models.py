from __future__ import annotations
from dataclasses import dataclass, asdict, field
from typing import List, Dict, Any
from datetime import datetime
import uuid


def now_iso() -> str:
    return datetime.now().astimezone().isoformat()


@dataclass
class ProductModel:
    id: str
    name: str
    description: str
    price: float
    currency: str
    ingredients: List[str]
    benefits: List[str]
    how_to_use: str
    side_effects: str
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ProductModel":
        # non-destructive defaults and normalization
        pid = data.get("id") or data.get("product_id") or str(uuid.uuid4())
        name = data.get("name") or data.get("title") or ""
        description = data.get("description") or data.get("summary") or ""
        price = float(data.get("price", {}).get("amount") if isinstance(data.get("price"), dict) else data.get("price", 0) or 0)
        currency = (data.get("price", {}).get("currency") if isinstance(data.get("price"), dict) else data.get("currency")) or "INR"
        ingredients = data.get("ingredients") or data.get("key_ingredients") or []
        benefits = data.get("benefits") or []
        how_to_use = data.get("how_to_use") or data.get("usage") or ""
        side_effects = data.get("side_effects") or data.get("safety") or ""
        metadata = data.get("metadata") or {}
        metadata.setdefault("ingested_at", now_iso())
        return cls(
            id=str(pid),
            name=str(name),
            description=str(description),
            price=price,
            currency=str(currency),
            ingredients=[str(i) for i in ingredients],
            benefits=[str(b) for b in benefits],
            how_to_use=str(how_to_use),
            side_effects=str(side_effects),
            metadata=metadata,
        )

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["metadata"].setdefault("normalized_at", now_iso())
        return d
