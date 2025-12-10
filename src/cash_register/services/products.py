import ruyaml
from django.conf import settings

from cash_register.types import Product, Products

yaml = ruyaml.YAML()


def get_products() -> Products:
    products_file = settings.BASE_DIR / "cash_register" / "data" / "products.yaml"
    with products_file.open("r") as f:
        product_list = yaml.load(f)
        products = [Product.model_validate(p) for p in product_list]
    return Products(products)


all_products = get_products()
