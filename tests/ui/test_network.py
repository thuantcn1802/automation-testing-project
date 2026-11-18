import re

import pytest
from playwright.sync_api import expect

from pages.home_page import PRODUCT_LIST, HomePage

pytestmark = pytest.mark.ui

IMAGE_URL = re.compile(r"\.(png|jpe?g|webp|avif|svg)(\?.*)?$", re.IGNORECASE)
EMPTY_PAGE = {
    "current_page": 1,
    "data": [],
    "from": None,
    "last_page": 1,
    "per_page": 9,
    "to": None,
    "total": 0,
}


def test_home_with_image_requests_blocked_still_lists_products(page):
    """Goal: keep the product grid usable when images cannot load.
    Precondition: a browser route aborts image requests.
    Expected: an intercepted image request fails and product names remain visible."""
    blocked = set()

    def block_image(route):
        blocked.add(route.request.url)
        route.abort()

    page.route(IMAGE_URL, block_image)
    with page.expect_event("requestfailed", predicate=lambda request: request.url in blocked):
        home = HomePage(page).open()

    expect(home.product_names.first).to_be_visible()


def test_home_with_empty_product_response_shows_no_results(page):
    """Goal: verify the catalog's empty state through a browser route.
    Precondition: the product-list response is mocked with an empty page.
    Expected: the no-results message appears and the grid contains no product cards."""
    page.route(PRODUCT_LIST, lambda route: route.fulfill(status=200, json=EMPTY_PAGE))
    home = HomePage(page).open()

    expect(home.no_results).to_have_text("There are no products found.")
    expect(home.product_names).to_have_count(0)
