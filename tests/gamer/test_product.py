from cash_register.services.repositories.products import all_products


def test_load_products():
    assert all_products.count == 108


def test_get_randon_products():
    assert len(all_products.get_random(10)) == 10
    assert set(all_products.get_random()[0].model_dump()) == {"id", "name", "price"}
