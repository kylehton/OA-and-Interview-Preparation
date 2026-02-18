from p05_rate_limiter.solution import RateLimiter


def test_basic_same_second():
    rl = RateLimiter(2, 5)
    assert rl.allow(10) is True
    assert rl.allow(10) is True
    assert rl.allow(10) is False


def test_window_boundary_math():
    # window [T-window+1 .. T]
    rl = RateLimiter(2, 3)
    assert rl.allow(10) is True
    assert rl.allow(10) is True
    assert rl.allow(12) is False  # window at 12 is [10..12] includes both allowed at 10


def test_old_requests_expire():
    rl = RateLimiter(2, 3)
    assert rl.allow(10) is True
    assert rl.allow(10) is True
    assert rl.allow(13) is True  # window at 13 is [11..13], old 10s expired


def test_rejections_do_not_count():
    rl = RateLimiter(1, 10)
    assert rl.allow(5) is True
    assert rl.allow(5) is False
    assert rl.allow(6) is False
    assert rl.allow(20) is True


def test_non_monotonic_timestamps():
    # Still must behave correctly.
    rl = RateLimiter(2, 4)
    assert rl.allow(10) is True
    assert rl.allow(11) is True
    # timestamp goes backwards: at 9, window is [6..9] includes none => allow
    assert rl.allow(9) is True
    # at 11 again, window [8..11] includes allowed at 9,10,11 => 3, max 2 => reject
    assert rl.allow(11) is False
