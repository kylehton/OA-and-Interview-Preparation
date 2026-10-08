from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


def _load():
    spec = spec_from_file_location("p10_solution", Path(__file__).parents[1] / "solution.py")
    module = module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


process_ledger = _load().process_ledger


def test_part_1_open_deposit_balance_and_idempotency():
    commands = [
        "OPEN a USD", "DEPOSIT d1 a USD 100", "DEPOSIT d1 a USD 900",
        "BALANCE a USD", "BALANCE a EUR",
    ]
    assert process_ledger(commands) == ["OK", "OK", "ERROR", "100", "0"]


def test_part_1_failed_transaction_id_is_retryable():
    commands = ["DEPOSIT d missing USD 10", "OPEN a USD", "DEPOSIT d a USD 10"]
    assert process_ledger(commands) == ["ERROR", "OK", "OK"]


def test_part_2_direct_conversion_and_floor_rounding():
    commands = [
        "OPEN a USD", "DEPOSIT d a USD 1000", "RATE 1 USD EUR 9 10",
        "CONVERT c 1 a USD EUR 333", "BALANCE a USD", "BALANCE a EUR",
    ]
    assert process_ledger(commands) == ["OK", "OK", "OK", "OK", "667", "299"]


def test_part_3_historical_and_inverse_lookup():
    commands = [
        "OPEN a EUR", "DEPOSIT d a EUR 190",
        "RATE 10 USD EUR 3 4", "RATE 1 USD EUR 1 2",
        "CONVERT old 5 a EUR USD 50",   # inverse of 1/2 => 100
        "CONVERT new 10 a EUR USD 90",  # inverse of 3/4 => 120
        "BALANCE a USD",
    ]
    assert process_ledger(commands) == ["OK", "OK", "OK", "OK", "OK", "OK", "220"]


def test_part_3_zero_output_conversion_is_atomic():
    commands = [
        "OPEN a USD", "DEPOSIT d a USD 1", "RATE 1 USD JPY 1 100",
        "CONVERT c 1 a USD JPY 1", "BALANCE a USD",
    ]
    assert process_ledger(commands) == ["OK", "OK", "OK", "ERROR", "1"]


def test_part_4_cross_account_transfer():
    commands = [
        "OPEN a USD", "OPEN b EUR", "DEPOSIT d1 a USD 100",
        "RATE 1 USD EUR 9 10", "TRANSFER t1 1 a b 100",
        "BALANCE a USD", "BALANCE b EUR",
    ]
    assert process_ledger(commands) == ["OK", "OK", "OK", "OK", "OK", "0", "90"]


def test_part_4_same_currency_transfer_needs_no_rate_and_is_atomic():
    commands = [
        "OPEN a USD", "OPEN b USD", "DEPOSIT d a USD 50",
        "TRANSFER bad 0 a b 60", "TRANSFER bad 0 a b 50",
        "BALANCE b USD",
    ]
    assert process_ledger(commands) == ["OK", "OK", "OK", "ERROR", "OK", "50"]


def test_part_1_open_and_deposit_validation_is_atomic():
    commands = [
        "OPEN a US", "OPEN a USD", "OPEN a EUR",
        "DEPOSIT d a USD 0", "DEPOSIT d a USD 10", "BALANCE a USD",
    ]
    assert process_ledger(commands) == ["ERROR", "OK", "ERROR", "ERROR", "OK", "10"]


def test_part_1_exact_arity_and_ascii_currency_are_required():
    commands = [
        "OPEN a USD extra", "OPEN a ÉUR", "OPEN a USD",
        "DEPOSIT same a USD 10 extra", "DEPOSIT same a USD 10",
        "BALANCE a USD extra", "BALANCE a USD",
    ]
    assert process_ledger(commands) == [
        "ERROR", "ERROR", "OK", "ERROR", "OK", "ERROR", "10"
    ]


def test_part_4_transaction_ids_are_global_across_command_types():
    commands = [
        "OPEN a USD", "OPEN b EUR", "DEPOSIT shared a USD 20",
        "RATE 1 USD EUR 1 1", "CONVERT shared 1 a USD EUR 5",
        "TRANSFER shared 1 a b 5", "BALANCE a USD", "BALANCE a EUR",
        "BALANCE b EUR",
    ]
    assert process_ledger(commands) == [
        "OK", "OK", "OK", "OK", "ERROR", "ERROR", "20", "0", "0"
    ]


