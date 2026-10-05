from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


def _load():
    spec = spec_from_file_location("p02_solution", Path(__file__).parents[1] / "solution.py")
    module = module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


process_commands = _load().process_commands


def test_part_1_create_credit_and_balance():
    commands = ["CREATE a", "CREDIT c1 a 250", "BALANCE a", "CREATE a"]
    assert process_commands(commands) == ["OK", "OK", "250", "ERROR"]


def test_part_1_malformed_and_duplicate_transactions():
    commands = ["CREATE a", "CREDIT c1 a 10", "CREDIT c1 a 99", "BALANCE a", "WHAT"]
    assert process_commands(commands) == ["OK", "OK", "ERROR", "10", "ERROR"]


def test_part_2_failed_id_can_be_retried():
    commands = [
        "CREATE a",
        "DEBIT d1 a 10",
        "CREDIT c1 a 20",
        "DEBIT d1 a 10",
        "BALANCE a",
    ]
    assert process_commands(commands) == ["OK", "ERROR", "OK", "OK", "10"]


def test_part_3_credit_and_debit_reversals():
    commands = [
        "CREATE a",
        "CREDIT c1 a 100",
        "DEBIT d1 a 30",
        "REVERSE r1 d1",
        "REVERSE r2 d1",
        "REVERSE r3 c1",
        "BALANCE a",
    ]
    assert process_commands(commands) == ["OK", "OK", "OK", "OK", "ERROR", "OK", "0"]


def test_part_3_failed_reversal_is_atomic_and_retryable():
    commands = [
        "CREATE a",
        "CREDIT c1 a 50",
        "DEBIT d1 a 50",
        "REVERSE r1 c1",  # cannot remove 50 yet
        "REVERSE r2 d1",
        "REVERSE r1 c1",  # r1 was not reserved by its failed attempt
    ]
    assert process_commands(commands) == ["OK", "OK", "OK", "ERROR", "OK", "OK"]


def test_part_4_transfer_and_reversal():
    commands = [
        "CREATE alice",
        "CREATE bob",
        "CREDIT c1 alice 500",
        "TRANSFER t1 alice bob 125",
        "BALANCE alice",
        "REVERSE r1 t1",
        "BALANCE bob",
    ]
    assert process_commands(commands) == ["OK", "OK", "OK", "OK", "375", "OK", "0"]


def test_part_4_transfer_reversal_requires_destination_funds():
    commands = [
        "CREATE a",
        "CREATE b",
        "CREDIT c1 a 100",
        "TRANSFER t1 a b 80",
        "DEBIT d1 b 80",
        "REVERSE r1 t1",
        "BALANCE a",
    ]
    assert process_commands(commands) == ["OK", "OK", "OK", "OK", "OK", "ERROR", "20"]

