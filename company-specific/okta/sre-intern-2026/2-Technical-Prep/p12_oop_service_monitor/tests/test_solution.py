import threading
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from solution import ServiceMonitor, ThreadSafeServiceMonitor


def test_basic_monitor():
    m = ServiceMonitor()
    m.record("a", 200)
    m.record("a", 500)
    m.record("b", 500)
    m.record("b", 500)
    m.record("c", 200)

    assert m.error_rate("a") == 0.5
    assert m.error_rate("b") == 1.0
    assert m.error_rate("missing") == 0.0

    # sorting rules: b(1.0), a(0.5), c(0.0)
    assert m.top_unhealthy(10) == [("b", 1.0), ("a", 0.5), ("c", 0.0)]


def test_invalid_records_ignored():
    m = ServiceMonitor()
    m.record("", 500)
    m.record("a", "500")  # type: ignore
    m.record("a", 200)
    assert m.error_rate("a") == 0.0  # 0 errors / 1 total


def test_ties_by_total_then_name():
    m = ServiceMonitor()
    # a: 1/2 = 0.5, total 2
    m.record("a", 500)
    m.record("a", 200)
    # b: 1/3 = 0.3333
    m.record("b", 500)
    m.record("b", 200)
    m.record("b", 200)
    # c: 1/2 = 0.5, total 2 -> tie with a, name asc
    m.record("c", 500)
    m.record("c", 200)

    assert m.top_unhealthy(3) == [("a", 0.5), ("c", 0.5), ("b", 0.3333)]


def test_thread_safe_monitor_smoke():
    m = ThreadSafeServiceMonitor()

    def worker():
        for _ in range(500):
            m.record("api", 500)
            m.record("api", 200)

    threads = [threading.Thread(target=worker) for _ in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    # Expect ~50% error rate
    assert m.error_rate("api") == 0.5
