from dataclasses import dataclass
from functools import cached_property
from pathlib import Path
from random import randint, shuffle

import ruyaml
from django.conf import settings

from cash_register.types import Product

yaml = ruyaml.YAML()


@dataclass
class Products:
    products: list[Product]

    def get(self, id: int) -> Product:
        return self.map[id]

    def get_random(self, count: int | None = None) -> list[Product]:
        _count: int = count or randint(1, 8)
        product_ids: set[int] = set()
        products: list[Product] = []
        while len(product_ids) < _count:
            product_index = randint(0, self.count - 1)
            if product_index in product_ids:
                continue
            product_ids.add(product_index)
            products.append(self.products[product_index])
        shuffle(products)
        return products

    @cached_property
    def count(self):
        return len(self.products)

    @cached_property
    def map(self) -> dict[int, Product]:
        return {p.id: p for p in self.products}

    @classmethod
    def load(cls, products_file: Path | str) -> "Products":
        if isinstance(products_file, str):
            products_file = Path(products_file)
        with products_file.open("r") as f:
            product_list: list[Product] = yaml.load(f)  # type: ignore
            products = [Product.model_validate(p) for p in product_list]
        return Products(products)


all_products = Products.load(settings.CASH_REGISTER_DATA_DIR / "products.yaml")
