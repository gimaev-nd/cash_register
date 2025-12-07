from cash_register.services.products import get_products


def test_load_products():
    products = get_products()

    assert products.count == 108


def test_get_randon_products():
    products = get_products()

    assert len(products.get_random(10)) == 10
    assert set(products.get_random()[0].keys()) == set(["id", "name", "price"])
