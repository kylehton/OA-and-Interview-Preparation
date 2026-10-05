from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


def _load():
    spec = spec_from_file_location("p06_solution", Path(__file__).parents[1] / "solution.py")
    module = module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


process_invoices = _load().process_invoices


def test_part_1_draft_lines_and_totals():
    commands = [
        "CREATE inv cus USD",
        "ADD inv a 100",
        "ADD inv b 250",
        "TOTAL inv",
        "ADD inv a 999",
    ]
    assert process_invoices(commands) == ["OK", "OK", "OK", "350", "ERROR"]


def test_part_1_invalid_commands_are_atomic():
    commands = ["CREATE inv cus usd", "CREATE inv cus USD", "ADD inv x -1", "TOTAL inv"]
    assert process_invoices(commands) == ["ERROR", "OK", "ERROR", "0"]


def test_part_2_finalize_and_partial_payments():
    commands = [
        "CREATE inv cus USD",
        "FINALIZE inv",
        "ADD inv x 100",
        "FINALIZE inv",
        "PAY inv p1 40",
        "PAY inv p2 60",
        "STATUS inv",
    ]
    assert process_invoices(commands) == [
        "OK", "ERROR", "OK", "OK", "OK", "OK", "PAID,100,100"
    ]


def test_part_2_failed_payment_id_can_be_retried():
    commands = [
        "CREATE a c USD", "ADD a x 50", "FINALIZE a",
        "PAY a p 60", "PAY a p 50",
    ]
    assert process_invoices(commands) == ["OK", "OK", "OK", "ERROR", "OK"]


def test_part_3_void_rules():
    commands = [
        "CREATE draft c USD", "VOID draft", "STATUS draft",
        "CREATE open c USD", "ADD open x 20", "FINALIZE open", "VOID open",
        "STATUS open",
    ]
    assert process_invoices(commands) == [
        "OK", "OK", "VOID,0,0", "OK", "OK", "OK", "OK", "VOID,20,0"
    ]


def test_part_4_refund_reopens_paid_invoice_and_ids_are_global():
    commands = [
        "CREATE inv cus USD", "ADD inv x 500", "FINALIZE inv",
        "PAY inv pay1 500", "REFUND inv ref1 125", "STATUS inv",
        "PAY inv ref1 125",  # refund ID already occupies the namespace
        "PAY inv pay2 125", "STATUS inv",
    ]
    assert process_invoices(commands) == [
        "OK", "OK", "OK", "OK", "OK", "OPEN,500,375",
        "ERROR", "OK", "PAID,500,500",
    ]


def test_part_4_over_refund_does_not_mutate():
    commands = [
        "CREATE i c USD", "ADD i x 10", "FINALIZE i", "PAY i p 5",
        "REFUND i r 6", "STATUS i",
    ]
    assert process_invoices(commands)[-2:] == ["ERROR", "OPEN,10,5"]

