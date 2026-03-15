def get_range_for_difficulty(difficulty: str) -> tuple:
    """Return the inclusive (low, high) range for a given difficulty level.

    The range determines the pool of possible secret numbers. A wider range
    makes the game harder because there are more values to guess from.

    Args:
        difficulty: One of ``"Easy"``, ``"Normal"``, or ``"Hard"``
            (case-sensitive).

    Returns:
        A ``(low, high)`` tuple of integers representing the inclusive bounds
        of the guessing range::

            "Easy"   → (1, 20)
            "Normal" → (1, 50)
            "Hard"   → (1, 100)

    Raises:
        NotImplementedError: This function has not yet been refactored out of
            ``app.py``. Move the implementation here before calling it.

    Example:
        >>> low, high = get_range_for_difficulty("Easy")
        >>> low, high
        (1, 20)
    """
    raise NotImplementedError(
        "Refactor this function from app.py into logic_utils.py")


def parse_guess(raw: str) -> tuple:
    """Parse raw text input from the player into a validated integer guess.

    Accepts whole numbers and decimal strings (decimals are truncated toward
    zero via ``int(float(raw))``). Returns a three-element tuple so the caller
    can distinguish between a valid guess, an empty/missing input, and a
    non-numeric entry without raising exceptions.

    Args:
        raw: The raw string typed by the player. May be ``None``, empty, a
            valid integer string (``"42"``), a decimal string (``"3.7"``), or
            a non-numeric string (``"abc"``).

    Returns:
        A three-element tuple ``(ok, guess_int, error_message)``:

        - ``ok`` (bool): ``True`` if parsing succeeded, ``False`` otherwise.
        - ``guess_int`` (int | None): The parsed integer value when ``ok`` is
          ``True``; ``None`` on failure.
        - ``error_message`` (str | None): A human-readable error string when
          ``ok`` is ``False``; ``None`` on success.

    Raises:
        NotImplementedError: This function has not yet been refactored out of
            ``app.py``. Move the implementation here before calling it.

    Examples:
        >>> parse_guess("42")
        (True, 42, None)

        >>> parse_guess("3.7")
        (True, 3, None)

        >>> parse_guess("")
        (False, None, 'Enter a guess.')

        >>> parse_guess("abc")
        (False, None, 'That is not a number.')
    """
    raise NotImplementedError(
        "Refactor this function from app.py into logic_utils.py")


def check_guess(guess: int, secret) -> tuple:
    """Compare a player's guess against the secret and return the outcome.

    Both ``guess`` and ``secret`` are cast to ``int`` before comparison,
    guarding against the string-secret bug present in older versions of the
    caller (see FIXME comment below for details).

    Args:
        guess: The player's guessed number. Accepts ``int`` or any value
            safely convertible via ``int()`` (e.g. ``float``, numeric
            ``str``). Decimal strings such as ``"3.7"`` are **not** supported
            and will raise ``ValueError``.
        secret: The hidden target number. Same type flexibility as ``guess``.

    Returns:
        A two-element tuple ``(outcome, message)``:

        - ``outcome`` (str): One of ``"Win"``, ``"Too High"``,
          or ``"Too Low"``.
        - ``message`` (str): An emoji-annotated hint for the player:

          - ``"🎉 Correct!"`` on a win.
          - ``"📉 Go LOWER!"`` when the guess exceeds the secret.
          - ``"📈 Go HIGHER!"`` when the guess falls below the secret.

    Raises:
        ValueError: If ``guess`` or ``secret`` cannot be converted to ``int``
            (e.g. passing the string ``"3.7"``).

    Examples:
        >>> check_guess(50, 50)
        ('Win', '🎉 Correct!')

        >>> check_guess(80, 50)
        ('Too High', '📉 Go LOWER!')

        >>> check_guess(20, 50)
        ('Too Low', '📈 Go HIGHER!')

        >>> check_guess(15, "8")   # string secret — cast to int(8) = 8
        ('Too High', '📉 Go LOWER!')
    """
    # FIXME: The original version in app.py had two related bugs:
    #   1. On even attempts, the caller passed str(secret) instead of
    #      int(secret). This caused a TypeError in the int comparison,
    #      falling into an except block that used lexicographic string
    #      comparison — e.g. "15" > "8" is False because "1" < "8",
    #      silently inverting the Too High / Too Low hints.
    #   2. The outcome labels and hint messages were swapped: "Too High"
    #      returned "Go HIGHER" and "Too Low" returned "Go LOWER", which
    #      is the opposite of what the player should do.
    #   Both bugs are fixed below: secret is cast to int to prevent type
    #   mismatches, and the messages now correctly direct the player.
    guess = int(guess)
    secret = int(secret)
    if guess == secret:
        return "Win", "🎉 Correct!"
    if guess > secret:
        return "Too High", "📉 Go LOWER!"
    return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int) -> int:
    """Calculate and return an updated score based on the outcome of a guess.

    Scoring rules:

    - **Win**: Awards ``100 - 10 * (attempt_number + 1)`` points, with a
      minimum of 10 points. Winning earlier yields a higher bonus.
    - **Too High on an even attempt**: Awards +5 points (partial credit).
    - **Too High on an odd attempt**: Deducts 5 points.
    - **Too Low**: Always deducts 5 points.
    - **Any other outcome**: Score is unchanged.

    Args:
        current_score: The player's score before this guess.
        outcome: The result string from :func:`check_guess` — one of
            ``"Win"``, ``"Too High"``, or ``"Too Low"``.
        attempt_number: The 1-based index of the current attempt (i.e. how
            many guesses the player has made so far, including this one).

    Returns:
        The new integer score after applying the outcome's point adjustment.

    Raises:
        NotImplementedError: This function has not yet been refactored out of
            ``app.py``. Move the implementation here before calling it.

    Examples:
        >>> update_score(0, "Win", 1)
        80

        >>> update_score(50, "Too Low", 3)
        45

        >>> update_score(50, "Too High", 2)   # even attempt → +5
        55

        >>> update_score(50, "Too High", 3)   # odd attempt → -5
        45
    """
    raise NotImplementedError(
        "Refactor this function from app.py into logic_utils.py")
