import re

import pytest
from playwright.sync_api import expect

from pages.contact_page import ContactPage
from pages.home_page import HomePage
from pages.login_page import LoginPage


@pytest.mark.smoke
def test_search_returns_matching_pliers(page):
    """Goal: search filters the product grid.
    Precondition: the catalog contains pliers.
    Expected: at least one result, and every name contains 'pliers'."""
    home = HomePage(page).open().search("pliers")
    expect(home.search_completed).to_be_visible()
    names = home.product_names.all_inner_texts()
    assert names, "search returned no products"
    assert all("pliers" in name.lower() for name in names), names


@pytest.mark.smoke
def test_add_three_claw_hammers_updates_cart_badge(page):
    """Goal: adding a product uses the selected quantity.
    Precondition: the cart is empty and Claw Hammer is available.
    Expected: the cart badge shows 3."""
    product = HomePage(page).open().open_product("Claw Hammer").add_to_cart(quantity=3)
    expect(product.cart_quantity).to_have_text("3")


@pytest.mark.smoke
def test_invalid_login_shows_error_and_stays_on_login(page):
    """Goal: reject invalid credentials.
    Precondition: the email address has no account.
    Expected: an invalid credentials error and the login URL stays active."""
    login = LoginPage(page).open().login("nobody-here@example.com", "Wrong-Password-123")
    expect(login.error).to_contain_text("Invalid email or password")
    expect(page).to_have_url(re.compile(r"/auth/login$"))


@pytest.mark.smoke
def test_empty_contact_form_shows_required_errors(page):
    """Goal: validate required fields on the contact form.
    Precondition: the form has no input.
    Expected: the subject and message required errors appear."""
    contact = ContactPage(page).open().submit()
    expect(contact.errors).to_contain_text(["Subject is required", "Message is required"])
