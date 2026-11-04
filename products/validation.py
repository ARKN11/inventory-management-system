
from re import fullmatch
from decimal import Decimal, InvalidOperation


PRODUCT_ID_PATTERN = r"P\d{3}"


def validate_product_id(product_id: str) -> str:
    if not isinstance(product_id, str):
        raise ValueError("Product ID must be a string.")

    product_id = product_id.strip()

    if not product_id:
        raise ValueError("Product ID cannot be empty.")

    if not fullmatch(PRODUCT_ID_PATTERN, product_id):
        raise ValueError(
            "Product ID must start with P followed by exactly three digits."
        )

    return product_id


def validate_product_name(product_name: str) -> str:
    if not isinstance(product_name, str):
        raise ValueError("Product name must be a string.")

    product_name = product_name.strip()

    if not product_name:
        raise ValueError("Product name cannot be empty.")

    if not 2 <= len(product_name) <= 100:
        raise ValueError("Product name must be between 2 and 100 characters.")

    return product_name


def validate_price(price: int | float | Decimal | str) -> Decimal:
    if isinstance(price, bool) or not isinstance(
        price, (int, float, Decimal, str)
    ):
        raise ValueError("Price must be a numeric value.")

    try:
        price = Decimal(str(price).strip())
    except (InvalidOperation, ValueError) as error:
        raise ValueError("Price must be a valid number.") from error

    if not price.is_finite() or price <= 0:
        raise ValueError("Price must be a finite number greater than zero.")

    return price


def validate_product_quantity(quantity: int) -> int:
    if isinstance(quantity, bool) or not isinstance(quantity, int):
        raise ValueError("Quantity must be an integer.")

    if quantity < 0:
        raise ValueError("Quantity cannot be negative.")

    return quantity


def validate_product(product: dict) -> dict:
    if not isinstance(product, dict):
        raise ValueError("Product must be a dictionary.")

    required_fields = {"name", "price", "quantity"}

    missing_fields = required_fields - product.keys()
    unexpected_fields = product.keys() - required_fields

    if missing_fields:
        raise ValueError(f"Missing required fields: {missing_fields}")

    if unexpected_fields:
        raise ValueError(f"Unexpected fields: {unexpected_fields}")

    return {
        "name": validate_product_name(product["name"]),
        "price": validate_price(product["price"]),
        "quantity": validate_product_quantity(product["quantity"])
    }


def validate_product_entry(product_entry: dict) -> dict:
    if not isinstance(product_entry, dict):
        raise ValueError("Product entry must be a dictionary.")

    if len(product_entry) != 1:
        raise ValueError("Product entry must contain exactly one product.")

    product_id, product_data = next(iter(product_entry.items()))

    validated_id = validate_product_id(product_id)
    validated_product = validate_product(product_data)

    return {
        validated_id: validated_product
    }
