from re import fullmatch
from decimal import Decimal

PRODUCT_ID_PATTERN = r"P\d{3}"


def validate_product_id(product_id: str) -> str:
    if not isinstance(product_id, str):
        raise ValueError("Product ID must be a string.")
    product_id = product_id.strip()
    if not product_id:
        raise ValueError("Product ID is empty.")
    pattern_validation = fullmatch(PRODUCT_ID_PATTERN, product_id)
    if pattern_validation:
        return product_id
    raise ValueError(
        "Product ID must consist of an uppercase P followed by exactly three digits."
    )


def validate_product_name(product_name: str) -> str:
    if not isinstance(product_name, str):
        raise ValueError("Product Name must be a string.")
    product_name = product_name.strip()
    if not product_name:
        raise ValueError("Product Name is empty.")
    if not 2 <= len(product_name) <= 100:
        raise ValueError("Product Name must be between 2-100 characters.")
    return product_name


def validate_product_price(price: int | float | Decimal) -> Decimal:
    if isinstance(price, bool) or not isinstance(price, (int, float, Decimal)):
        raise ValueError("Wrong type: Price must be an int, float, or Decimal.")
    if not isinstance(price, Decimal):
        price = Decimal(str(price))
    if price <= 0 or not price.is_finite():
        raise ValueError("Price must be a finite number greater than zero.")

    return price


def validate_product_quantity(quantity: int) -> int:
    if isinstance(quantity, bool) or not isinstance(quantity, int):
        raise ValueError("Quantity must be an integer.")
    if quantity < 0:
        raise ValueError("Quantity must be 0 or higher.")
    return quantity


def validate_product(product: dict) -> dict:
    if not isinstance(product, dict):
        raise ValueError("Product must be dictionary.")
    required_fields = {"id", "name", "price", "quantity"}
    missing_fiealds = required_fields - product.keys()
    unexpected_fields = product.keys() - required_fields
    if missing_fiealds:
        raise ValueError(f"You missed {missing_fiealds}")
    if unexpected_fields:
        raise ValueError(f"Unexpected fields founded: {unexpected_fields}")
    return {
        "id": validate_product_id(product["id"]),
        "name": validate_product_name(product["name"]),
        "price": validate_product_price(product["price"]),
        "quantity": validate_product_quantity(product["quantity"]),
    }
