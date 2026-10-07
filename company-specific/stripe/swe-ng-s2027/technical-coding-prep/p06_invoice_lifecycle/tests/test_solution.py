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
        "PAY inv p3 1",
    ]
    assert process_invoices(commands) == [
        "OK", "ERROR", "OK", "OK", "OK", "OK", "ERROR"
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


def test_part_1_line_ids_are_scoped_to_their_invoice():
    commands = [
        "CREATE inv1 c1 USD", "CREATE inv2 c2 USD",
        "ADD inv1 shared 10", "ADD inv2 shared 20",
        "TOTAL inv1", "TOTAL inv2",
    ]
    assert process_invoices(commands) == ["OK", "OK", "OK", "OK", "10", "20"]


def test_part_1_invalid_create_and_add_do_not_reserve_identifiers():
    commands = [
        "CREATE inv c US", "CREATE inv c USD", "CREATE inv other EUR",
        "ADD inv line 0", "ADD inv line 10", "TOTAL inv",
    ]
    assert process_invoices(commands) == ["ERROR", "OK", "ERROR", "ERROR", "OK", "10"]


def test_part_2_finalized_invoice_rejects_new_lines():
    commands = [
        "CREATE inv c USD", "ADD inv first 10", "FINALIZE inv",
        "ADD inv second 20", "TOTAL inv",
    ]
    assert process_invoices(commands) == [
        "OK", "OK", "OK", "ERROR", "10"
    ]


def test_part_1_exact_arity_and_ascii_currency_are_required():
    commands = [
        "CREATE too many USD EXTRA",
        "CREATE inv customer ÉUR",
        "CREATE inv customer USD",
        "ADD inv line 10 EXTRA",
        "ADD inv line 10",
        "TOTAL inv EXTRA",
        "TOTAL inv",
    ]
    assert process_invoices(commands) == [
        "ERROR", "ERROR", "OK", "ERROR", "OK", "ERROR", "10"
    ]


def test_part_3_status_reports_each_state():
    commands = [
        "CREATE draft c USD", "STATUS draft", "ADD draft x 10",
        "FINALIZE draft", "STATUS draft", "PAY draft p 10", "STATUS draft",
    ]
    assert process_invoices(commands) == [
        "OK", "DRAFT,0,0", "OK", "OK", "OPEN,10,0", "OK", "PAID,10,10"
    ]


def test_part_4_full_refund_does_not_erase_payment_history_for_voiding():
    commands = [
        "CREATE inv c USD", "ADD inv x 10", "FINALIZE inv", "PAY inv p 10",
        "REFUND inv r 10", "VOID inv", "STATUS inv",
    ]
    assert process_invoices(commands) == [
        "OK", "OK", "OK", "OK", "OK", "ERROR", "OPEN,10,0"
    ]


def test_part_2_payment_ids_are_global_across_invoices():
    commands = [
        "CREATE a c USD", "ADD a x 10", "FINALIZE a",
        "CREATE b c USD", "ADD b x 10", "FINALIZE b",
        "PAY a shared 10", "PAY b shared 10", "STATUS a", "STATUS b",
    ]
    assert process_invoices(commands) == [
        "OK", "OK", "OK", "OK", "OK", "OK", "OK", "ERROR",
        "PAID,10,10", "OPEN,10,0",
    ]


def test_part_3_void_rejects_partially_and_fully_paid_invoices():
    commands = [
        "CREATE inv c USD", "ADD inv x 10", "FINALIZE inv",
        "PAY inv p1 5", "VOID inv", "STATUS inv",
        "PAY inv p2 5", "VOID inv", "STATUS inv",
    ]
    assert process_invoices(commands) == [
        "OK", "OK", "OK", "OK", "ERROR", "OPEN,10,5",
        "OK", "ERROR", "PAID,10,10",
    ]


def test_part_4_failed_refund_id_is_reusable_and_ids_share_namespace():
    commands = [
        "CREATE inv c USD", "ADD inv x 10", "FINALIZE inv", "PAY inv pay 10",
        "REFUND inv pay 1", "REFUND inv refund 11", "REFUND inv refund 10",
        "STATUS inv", "PAY inv refund 1",
    ]
    assert process_invoices(commands) == [
        "OK", "OK", "OK", "OK", "ERROR", "ERROR", "OK",
        "OPEN,10,0", "ERROR",
    ]
