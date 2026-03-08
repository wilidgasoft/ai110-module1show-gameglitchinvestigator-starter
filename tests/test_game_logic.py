import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from logic_utils import check_guess


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
    """When the guess is above the secret, the hint must say LOWER, not HIGHER."""
    _, message = check_guess(80, 50)
    assert "LOWER" in message, f"Expected 'LOWER' in message, got: {message}"

def test_too_low_message_directs_player_higher():
    """When the guess is below the secret, the hint must say HIGHER, not LOWER."""
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
    """guess=15, secret='8': lexicographically '15'>'8' is False, so the old code
    returned 'Too Low'. Casting to int gives 15 > 8 = True → correct 'Too High'."""
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
