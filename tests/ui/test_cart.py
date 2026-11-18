import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage

pytestmark = pytest.mark.ui


def test_cart_with_two_items_shows_correct_line_price_and_total(page):
    """Goal: calculate the cart line price and total.
    Precondition: the cart is empty and Combination Pliers is available.
    Expected: the line price and cart total equal the unit price times two."""
    name = "Combination Pliers"
    quantity = 2
    product = HomePage(page).open().open_product(name)
    unit_price = product.price()
    product.add_to_cart(quantity=quantity)
    expect(product.cart_quantity).to_have_text(str(quantity))

    cart = product.go_to_cart()

    expect(cart.product_titles).to_have_text([name])
    expect(cart.quantities).to_have_value(str(quantity))
    expect(cart.line_prices).to_have_count(1)
    expected_total = unit_price * quantity
    assert cart.line_totals() == pytest.approx([expected_total])
    assert cart.total_value() == pytest.approx(expected_total)


def test_cart_continue_shopping_returns_to_catalog(page):
    """Goal: resume shopping from the cart.
    Precondition: the cart contains one Claw Hammer.
    Expected: Continue Shopping opens the catalog and displays products."""
    name = "Claw Hammer"
    product = HomePage(page).open().open_product(name).add_to_cart()
    expect(product.cart_quantity).to_have_text("1")
    cart = product.go_to_cart()
    expect(cart.product_titles).to_have_text([name])

    cart.continue_shopping.click()

    expect(HomePage(page).product_names.first).to_be_visible()
