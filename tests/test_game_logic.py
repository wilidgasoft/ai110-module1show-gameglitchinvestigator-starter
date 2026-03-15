import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from logic_utils import check_guess  # noqa: E402


# ---------------------------------------------------------------------------
# Original tests — fixed: check_guess returns (outcome, message), not a str
# ---------------------------------------------------------------------------

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"


def test_guess_too_high():
    # If secret is 50 and guess is 60, outcome should be "Too High"
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"


def test_guess_too_low():
    # If secret is 50 and guess is 40, outcome should be "Too Low"
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"


# ---------------------------------------------------------------------------
# Bug fix: hint messages were swapped
#   Before: guess > secret → "📈 Go HIGHER!"  (wrong — player should go lower)
#           guess < secret → "📉 Go LOWER!"   (wrong — player should go higher)
#   After:  guess > secret → "📉 Go LOWER!"
#           guess < secret → "📈 Go HIGHER!"
# ---------------------------------------------------------------------------

def test_too_high_message_directs_player_lower():
    """Hint must say LOWER (not HIGHER) when guess exceeds the secret."""
    _, message = check_guess(80, 50)
    assert "LOWER" in message, f"Expected 'LOWER' in message, got: {message}"


def test_too_low_message_directs_player_higher():
    """Hint must say HIGHER (not LOWER) when guess falls below the secret."""
    _, message = check_guess(20, 50)
    assert "HIGHER" in message, f"Expected 'HIGHER' in message, got: {message}"


# ---------------------------------------------------------------------------
# Bug fix: string-secret type coercion
#   On even attempts, app.py passed str(secret) into check_guess.
#   Python's lexicographic string comparison inverted hints for many values —
#   e.g. "15" > "8" is False (because "1" < "8"), so guess=15, secret="8"
#   would wrongly return "Too Low" instead of "Too High".
#   Fixed: check_guess now casts both values to int before comparing.
# ---------------------------------------------------------------------------

def test_string_secret_too_high():
    """guess=15, secret='8': lexicographically '15'>'8' is False, so old code
    returned 'Too Low'. int cast gives 15 > 8 = True → correct 'Too High'."""
    outcome, message = check_guess(15, "8")
    assert outcome == "Too High", f"Expected 'Too High', got: {outcome}"
    assert "LOWER" in message


def test_string_secret_too_low():
    """guess=10, secret='50' passed as string should still yield 'Too Low'."""
    outcome, message = check_guess(10, "50")
    assert outcome == "Too Low", f"Expected 'Too Low', got: {outcome}"
    assert "HIGHER" in message


def test_string_secret_win():
    """Win detection must still work when secret is passed as a string."""
    outcome, _ = check_guess(42, "42")
    assert outcome == "Win"


def test_string_secret_boundary_low():
    """guess=9, secret='10': 9 < 10 → Too Low (string '9'>'10' would be True,
    which was the old incorrect behaviour)."""
    outcome, _ = check_guess(9, "10")
    assert outcome == "Too Low"


def test_string_secret_boundary_high():
    """guess=11, secret='10': 11 > 10 → Too High."""
    outcome, _ = check_guess(11, "10")
    assert outcome == "Too High"


# ---------------------------------------------------------------------------
# Edge cases: negative numbers
#   int() handles negatives just fine, so check_guess should work correctly.
# ---------------------------------------------------------------------------

def test_negative_guess_is_too_low():
    """A negative guess is always below a positive secret."""
    outcome, message = check_guess(-5, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message


def test_negative_secret_makes_positive_guess_too_high():
    """When the secret itself is negative, a positive guess is Too High."""
    outcome, message = check_guess(5, -10)
    assert outcome == "Too High"
    assert "LOWER" in message


# ---------------------------------------------------------------------------
# Edge cases: decimal / float inputs
#   int(float) truncates toward zero — e.g. int(3.7) == 3, int(4.9) == 4.
#   Decimal *strings* like "3.7" are NOT supported and raise ValueError.
# ---------------------------------------------------------------------------

def test_float_guess_truncates_to_int():
    """3.7 truncates to 3, which is less than 4 → Too Low."""
    outcome, _ = check_guess(3.7, 4)
    assert outcome == "Too Low"


def test_float_guess_truncation_can_produce_win():
    """4.9 truncates to 4, which equals the secret 4 → Win.
    This is a known truncation side-effect worth documenting."""
    outcome, _ = check_guess(4.9, 4)
    assert outcome == "Win"


def test_decimal_string_raises_value_error():
    """'3.7' cannot be cast directly to int — int('3.7') raises ValueError.
    parse_guess must catch this before it reaches check_guess."""
    with pytest.raises(ValueError):
        check_guess("3.7", 50)


# ---------------------------------------------------------------------------
# Edge cases: extremely large values
#   Python integers have arbitrary precision, so huge numbers work fine.
# ---------------------------------------------------------------------------

def test_very_large_guess_is_too_high():
    """A quadrillion is way above any normal secret."""
    outcome, _ = check_guess(10**15, 50)
    assert outcome == "Too High"


def test_very_large_negative_guess_is_too_low():
    """A large negative is way below any normal secret."""
    outcome, _ = check_guess(-10**15, 50)
    assert outcome == "Too Low"


def test_very_large_equal_values_is_win():
    """Two identical huge numbers should still register as a Win."""
    outcome, _ = check_guess(10**15, 10**15)
    assert outcome == "Win"


# ---------------------------------------------------------------------------
# Edge cases: zero boundary
# ---------------------------------------------------------------------------

def test_zero_guess_is_too_low():
    """0 is below any positive secret."""
    outcome, _ = check_guess(0, 50)
    assert outcome == "Too Low"


def test_zero_secret_makes_positive_guess_too_high():
    """Any positive guess is above a secret of 0."""
    outcome, _ = check_guess(5, 0)
    assert outcome == "Too High"
