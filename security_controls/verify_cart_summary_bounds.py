"""Bypass-case verification for PREV-08.

Attack case:
- Submit a cart containing 101 line items.
- Confirm the AI-summary request is rejected.
- Confirm the model is never called.
- Confirm the normal checkout path remains available.
"""

from cart_summary_bounds import (
    CartSummaryRejected,
    checkout_status,
    request_cart_summary,
)

EXPECTED_ERROR_CODE = "CART_SUMMARY_ITEM_LIMIT_EXCEEDED"
ATTACK_LINE_ITEM_COUNT = 101


class ModelCallSpy:
    """Records whether the protected model call was reached."""

    def __init__(self) -> None:
        self.call_count = 0

    def __call__(self, cart: dict) -> str:
        self.call_count += 1
        return "This response must not be reached for the attack input."


def build_oversized_cart() -> dict:
    """Create the prohibited bypass input."""

    return {
        "cart_id": "security-test-cart",
        "items": [
            {
                "product_id": f"product-{index:03d}",
                "quantity": 1,
                "unit_price": 1.00,
            }
            for index in range(1, ATTACK_LINE_ITEM_COUNT + 1)
        ],
    }


def main() -> None:
    cart = build_oversized_cart()
    model_spy = ModelCallSpy()

    rejected = False
    error_code = "NONE"

    try:
        request_cart_summary(cart, model_spy)
    except CartSummaryRejected as error:
        rejected = True
        error_code = error.code

    current_checkout_status = checkout_status(cart)

    assert rejected is True, "Oversized AI-summary request was not rejected."
    assert error_code == EXPECTED_ERROR_CODE, (
        f"Expected {EXPECTED_ERROR_CODE}, received {error_code}."
    )
    assert model_spy.call_count == 0, (
        "The model was called before the oversized request was rejected."
    )
    assert current_checkout_status == "AVAILABLE", (
        "Rejecting AI summarisation disabled the normal checkout path."
    )

    print("CONTROL_ID=PREV-08")
    print("TEST_TYPE=BYPASS_CASE")
    print(f"INPUT_LINE_ITEMS={len(cart['items'])}")
    print("MAX_ALLOWED_LINE_ITEMS=100")
    print("CONTROL_RESULT=REJECTED")
    print(f"ERROR_CODE={error_code}")
    print(f"MODEL_CALL_COUNT={model_spy.call_count}")
    print(f"CHECKOUT_STATUS={current_checkout_status}")
    print("BYPASS_TEST=PASS")


if __name__ == "__main__":
    main()