def test_part_2_invalid_rates_are_rejected_without_affecting_later_rates():
    commands = [
        "OPEN a USD", "DEPOSIT dep a USD 10",
        "RATE -1 USD EUR 1 1", "RATE 1 USD USD 1 1", "RATE 1 USD EUR 0 1",
        "RATE 1 USD EUR 1 1", "CONVERT conv 1 a USD EUR 10", "BALANCE a EUR",
    ]
    assert process_ledger(commands) == [
        "OK", "OK", "ERROR", "ERROR", "ERROR", "OK", "OK", "10"
    ]


def test_part_3_direct_rate_wins_over_newer_reverse_rate():
    commands = [
        "OPEN a USD", "DEPOSIT dep a USD 100",
        "RATE 1 USD EUR 1 2", "RATE 10 EUR USD 100 1",
        "CONVERT conv 10 a USD EUR 100", "BALANCE a EUR",
    ]
    assert process_ledger(commands) == ["OK", "OK", "OK", "OK", "OK", "50"]


def test_part_2_failed_conversion_id_is_reusable():
    commands = [
        "OPEN a USD", "DEPOSIT dep a USD 10",
        "CONVERT conv 5 a USD EUR 10", "RATE 5 USD EUR 1 1",
        "CONVERT conv 5 a USD EUR 10", "BALANCE a EUR",
    ]
    assert process_ledger(commands) == ["OK", "OK", "ERROR", "OK", "OK", "10"]


def test_part_4_invalid_transfer_id_is_reusable():
    commands = [
        "OPEN a USD", "OPEN b USD", "DEPOSIT dep a USD 10",
        "TRANSFER move 1 a a 10", "TRANSFER move 1 a b 10",
        "BALANCE a USD", "BALANCE b USD",
    ]
    assert process_ledger(commands) == ["OK", "OK", "OK", "ERROR", "OK", "0", "10"]


def test_part_4_transfer_can_use_an_inverse_rate():
    commands = [
        "OPEN eur EUR", "OPEN usd USD", "DEPOSIT dep eur EUR 50",
        "RATE 1 USD EUR 1 2", "TRANSFER move 1 eur usd 50",
        "BALANCE eur EUR", "BALANCE usd USD",
    ]
    assert process_ledger(commands) == ["OK", "OK", "OK", "OK", "OK", "0", "100"]


def test_part_2_later_rate_wins_an_equal_timestamp_tie():
    commands = [
        "OPEN a USD", "DEPOSIT dep a USD 100",
        "RATE 1 USD EUR 1 2", "RATE 1 USD EUR 3 4",
        "CONVERT conv 1 a USD EUR 100", "BALANCE a EUR",
    ]
    assert process_ledger(commands) == ["OK", "OK", "OK", "OK", "OK", "75"]


def test_part_3_ineligible_direct_rate_does_not_block_eligible_inverse():
    commands = [
        "OPEN a USD", "DEPOSIT dep a USD 100",
        "RATE 10 USD EUR 9 10", "RATE 5 EUR USD 2 1",
        "CONVERT conv 5 a USD EUR 100", "BALANCE a EUR",
    ]
    assert process_ledger(commands) == ["OK", "OK", "OK", "OK", "OK", "50"]


def test_part_2_same_currency_conversion_is_invalid_and_id_is_reusable():
    commands = [
        "OPEN a USD", "DEPOSIT dep a USD 10",
        "CONVERT conv 1 a USD USD 5", "RATE 1 USD EUR 1 1",
        "CONVERT conv 1 a USD EUR 5", "BALANCE a EUR",
    ]
    assert process_ledger(commands) == ["OK", "OK", "ERROR", "OK", "OK", "5"]


def test_part_4_negative_operation_timestamps_are_invalid_without_reserving_ids():
    commands = [
        "OPEN a USD", "OPEN b EUR", "DEPOSIT dep a USD 20",
        "RATE 0 USD EUR 1 1",
        "CONVERT conv -1 a USD EUR 5", "CONVERT conv 0 a USD EUR 5",
        "TRANSFER move -1 a b 5", "TRANSFER move 0 a b 5",
        "BALANCE a USD", "BALANCE a EUR", "BALANCE b EUR",
    ]
    assert process_ledger(commands) == [
        "OK", "OK", "OK", "OK", "ERROR", "OK", "ERROR", "OK", "10", "5", "5"
    ]

def test_part_1_invalid_numeric_token_returns_error_instead_of_raising():
    commands = [
        "OPEN a USD",
        "DEPOSIT d a USD ²",
        "BALANCE a USD",
    ]
    assert process_ledger(commands) == ["OK", "ERROR", "0"]