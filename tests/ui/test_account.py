import pytest
from playwright.sync_api import expect

from pages.account_page import AccountPage
from pages.login_page import LoginPage

pytestmark = pytest.mark.ui


def test_login_empty_form_shows_required_errors(page):
    """Goal: validate the required sign-in fields.
    Precondition: both login fields are blank.
    Expected: the email and password fields show required-field errors."""
    login = LoginPage(page).open()
    login.submit_button.click()

    expect(login.email_error).to_have_text("Email is required")
    expect(login.password_error).to_have_text("Password is required")


def test_account_with_saved_login_shows_user_menu(logged_in_page):
    """Goal: open the account page using the saved login state.
    Precondition: the logged_in_page fixture signed in a dedicated test user.
    Expected: My account opens and the user menu shows the test user's name."""
    account = AccountPage(logged_in_page).open()

    expect(account.title).to_have_text("My account")
    expect(account.nav_menu).to_contain_text("QA Bot")
