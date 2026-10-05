from dataclasses import dataclass


@dataclass(frozen=True)
class Product:
    sku: str
    unit_price: int


@dataclass(frozen=True)
class CartLine:
    sku: str
    quantity: int


@dataclass(frozen=True)
class Quote:
    subtotal: int
    discount: int
    tax: int
    total: int

