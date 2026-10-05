"""Starter for P01. Read README.md before implementing."""

from __future__ import annotations

def get_num(num):
    if not num.isnumeric() or int(num) < 0:
        return -1
    return int(num)

def parse_catalog(catalog: list[str]) -> dict[str, int]:
    catalog_dict = {}
    for item in catalog:
        item_parts = item.strip().split(',')
        if len(item_parts) != 2:
            continue
        item_sku = item_parts[0].strip()
        if len(item_sku) > 0 and item_sku not in catalog_dict:
            item_price = get_num(item_parts[1].strip())
            if item_price > 0:
                catalog_dict[item_sku] = item_price
    return catalog_dict

def parse_orders(orders: list[str]) -> dict[str, int]:
    order_dict = {}
    for item in orders:
        item_parts = item.strip().split(',')
        if len(item_parts) != 2:
            continue
        item_sku = item_parts[0].strip()
        if len(item_sku) == 0:
            continue
        item_quantity = get_num(item_parts[1].strip())
        if item_quantity > 0:
            order_dict[item_sku] = order_dict.get(item_sku, 0) + item_quantity
    return order_dict

def apply_discount(rules, catalog, orders, prices):
    if rules:
        for rule in rules:
            rule_parts = rule.strip().split(',')
            if len(rule_parts) >= 3:
                operation = rule_parts[0].strip()
                sku = rule_parts[1].strip()
                if sku in orders and sku in catalog:
                    if operation == 'BULK' and len(rule_parts) == 4:
                        min_q = get_num(rule_parts[2].strip())
                        price = get_num(rule_parts[3].strip())
                        num_ordered = orders[sku]
                        if min_q <= 0 or price <= 0:
                            continue
                        if min_q <= num_ordered:
                            prices[sku] = min(prices.get(sku, float('inf')), price * num_ordered)
                    elif operation == 'PERCENT' and len(rule_parts) == 3:
                        points_off = get_num(rule_parts[2].strip())
                        if 1 <= points_off <= 10000:
                            base_total = catalog[sku] * orders[sku]
                            discounted_total = (base_total * (10000 - points_off)) // 10000
                            prices[sku] = min(prices.get(sku, float('inf')), discounted_total)

def apply_tax(rules, subtotal):
    if rules:
        for rule in rules:
            parts = rule.strip().split(',')
            if len(parts) == 2 and parts[0].strip() == 'TAX':
                tax_points = get_num(parts[1].strip())
                if 0 <= tax_points <= 10000:
                    tax = subtotal * tax_points // 10000
                    return subtotal + tax
    return subtotal

def checkout_total(
    catalog: list[str], order: list[str], rules: list[str] | None = None
) -> int:
    catalog_dict = parse_catalog(catalog)
    order_dict = parse_orders(order)
    price_dict = {}
    for sku, quantity in order_dict.items():
        if sku in catalog_dict:
            price_dict[sku] = quantity * catalog_dict[sku]

    apply_discount(rules, catalog_dict, order_dict, price_dict)
    subtotal = 0    
    for price in price_dict.values():
        subtotal += price
    return apply_tax(rules, subtotal)
