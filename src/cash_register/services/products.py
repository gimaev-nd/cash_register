from weakref import ProxyTypes

import ruyaml
from django.conf import settings

from cash_register.types import Products

yaml = ruyaml.YAML()


def get_products() -> Products:
    products_file = (
        settings.BASE_DIR / "src" / "cash_register" / "data" / "products.yaml"
    )
    with products_file.open("r") as f:
        products = yaml.load(f)
    return Products(products)
