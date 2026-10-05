"""Starter for P01. Read README.md before implementing."""

from __future__ import annotations

def list_to_dict(li: list[str], combine: bool) -> dict[str, int]:
    # Assumes list is in the form of "val1,val2"
    li_dict = {}
    for item in li:
        pair = item.strip().split(',')
        if pair[0] not in li_dict:
            li_dict[pair[0]] = int(pair[1])
        elif combine:
            li_dict[pair[0]] += int(pair[1])
    return li_dict

def checkout_total(
    catalog: list[str], order: list[str], rules: list[str] | None = None
) -> int:
    catalog_dict = list_to_dict(catalog, False)
    order_dict = list_to_dict(order, True)
    total= 0
    for sku, val in catalog_dict.items():
        if sku in order_dict:
            total += (val * order_dict[sku])

    return total
