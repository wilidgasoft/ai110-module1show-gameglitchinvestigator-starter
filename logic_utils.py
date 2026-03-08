def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    raise NotImplementedError("Refactor this function from app.py into logic_utils.py")


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    raise NotImplementedError("Refactor this function from app.py into logic_utils.py")


def check_guess(guess: int, secret) -> tuple:
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    # FIXME: The original version in app.py had two related bugs:
    #   1. On even attempts, the caller passed str(secret) instead of int(secret).
    #      This caused a TypeError in the int comparison, falling into an except block
    #      that used lexicographic string comparison — e.g. "15" > "8" is False because
    #      "1" < "8", silently inverting the Too High / Too Low hints.
    #   2. The outcome labels and hint messages were swapped: "Too High" returned
    #      "Go HIGHER" and "Too Low" returned "Go LOWER", which is the opposite of
    #      what the player should do.
    #   Both bugs are fixed below: secret is cast to int to prevent type mismatches,
    #   and the messages now correctly direct the player.
    guess = int(guess)
    secret = int(secret)
    if guess == secret:
        return "Win", "🎉 Correct!"
    if guess > secret:
        return "Too High", "📉 Go LOWER!"
    return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    raise NotImplementedError("Refactor this function from app.py into logic_utils.py")
