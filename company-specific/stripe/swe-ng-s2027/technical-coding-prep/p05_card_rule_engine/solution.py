"""Starter for P05. Read README.md before implementing."""

from __future__ import annotations


class CardEngine:
    def __init__(self):
        # bucket sorted array of 3-tuple (start, end, network) keyed by leading digit
        self.bin_ranges = [[] for _ in range(10)]

    def trim(self, string: str) -> str:
        return string.strip().replace(" ", "")

    def find_network(self, card_num: str, country: str):
        digit_key = int(card_num[0])
        curr_span = float('inf')
        curr_network = None
        for bin in self.bin_ranges[digit_key]:
            start, end, network, countries = bin
            if countries is None or country in countries or '*' in countries:
                if start <= int(card_num[:6]) <= end:
                    if (end - start) < curr_span:
                        curr_network = network
                        curr_span = end - start
        return curr_network
    def normalize_card(self, card: list[str]):
        if len(card) == 3:
            payment_id = self.trim(card[0])
            card_num = self.trim(card[1]).replace('-', '')
            country = self.trim(card[2])
            if len(payment_id) != 0: 
                if card_num.isnumeric() and 12 <= len(card_num) <= 19 and card_num.isascii() and country.isalpha() and country.isascii() and country.isupper() and len(country) == 2:
                    if not self.checksum(card_num):
                        return f'{payment_id},NONE,INVALID_LUHN'
                    else:
                        network = self.find_network(card_num, country)
                        if network is not None:
                            return f'{payment_id},{network},VALID'
                        return f'{payment_id},NONE,UNSUPPORTED'
                else:
                    return f'{payment_id},NONE,INVALID_FORMAT'
        return 'ERROR'

    def checksum(self, card_num: str) -> bool:
        double = 0
        index = len(card_num)-1
        while index >= 0:
            digit = int(card_num[index])
            if double % 2 == 1:
                digit *= 2
                if digit > 9:
                    digit -= 9
                    card_num = card_num[0:index] + chr(digit) + card_num[index+1:]
            index -= 1
        return int(card_num) % 2 == 0

    def check_range(self, range_str: str):
        range_str = self.trim(range_str)
        if range_str.isascii() and range_str.isnumeric() and len(range_str) == 6:
            return True
        
    def parse_bin_ranges(self, bin_ranges: list[str]):
        for bin_range in bin_ranges:
            result = None
            parts = bin_range.split(',')
            countries = None
            if 3 <= len(parts) <= 4: 
                if len(parts) == 4:
                    start, end, network, countries = parts
                else:
                    start, end, network = parts
                start, end, network = self.trim(start), self.trim(end), self.trim(network)
                if self.check_range(start) and self.check_range(end) and len(network) != 0:
                    digit_key = int(start[0])
                    start = int(start)
                    end = int(end)
                    if start <= end:
                        result = [start, end, network, None]
                        if countries and len(countries) > 0:
                            countries = (str(countries)).split('|')
                            country_set = set()
                            for country in countries:
                                country = self.trim(country)  
                                if len(country) != 2 and country != '*':
                                    result = None                         
                                elif len(country) == 2 and country.isascii() and country.isupper():
                                    country_set.add(self.trim(country))
                                    if result and len(country_set) == len(countries):
                                        result[3] = country_set
                                        print(country_set)
            if result is not None:
                self.bin_ranges[digit_key].append(result)

def validate_cards(cards: list[str], bin_ranges: list[str]) -> list[str]:
    """Validate cards and optionally route them using BIN rules."""
    cardEngine = CardEngine()
    responses = []
    cardEngine.parse_bin_ranges(bin_ranges)
    for row in cards:
        card = row.split(',')
        res = (cardEngine.normalize_card(card))
        responses.append(res)
    return responses
    
