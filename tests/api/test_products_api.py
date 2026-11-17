import json
from pathlib import Path

import pytest

pytestmark = pytest.mark.api

KEYWORDS_PATH = Path(__file__).parents[2] / "data" / "search_keywords.json"
SEARCH_CASES = json.loads(KEYWORDS_PATH.read_text(encoding="utf-8"))


def test_products_first_page_has_pagination_and_product_fields(api):
    """Goal: check the product-list response contract.
    Precondition: the catalog contains products.
    Expected: the response contains pagination metadata and valid product entries."""
    response = api.get("/products", params={"page": 1})

    assert response.status == 200, response.text()
    body = response.json()
    for field in ("current_page", "data", "per_page", "total", "last_page"):
        assert field in body, f"Missing pagination field: {field}"
    assert isinstance(body["data"], list)
    assert 0 < len(body["data"]) <= body["per_page"]
    for product in body["data"]:
        assert {"id", "name", "price"} <= product.keys()
        assert isinstance(product["id"], (str, int))
        assert isinstance(product["name"], str) and product["name"].strip()
        assert isinstance(product["price"], (int, float)) and product["price"] > 0


@pytest.mark.parametrize("case", SEARCH_CASES, ids=[case["keyword"] for case in SEARCH_CASES])
def test_product_search_by_keyword_returns_only_matching_names(api, case):
    """Goal: verify the product search response by keyword.
    Precondition: each keyword in the JSON data matches at least one product.
    Expected: the response contains results and each name contains the expected term."""
    response = api.get("/products/search", params={"q": case["keyword"]})

    assert response.status == 200, response.text()
    names = [product["name"] for product in response.json()["data"]]
    assert names, f"No results for {case['keyword']}"
    assert all(case["must_contain"] in name.lower() for name in names), names


@pytest.mark.parametrize(
    ("path", "expected_status"),
    [
        pytest.param("/users/me", 401, id="unauthenticated-profile"),
        pytest.param("/products/does-not-exist", 404, id="missing-product"),
    ],
)
def test_resource_request_without_access_or_missing_returns_4xx(api, path, expected_status):
    """Goal: check the status codes for denied access and missing resources.
    Precondition: the request has no authorization and the test product ID is absent.
    Expected: the protected profile returns 401 and the missing product returns 404."""
    response = api.get(path)

    assert response.status == expected_status, response.text()
