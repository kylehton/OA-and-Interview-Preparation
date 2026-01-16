"""
Problem 1
You are given a list of events representing charges and disputes.
Input Format: def flagged_merchants(events: list[str])-> list[str]:
- events is a list of strings
- Each string is exactly one of:
- "CHARGE <merchant_id> <amount>"
- "DISPUTE <merchant_id> <amount>"
- <merchant_id> is a non-empty string
- <amount> is a positive integer (representing cents)

A merchant is flagged if:
(total_disputed_amount / total_charged_amount) > 0.25

Return a list of merchant IDs that are flagged, sorted lexicographically.

Constraints:
- Events are processed in order
- Amounts are positive integers
- A dispute can occur before any charge
- Process all events before flagging
- Division by zero must be handled safely
"""

# must check whether the disputed amount is over 25% of the charged amount
# need to track user amount based on charges, using merchant id as key
# checks: make sure charged amount not 0 before division

from collections import defaultdict
from email.policy import default

def flagged_merchants(events: list[str])-> list[str]:
    charge_log = defaultdict(list)
    flagged = []
    for event in events:
        operation, merchant_id, amount = event.strip().split()
        amount = int(amount)
        if operation.upper() == 'CHARGE':
            if merchant_id not in charge_log:
                charge_log[merchant_id] = [amount, 0]
            else:
                charge_log[merchant_id][0] += amount
        elif operation.upper() == 'DISPUTE':
            if merchant_id not in charge_log:
                charge_log[merchant_id] = [0, amount]
            else:
                charge_log[merchant_id][1] += amount
    for merc_id in charge_log.keys():
        curr_merchant = charge_log[merc_id]
        if curr_merchant[0] == 0:
            continue
        elif (curr_merchant[1]/curr_merchant[0]) > 0.25:
            flagged.append(merc_id)
    flagged.sort()
    return flagged

def p1_test_cases():
    events1 = [
    "CHARGE m1 100",
    "DISPUTE m1 30"
    ]
    expected = ["m1"]
    result = flagged_merchants(events1)
    assert result == expected, f"1. Expected {expected}, got {result}"

    events2 = [
    "CHARGE m1 100",
    "DISPUTE m1 20"
    ]
    expected = []
    result = flagged_merchants(events2)
    assert result == expected, f"2. Expected {expected}, got {result}"

    events3 = [
    "CHARGE m1 100",
    "DISPUTE m1 30",
    "CHARGE m2 200",
    "DISPUTE m2 40"
    ]
    expected = ["m1"]
    result = flagged_merchants(events3)
    assert result == expected, f"3. Expected {expected}, got {result}"

    events4 = [
    "DISPUTE m1 50",
    "CHARGE m1 100"
    ]
    expected = ["m1"]
    result = flagged_merchants(events4)
    assert result == expected, f"4. Expected {expected}, got {result}"

    events5 = [
    "DISPUTE m1 100"
    ]
    expected = []
    result = flagged_merchants(events5)
    assert result == expected, f"5. Expected {expected}, got {result}"

    events6 = [
    "CHARGE m1 200",
    "DISPUTE m1 30",
    "DISPUTE m1 30"
    ]
    expected = ["m1"]
    result = flagged_merchants(events6)
    assert result == expected, f"6. Expected {expected}, got {result}"

    events7 = [
        "CHARGE b 100",
        "DISPUTE b 30",
        "CHARGE a 100",
        "DISPUTE a 30"
    ]
    expected = ["a", "b"]
    result = flagged_merchants(events7)
    assert result == expected, f"7. Expected {expected}, got {result}"

    print("Problem 1: All test cases passed!")


"""
Problem 2

Input Format: def total_processed_amount(events: list[str]) -> int:
- events is a list of strings

Each string is exactly:
- "PAY <transaction_id> <amount>"
- <transaction_id> is a unique string identifier

<amount> is a positive integer

Rules:
- Each transaction ID may appear multiple times
- Only the first occurrence of a transaction ID is counted
- Sum all unique transaction amounts
- Order of events does not matter

Output Format:
- Return a single integer: total processed amount
"""

