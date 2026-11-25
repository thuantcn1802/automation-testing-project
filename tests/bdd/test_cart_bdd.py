"""BDD steps for the shopping cart business flow."""

import pytest
from playwright.sync_api import expect
from pytest_bdd import given, parsers, scenarios, then, when

from pages.home_page import HomePage

pytestmark = [pytest.mark.bdd, pytest.mark.ui]

scenarios("cart.feature")


@given("I am on the home page", target_fixture="home")
def home(page):
    home = HomePage(page).open()
    expect(home.product_names.first).to_be_visible()
    return home


@when(
    parsers.parse('I open the product "{product}"'),
    target_fixture="product_page",
)
def open_product(home, product):
    product_page = home.open_product(product)
    expect(product_page.name).to_have_text(product)
    return product_page


@when(
    parsers.parse("I add it to the cart with quantity {quantity:d}"),
    target_fixture="unit_price",
)
def add_product_to_cart(product_page, quantity):
    expect(product_page.unit_price).to_be_visible()
    unit_price = product_page.price()
    product_page.add_to_cart(quantity=quantity)
    expect(product_page.cart_quantity).to_have_text(str(quantity))
    return unit_price


@when("I view my cart", target_fixture="cart")
def view_cart(product_page):
    return product_page.go_to_cart()


@then(parsers.parse('the cart contains "{product}" with quantity {quantity:d}'))
def cart_contains_product(cart, product, quantity):
    expect(cart.product_titles).to_have_text([product])
    expect(cart.quantities).to_have_value(str(quantity))


@then(
    parsers.parse("the line price equals the unit price multiplied by {quantity:d}")
)
def cart_line_price_is_correct(cart, unit_price, quantity):
    expect(cart.line_prices).to_have_count(1)
    assert cart.line_totals() == pytest.approx([unit_price * quantity])


@then("the cart total equals the sum of the line prices")
def cart_total_is_correct(cart):
    expect(cart.total).to_be_visible()
    assert cart.total_value() == pytest.approx(sum(cart.line_totals()))
