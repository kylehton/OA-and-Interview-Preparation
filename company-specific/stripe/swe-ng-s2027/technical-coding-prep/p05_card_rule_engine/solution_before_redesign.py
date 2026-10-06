"""Preserved P05 attempt from before the 2026-10-06 problem redesign."""

from __future__ import annotations

import csv


class CardEngine:
    def __init__(self):
        self.bin = 0

    def trim_str(self, string: str):
        string = string.replace(" ", "")
        string = string.replace("-", "")
        return string

    def normalize_card(self, parts: list[str]):
        print(parts)
        if len(parts) == 3:
            payment_id = parts[0]
            card_number = self.trim_str(parts[1])
            country = parts[2]
            if (card_number).isnumeric() and (12 <= len(card_number) <= 19):
                if len(payment_id) > 0 and country.isascii() and country.isupper() and len(country) == 2:
                    return f'{payment_id},{card_number},{country}'
        else:
            return 'ERROR'
        return f'{parts[0]},NONE,INVALID_FORMAT'


def validate_cards(cards: list[str], bin_ranges: list[str]) -> list[str]:
    """Classify every card row in input order."""
    responses = []
    cardEngine = CardEngine()
    for card in csv.reader(cards):
        responses.append(cardEngine.normalize_card(card))
    return responses
