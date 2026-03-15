import json
import os
import random
import streamlit as st
from logic_utils import check_guess


# BUG FIX (resolved with Claude Agent mode): Normal and Hard ranges were
# swapped — Hard had a narrower range (1–50) than Normal (1–100), making
# Hard easier to guess than Normal. Fixed so difficulty scales correctly:
# Easy = 1–20, Normal = 1–50, Hard = 1–100.
def get_range_for_difficulty(difficulty: str):
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 50
    if difficulty == "Hard":
        return 1, 100


def parse_guess(raw: str):
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


HIGHSCORE_FILE = os.path.join(os.path.dirname(__file__), "highscores.json")


def load_high_scores() -> dict:
    if os.path.exists(HIGHSCORE_FILE):
        with open(HIGHSCORE_FILE) as f:
            return json.load(f)
    return {"Easy": 0, "Normal": 0, "Hard": 0}


def save_high_score(difficulty: str, score: int) -> bool:
    """Save score if it beats the current record.

    Returns True if a new high score was set.
    """
    scores = load_high_scores()
    if score > scores.get(difficulty, 0):
        scores[difficulty] = score
        with open(HIGHSCORE_FILE, "w") as f:
            json.dump(scores, f)
        return True
    return False


def update_score(current_score: int, outcome: str, attempt_number: int):
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        if attempt_number % 2 == 0:
            return current_score + 5
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score


st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

# Initialize all session state before any sidebar section reads from it
if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)
if "attempts" not in st.session_state:
    st.session_state.attempts = 1
if "score" not in st.session_state:
    st.session_state.score = 0
if "status" not in st.session_state:
    st.session_state.status = "playing"
if "history" not in st.session_state:
    st.session_state.history = []
if "guess_details" not in st.session_state:
    st.session_state.guess_details = []
if "win_message" not in st.session_state:
    st.session_state.win_message = None
if "new_high_score" not in st.session_state:
    st.session_state.new_high_score = False

st.sidebar.divider()
st.sidebar.subheader("🏆 High Scores")
high_scores = load_high_scores()
for diff in ["Easy", "Normal", "Hard"]:
    st.sidebar.caption(f"{diff}: {high_scores.get(diff, 0)} pts")

st.sidebar.divider()
st.sidebar.subheader("📊 Guess History")
if not st.session_state.guess_details:
    st.sidebar.caption("No guesses yet.")
else:
    game_over = st.session_state.status != "playing"
    for i, entry in enumerate(st.session_state.guess_details, 1):
        g, o = entry["guess"], entry["outcome"]
        icon = "✅" if o == "Win" else ("🔴" if o == "Too High" else "🔵")
        st.sidebar.caption(f"#{i}: **{g}** {icon}")
        if game_over:
            distance = abs(g - st.session_state.secret)
            closeness = max(0.0, 1.0 - distance / max(high - low, 1))
            st.sidebar.progress(closeness)

st.subheader("Make a guess")

# BUG FIX (resolved with Claude Agent mode): Previously hardcoded
# "1 and 100" regardless of difficulty. Now uses `low` and `high`
# from get_range_for_difficulty(difficulty)
# so the message correctly reflects the active range (e.g. 1–20 for Easy).
st.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

raw_guess = st.text_input("Enter your guess:", key=f"guess_input_{difficulty}")

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)


# BUG FIX (resolved with Claude Agent mode): Previously, "New Game" always
# reset the secret using random.randint(1, 100), ignoring the selected
# difficulty. The fix uses `low` and `high` — already computed above via
# get_range_for_difficulty(difficulty) — so the new secret respects the
# correct range.
if new_game:
    st.session_state.attempts = 0
    st.session_state.secret = random.randint(low, high)
    st.session_state.guess_details = []
    st.session_state.status = "playing"
    st.session_state.score = 0
    st.session_state.win_message = None
    st.session_state.new_high_score = False
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        if st.session_state.win_message:
            st.success(st.session_state.win_message)
        if st.session_state.new_high_score:
            st.success("🏆 New high score!")
        st.info("Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

if submit:
    st.session_state.attempts += 1

    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.session_state.history.append(raw_guess)
        st.error(err)
    else:
        st.session_state.history.append(guess_int)

        # FIXME: On even attempts, secret is cast to str before being passed
        # to check_guess. This was the root cause of the high/low bug —
        # string comparisons are lexicographic, so e.g. "15" > "8" is False
        # ("1" < "8"), inverting the hints. check_guess (now in logic_utils.py)
        # casts both values to int to guard against this, but the correct
        # long-term fix is to always pass st.session_state.secret as int here.
        if st.session_state.attempts % 2 == 0:
            secret = str(st.session_state.secret)
        else:
            secret = st.session_state.secret

        outcome, message = check_guess(guess_int, secret)
        st.session_state.guess_details.append(
            {"guess": guess_int, "outcome": outcome})

        if show_hint:
            st.warning(message)

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.session_state.win_message = (
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
            st.session_state.new_high_score = save_high_score(
                difficulty, st.session_state.score)
            st.rerun()
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
