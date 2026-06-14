"""
validators.py
~~~~~~~~~~~~~
All input-validation logic lives here so the CLI and order layer stay clean.
"""

from __future__ import annotations

VALID_SIDES = {"BUY", "SELL"}
VALID_ORDER_TYPES = {"MARKET", "LIMIT", "STOP_MARKET"}


class ValidationError(ValueError):
    """Raised when user-supplied input fails validation."""


def validate_symbol(symbol: str) -> str:
    s = symbol.strip().upper()
    if not s:
        raise ValidationError("Symbol cannot be empty.")
    if len(s) < 3:
        raise ValidationError(f"Symbol '{s}' looks too short. Example: BTCUSDT")
    return s


def validate_side(side: str) -> str:
    s = side.strip().upper()
    if s not in VALID_SIDES:
        raise ValidationError(
            f"Invalid side '{s}'. Must be one of: {', '.join(sorted(VALID_SIDES))}"
        )
    return s


def validate_order_type(order_type: str) -> str:
    t = order_type.strip().upper()
    if t not in VALID_ORDER_TYPES:
        raise ValidationError(
            f"Invalid order type '{t}'. Must be one of: {', '.join(sorted(VALID_ORDER_TYPES))}"
        )
    return t


def validate_quantity(quantity: str | float) -> float:
    try:
        q = float(quantity)
    except (TypeError, ValueError):
        raise ValidationError(f"Quantity '{quantity}' is not a valid number.")
    if q <= 0:
        raise ValidationError(f"Quantity must be greater than 0. Got: {q}")
    return q


def validate_price(price: str | float | None, order_type: str) -> float | None:
    if order_type in ("MARKET", "STOP_MARKET"):
        return None

    # For LIMIT a price is required
    if price is None:
        raise ValidationError(f"Price is required for '{order_type}' orders.")
    try:
        p = float(price)
    except (TypeError, ValueError):
        raise ValidationError(f"Price '{price}' is not a valid number.")
    if p <= 0:
        raise ValidationError(f"Price must be greater than 0. Got: {p}")
    return p


def validate_stop_price(stop_price: str | float | None, order_type: str) -> float | None:
    """Stop price is required for STOP_MARKET orders."""
    order_type = order_type.strip().upper()
    if order_type != "STOP_MARKET":
        return None
    if stop_price is None:
        raise ValidationError("Stop price (--stop-price) is required for STOP_MARKET orders.")
    try:
        sp = float(stop_price)
    except (TypeError, ValueError):
        raise ValidationError(f"Stop price '{stop_price}' is not a valid number.")
    if sp <= 0:
        raise ValidationError(f"Stop price must be greater than 0. Got: {sp}")
    return sp


def validate_all(
    *,
    symbol: str,
    side: str,
    order_type: str,
    quantity: str | float,
    price: str | float | None = None,
    stop_price: str | float | None = None,
) -> dict:
    """
    Run all validations and return a clean params dict ready for the order layer.
    Raises ValidationError on the first failure found.
    """
    clean_symbol = validate_symbol(symbol)
    clean_side = validate_side(side)
    clean_type = validate_order_type(order_type)
    clean_qty = validate_quantity(quantity)
    clean_price = validate_price(price, clean_type)
    clean_stop = validate_stop_price(stop_price, clean_type)

    return {
        "symbol": clean_symbol,
        "side": clean_side,
        "order_type": clean_type,
        "quantity": clean_qty,
        "price": clean_price,
        "stop_price": clean_stop,
    }
