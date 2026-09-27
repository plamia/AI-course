"""PREV-08: bounded AI cart-summary requests.

This module rejects oversized AI-summary requests before a model is called.
The normal cart and checkout path remains independent of AI summarisation.
"""

from collections.abc import Callable
from typing import Any

MAX_CART_LINE_ITEMS = 100


class CartSummaryRejected(ValueError):
    """Raised when an AI-summary request violates a security bound."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code


def validate_summary_request(cart: dict[str, Any]) -> None:
    """Validate only the optional AI-summary request."""

    items = cart.get("items")

    if not isinstance(items, list):
        raise CartSummaryRejected(
            code="INVALID_CART_ITEMS",
            message="Cart items must be supplied as a list.",
        )

    if len(items) > MAX_CART_LINE_ITEMS:
        raise CartSummaryRejected(
            code="CART_SUMMARY_ITEM_LIMIT_EXCEEDED",
            message=(
                f"AI cart summary supports at most "
                f"{MAX_CART_LINE_ITEMS} line items."
            ),
        )


def request_cart_summary(
    cart: dict[str, Any],
    model_call: Callable[[dict[str, Any]], str],
) -> str:
    """Validate the request before invoking the model."""

    validate_summary_request(cart)
    return model_call(cart)


def checkout_status(cart: dict[str, Any]) -> str:
    """Represent the non-AI cart and checkout path.

    The AI-summary item limit must not disable this core path.
    """

    if not isinstance(cart.get("items"), list):
        return "INVALID_CART"

    return "AVAILABLE"