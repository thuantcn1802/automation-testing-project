import pytest

pytestmark = pytest.mark.api


@pytest.fixture
def new_cart(api):
    response = api.post("/carts")
    assert response.status == 201, response.text()
    return response.json()["id"]


def test_cart_add_product_quantity_two_is_stored(api, new_cart):
    """Goal: verify that adding an item persists its quantity.
    Precondition: the fixture creates an empty cart and the catalog contains products.
    Expected: the retrieved cart has one line with the selected product and quantity two."""
    products = api.get("/products", params={"page": 1})
    assert products.status == 200, products.text()
    catalog = products.json()["data"]
    assert catalog, "The catalog has no product to add"
    product_id = catalog[0]["id"]

    cart_path = f"/carts/{new_cart}"
    added = api.post(cart_path, data={"product_id": product_id, "quantity": 2})
    assert added.ok, added.text()

    cart = api.get(cart_path)
    assert cart.status == 200, cart.text()
    items = cart.json()["cart_items"]
    assert len(items) == 1
    assert str(items[0]["product_id"]) == str(product_id)
    assert items[0]["quantity"] == 2
