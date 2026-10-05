from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


def _load():
    spec = spec_from_file_location("p01_solution", Path(__file__).parents[1] / "solution.py")
    module = module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


checkout_total = _load().checkout_total


def test_part_1_basic_total_and_combined_quantities():
    catalog = ["notebook,500", "pen,125"]
    order = ["notebook,2", "pen,4", "pen,2"]
    assert checkout_total(catalog, order) == 1750


def test_part_1_first_valid_catalog_row_wins():
    assert checkout_total(["x,100", "x,1"], ["x,3"]) == 300


def test_part_2_rejects_alphanumeric_price():
    assert checkout_total(["z,10a"], ["z,1"]) == 0


def test_part_2_rejects_empty_sku():
    assert checkout_total([",100"], [",2"]) == 0


def test_part_2_invalid_catalog_row_does_not_block_later_valid_duplicate():
    assert checkout_total(["x,0", "x,100"], ["x,1"]) == 100


def test_part_2_trims_each_comma_separated_field():
    assert checkout_total([" x , 100 "], ["x,2"]) == 200


def test_part_2_ignores_invalid_order_rows_without_affecting_valid_quantity():
    order = ["x,0", "x,-1", "x,wat", "missing,9", "broken", "x,2"]
    assert checkout_total(["x,100"], order) == 200


def test_part_3_uses_lowest_applicable_discount_without_stacking():
    catalog = ["a,100", "b,250"]
    order = ["a,5", "b,2"]
    rules = [
        "BULK,a,5,80",       # 400, best for a
        "PERCENT,a,1000",    # 450
        "BULK,b,3,1",        # does not apply
        "PERCENT,b,2000",    # 400
    ]
    assert checkout_total(catalog, order, rules) == 800


def test_part_3_percentage_uses_integer_flooring():
    assert checkout_total(["x,101"], ["x,1"], ["PERCENT,x,3333"]) == 67


def test_part_3_invalid_rules_do_not_block_a_later_valid_discount():
    rules = [
        "PERCENT,x,10001",
        "PERCENT,x,0",
        "BULK,x,0,1",
        "BULK,x,2,0",
        "PERCENT,missing,5000",
        "broken",
        "PERCENT,x,5000",
    ]
    assert checkout_total(["x,100"], ["x,2"], rules) == 100


def test_part_3_allows_one_hundred_percent_discount():
    assert checkout_total(["x,100"], ["x,2"], ["PERCENT,x,10000"]) == 0


def test_part_3_trims_every_rule_field():
    assert checkout_total(["x,100"], ["x,2"], [" PERCENT , x , 5000 "]) == 100


def test_part_4_taxes_discounted_subtotal_and_first_valid_tax_wins():
    catalog = ["notebook,500", "pen,125"]
    order = ["notebook,2", "pen,6"]
    rules = [
        "TAX,not-an-int",
        "BULK,pen,5,100",
        "PERCENT,notebook,1000",
        "TAX,825",
        "TAX,10000",
    ]
    assert checkout_total(catalog, order, rules) == 1623


def test_part_4_zero_tax_is_valid_and_blocks_later_tax_rules():
    rules = ["TAX,10001", "TAX,-1", "TAX,0", "TAX,1000"]
    assert checkout_total(["x,100"], ["x,1"], rules) == 100


def test_part_4_tax_is_rounded_once_on_complete_discounted_subtotal():
    catalog = ["a,1", "b,1"]
    order = ["a,1", "b,1"]
    assert checkout_total(catalog, order, ["TAX,5000"]) == 3


def test_part_4_tax_requires_exact_arity_and_trims_fields():
    rules = ["TAX,500,extra", " TAX , 1000 "]
    assert checkout_total(["x,100"], ["x,1"], rules) == 110
