from datetime import date, timedelta


def is_business_day(day: date, holidays: set[date]) -> bool:
    return day.weekday() < 5


def next_business_day(day: date, holidays: set[date]) -> date:
    current = day + timedelta(days=1)
    while not is_business_day(current, holidays):
        current += timedelta(days=1)
    return current


def normalize_business_day(day: date, holidays: set[date]) -> date:
    current = day
    while not is_business_day(current, holidays):
        current += timedelta(days=1)
    return current

