# tender can be split into gift card and credit card
# there is no provided credit card, so we store some balance as
# credit available/owed by customer
# refunds are possible, so we should store all transac history too
# gift cards have an expr date, so we can store in a heap based on date

# CHARGE event logic: gift cards come first, deducing from their balance
# if charge amt exceeds avail gift card balance(s), deduct and store remaining
# unpaid as the credit card charge

# RETURN
# ADD_GIFTCARD -> ""
# CHARGE -> credit card charge amount, gift card id(s):amount used, gift card 2 ....

# should store by customer id, we can have a dict keyed by cust id, storing
# a heap and credit as an int
# all gift cards in get placed as (date, id, balance)

# REFUND -> cc amt refunded, new gc balance (if created)
# refund amount < cc charge
#   remainder will be negative, need to stop at 0

import heapq

class Solution:
    def processEvents(self, events: List[str], surchargeRates: List[str]) -> List[str]:

        def apply_surcharge(amount: int, zip_code: str) -> int:
            if amount > 0:
                for start, end, rate in surcharges:
                    if start <= zip_code <= end:
                        amount += int((amount * rate))
                        break
            return amount

        def apply_gift_cards(amt: int, gift_cards: List[tuple[int | float, str, int]], timestamp: int) -> tuple[int, List[str]]:
            gc_used = []
            while amt > 0 and gift_cards:
                expr, gc_id, balance = heapq.heappop(gift_cards)
                if timestamp < expr:
                    gc_balance_used = min(balance, amt)
                    amt -= gc_balance_used # remaining balance
                    gift_card_string = gc_id + ':' + str(gc_balance_used)
                    gc_used.append(gift_card_string)
                                
                    if balance > gc_balance_used:
                        heapq.heappush(gift_cards, (expr, gc_id, balance - gc_balance_used))     
            return amt, gc_used
            
        wallet = {}
        result = []
        surcharges = []
        transactions = {}

        for surcharge in surchargeRates:
            zc_range, rate = surcharge.strip().split(':')
            start, end = zc_range.strip().split('-')
            surcharges.append((start, end, float(rate)))
        
        for event in events:
            parts = event.strip().split(',')
            timestamp, operation = parts[0], parts[1]
            timestamp = int(timestamp)
            if operation == 'ADD_GIFTCARD':
                _, _, cust_id, card_id, amt, expr_date = parts
                amt = int(amt)
                if cust_id not in wallet:
                    wallet[cust_id] = []
                if amt > 0:
                    heapq.heappush(wallet[cust_id], (int(expr_date), card_id, amt))
                result.append("")
                
            elif operation == 'CHARGE':
                _, _, charge_id, cust_id, amt, zip_code = parts
                amt = int(amt)

                gift_cards = wallet.get(cust_id, [])
                amt, gc_used = apply_gift_cards(amt, gift_cards, timestamp)

                amt = apply_surcharge(amt, zip_code)
                transactions[charge_id] = (amt, cust_id)
                    
                gc_used.sort()
                result.append(",".join([str(amt)] + gc_used)) 
                    
            elif operation == 'REFUND':
                _, _, charge_id, refund_amount = parts
                refund_amount = int(refund_amount)
                cc_charge, cust_id = transactions[charge_id]
                remaining = max(refund_amount - cc_charge, 0)
                if (remaining > 0): # need to put rest in new gift card
                    heapq.heappush(wallet[cust_id], (float('inf'), f'REFUND_{charge_id}', remaining))
                result.append(f'{min(refund_amount, cc_charge)},{remaining}')

        return result