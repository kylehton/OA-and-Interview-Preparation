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


def test_part_2_ignores_invalid_rows_atomically():
    catalog = ["bad", "x,nope", ",100", "x,200", "y,-1", "z,50,extra"]
    order = ["x,2", "x,0", "missing,9", "broken", "x,wat"]
    assert checkout_total(catalog, order) == 400


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