# we essentially go through the entire list of amounts, summing only the first occurrence
# we can use a set to track already summed transaction ids
def total_processed_amount(events: list[str]) -> list[str]:
    seen = set()
    total_sum = 0
    for event in events:
        operation, transaction_id, amount = event.strip().split()
        amount = int(amount)
        if operation.upper() == 'PAY':
            if transaction_id not in seen:
                total_sum += amount
                seen.add(transaction_id)
    
    return total_sum

def p2_test_cases():
    events1 = [
        "PAY tx1 100",
        "PAY tx2 200",
        "PAY tx1 100"
    ]
    expected = 300
    result = total_processed_amount(events1)
    assert result == expected, f"1. Expected {expected}, got {result}"

    events2 = []
    expected = 0
    result = total_processed_amount(events2)
    assert result == expected, f"2. Expected {expected}, got {result}"

    events3 = [
        "PAY tx1 50"
    ]
    expected = 50
    result = total_processed_amount(events3)
    assert result == expected, f"3. Expected {expected}, got {result}"

    events4 = [
        "PAY tx1 100",
        "PAY tx1 200"
    ]
    expected = 100
    result = total_processed_amount(events4)
    assert result == expected, f"4. Expected {expected}, got {result}"

    events5 = [
        "PAY a 10",
        "PAY b 20",
        "PAY c 30"
    ]
    expected = 60
    result = total_processed_amount(events5)
    assert result == expected, f"5. Expected {expected}, got {result}"

    events6 = [
        "PAY x 1",
        "PAY y 2",
        "PAY x 1",
        "PAY y 2"
    ]
    expected = 3
    result = total_processed_amount(events6)
    assert result == expected, f"6. Expected {expected}, got {result}"

    print("Problem 2: All test cases passed!")

"""
Question 3: Account Lockout System

Input Format: 
def locked_users(events: list[str]) -> list[str]:

Each string:
"LOGIN <user_id> <status>"
<status> ∈ {"SUCCESS", "FAIL"}

Rules:
- Track consecutive FAILs per user
- A user is locked after 3 consecutive FAILs
- SUCCESS resets failure count
- Once locked, user stays locked
- Return locked user IDs sorted lexicographically

Output Format:
- List of strings
"""
# we need to track consec fails -> use defaultdict, increment on fail, reset on success
# for staying locked, check curr count, if 3, do not allow data mutation
def locked_users(events: list[str]) -> list[str]:
    fail_dict = defaultdict(int)
    locked = []
    for event in events:
        operation, user_id, status = event.strip().split()
        if operation.upper() == 'LOGIN':
            if user_id in fail_dict and fail_dict[user_id] >= 3:
                continue
            elif status.upper() == 'SUCCESS' and user_id in fail_dict:
                    fail_dict[user_id] = 0
            elif status.upper() == "FAIL":
                fail_dict[user_id] += 1
                if fail_dict[user_id] > 2:
                    locked.append(user_id)
    locked.sort()
    return locked

def p3_test_cases():
    events1 = [
        "LOGIN u1 FAIL",
        "LOGIN u1 FAIL",
        "LOGIN u1 FAIL"
    ]
    expected = ["u1"]
    result = locked_users(events1)
    assert result == expected, f"1. Expected {expected}, got {result}"

    events2 = [
        "LOGIN u1 FAIL",
        "LOGIN u1 SUCCESS",
        "LOGIN u1 FAIL",
        "LOGIN u1 FAIL",
        "LOGIN u1 FAIL"
    ]
    expected = ["u1"]
    result = locked_users(events2)
    assert result == expected, f"2. Expected {expected}, got {result}"

    events3 = [
        "LOGIN u1 FAIL",
        "LOGIN u2 FAIL",
        "LOGIN u1 FAIL",
        "LOGIN u1 FAIL",
        "LOGIN u2 FAIL",
        "LOGIN u2 FAIL",
        "LOGIN u2 FAIL"
    ]
    expected = ["u1", "u2"]
    result = locked_users(events3)
    assert result == expected, f"3. Expected {expected}, got {result}"

    events4 = []
    expected = []
    result = locked_users(events4)
    assert result == expected, f"4. Expected {expected}, got {result}"

    events5 = [
        "LOGIN u1 SUCCESS",
        "LOGIN u1 SUCCESS",
        "LOGIN u1 FAIL",
        "LOGIN u1 FAIL"
    ]
    expected = []
    result = locked_users(events5)
    assert result == expected, f"5. Expected {expected}, got {result}"

    print("Problem 3: All test cases passed!")


