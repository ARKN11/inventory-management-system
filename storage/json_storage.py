from pathlib import Path
import json
from typing import Any

ROOT_DIRECTORY = Path(__file__).resolve().parents[1]
PRODUCTS_FILE = ROOT_DIRECTORY / "data" / "products.json"


def load_products() -> dict[str, dict[str, Any]]:
    try:
        with PRODUCTS_FILE.open("r", encoding="utf-8") as file:
            products = json.load(file)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError as error:
        raise ValueError(f"Invalid JSON data in {PRODUCTS_FILE}") from error
    if not isinstance(products, dict):
        raise ValueError("The products database must contain a JSON object.")
    return products


def save_products(products: dict[str, dict[str, Any]]) -> None:

    if not isinstance(products, dict):
        raise ValueError("The products database must contain a dictionary.")
    PRODUCTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with PRODUCTS_FILE.open("w", encoding="utf-8") as file:
        json.dump(products, file, ensure_ascii=False, indent=4)
