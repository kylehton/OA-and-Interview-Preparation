from __future__ import annotations

from collections import defaultdict

from .models import CartLine, Product, Quote


class QuoteEngine:
    def __init__(self, products: list[Product]) -> None:
        self._products = {product.sku: product for product in products}
        self._cache: dict[tuple[str, ...], Quote] = {}

    def quote(
        self,
        cart: list[CartLine],
        *,
        tax_bps: int = 0,
        percentage_off: dict[str, int] | None = None,
        bulk_prices: dict[str, tuple[int, int]] | None = None,
    ) -> Quote:
        percentage_off = percentage_off or {}
        bulk_prices = bulk_prices or {}
        cache_key = tuple(sorted(line.sku for line in cart))
        if cache_key in self._cache:
            return self._cache[cache_key]

        quantities: dict[str, int] = defaultdict(int)
        for line in cart:
            if line.sku not in self._products or line.quantity <= 0:
                raise ValueError("invalid cart line")
            quantities[line.sku] += line.quantity

        subtotal = 0
        discounted_subtotal = 0
        for sku, quantity in quantities.items():
            unit_price = self._products[sku].unit_price
            base_total = unit_price * quantity
            candidates = [base_total]

            if sku in percentage_off:
                basis_points = percentage_off[sku]
                per_unit = unit_price * (10000 - basis_points) // 10000
                candidates.append(per_unit * quantity)

            if sku in bulk_prices:
                minimum, bulk_unit_price = bulk_prices[sku]
                if quantity >= minimum:
                    candidates.append(bulk_unit_price * quantity)

            subtotal += base_total
            discounted_subtotal += min(candidates)

        discount = subtotal - discounted_subtotal
        tax = subtotal * tax_bps // 10000
        result = Quote(subtotal, discount, tax, discounted_subtotal + tax)
        self._cache[cache_key] = result
        return result