"""
Question 4: Fraud Score Ranking
def fraud_ranking(events: list[str]) -> list[str]:

Rules:
- Same CHARGE / DISPUTE rules as before
- fraud_score = dispute / charge
- Include merchants with score ≥ 0.2

Sort by:
- Descending fraud score
- Lexicographical merchant ID
"""
# charges and disputes, where dispute can come before charges. must accumulate tg
# we can use a list to store charges [0] and disputes [1]
# this time, sort based on score, then on merchant id
# we can use another dict to store id: fraud score, and sort based on keys, then vals
def fraud_ranking(events: list[str]) -> list[str]:
    event_dict = defaultdict(list)
    fraud_score_dict = defaultdict(float)
    for event in events:
        operation, event_id, amount = event.strip().split()
        operation = operation.upper()
        amount = int(amount)
        if operation == 'CHARGE':
            if event_id not in event_dict:
                event_dict[event_id] = [amount, 0]
            else:
                event_dict[event_id][0] += amount
        elif operation == 'DISPUTE':
            if event_id not in event_dict:
                event_dict[event_id] = [0, amount]
            else:
                event_dict[event_id][1] += amount
        
    for key, value in event_dict.items():
        if value[0] > 0:
            f_score = value[1]/value[0]
            if f_score >= 0.2:
                fraud_score_dict[key] = f_score
    
    result = sorted(fraud_score_dict.items(), key = lambda item: (-item[1], item[0]))

    return_result = []
    for item in result:
        return_result.append(item[0])

    return return_result


def p4_test_cases():
    events1 = [
        "CHARGE a 100",
        "DISPUTE a 30",
        "CHARGE b 200",
        "DISPUTE b 50"
    ]
    expected = ["a", "b"]
    result = fraud_ranking(events1)
    assert result == expected, f"1. Expected {expected}, got {result}"

    events2 = [
        "CHARGE b 100",
        "DISPUTE b 20",
        "CHARGE a 100",
        "DISPUTE a 20"
    ]
    expected = ["a", "b"]
    result = fraud_ranking(events2)
    assert result == expected, f"2. Expected {expected}, got {result}"

    events3 = [
        "CHARGE a 100",
        "DISPUTE a 10",
        "CHARGE b 100",
        "DISPUTE b 30"
    ]
    expected = ["b"]
    result = fraud_ranking(events3)
    assert result == expected, f"3. Expected {expected}, got {result}"

    events4 = [
        "DISPUTE a 50",
        "CHARGE a 200"
    ]
    expected = ["a"]
    result = fraud_ranking(events4)
    assert result == expected, f"4. Expected {expected}, got {result}"

    events5 = [
        "DISPUTE a 50"
    ]
    expected = []
    result = fraud_ranking(events5)
    assert result == expected, f"5. Expected {expected}, got {result}"

    events6 = [
    "CHARGE a 100",
    "DISPUTE a 20",   
    "CHARGE z 100",
    "DISPUTE z 90"
    ]
    expected = ["z", "a"]
    result = fraud_ranking(events6)
    assert result == expected, f"6. Expected {expected}, got {result}"

    print("Problem 4: All test cases passed!")


if __name__ == '__main__':
    p1_test_cases()
    p2_test_cases()
    p3_test_cases()
    p4_test_cases()