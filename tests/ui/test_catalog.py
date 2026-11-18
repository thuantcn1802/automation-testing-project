import pytest
from playwright.sync_api import expect

from pages.cart_page import money
from pages.home_page import HomePage

pytestmark = pytest.mark.ui


def test_search_unknown_keyword_shows_no_results(page):
    """Goal: show the empty search state.
    Precondition: the search keyword matches no catalog product.
    Expected: the no-results message is visible and the grid has no products."""
    home = HomePage(page).open().search("zzz-no-such-tool")

    expect(home.no_results).to_have_text("There are no products found.")
    expect(home.product_names).to_have_count(0)


def test_sort_by_price_ascending_orders_products(page):
    """Goal: sort catalog products by price.
    Precondition: the catalog shows multiple products.
    Expected: displayed prices are in ascending order."""
    home = HomePage(page).open().sort_by("price,asc")

    expect(home.sorting_completed).to_be_visible()
    prices = home.prices()
    assert len(prices) > 1, prices
    assert prices == sorted(prices)


def test_filter_by_hammer_shows_only_hammer_products(page):
    """Goal: filter the catalog by category.
    Precondition: the Hammer category contains products.
    Expected: at least one product is shown and every name contains 'hammer'."""
    home = HomePage(page).open().filter_by_category("Hammer")

    expect(home.filter_completed).to_be_visible()
    names = home.product_names.all_inner_texts()
    assert names, "Hammer category returned no products"
    assert all("hammer" in name.lower() for name in names), names


def test_open_product_shows_name_and_price_from_catalog(page):
    """Goal: open the correct product details from the catalog.
    Precondition: the Combination Pliers card shows its price.
    Expected: the detail page shows the same name and price as the card."""
    name = "Combination Pliers"
    home = HomePage(page).open()
    listed_price = home.product_card_price(name)
    expect(listed_price).to_be_visible()
    price = money(listed_price.inner_text())

    product = home.open_product(name)

    expect(product.name).to_have_text(name)
    expect(product.unit_price).to_be_visible()
    assert product.price() == price
