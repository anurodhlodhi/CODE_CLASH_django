"""Public shop checks that pass before deliberate business defects are repaired."""

import pytest


pytestmark = pytest.mark.django_db


def test_catalogue_and_login_are_reachable(client, product):
    catalogue = client.get("/shop/")
    assert catalogue.status_code == 200
    assert product.name in catalogue.content.decode()
    assert client.get("/shop/login/").status_code == 200


def test_customer_pages_require_sign_in(client):
    for path in ("/shop/cart/", "/shop/orders/"):
        response = client.get(path)
        assert response.status_code == 302
        assert "/shop/login/" in response["Location"]


def test_admin_user_does_not_get_customer_cart(client, staff_user):
    client.force_login(staff_user)
    response = client.get("/shop/cart/")
    assert response.status_code == 302
    assert "/shop/login/" in response["Location"]

