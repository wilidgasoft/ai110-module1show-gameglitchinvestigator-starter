# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable.

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: _"How do I keep a variable from resetting in Streamlit when I click a button?"_
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [x] Describe the game's purpose.
      Is a Game of "Number Guessing" with 3 levels of difficulty and it has a hint that allows you to get the guess number.
- [x] Detail which bugs you found.
      **1. Difficulty ranges were swapped for Normal and Hard**
      **2. The "New Game" button ignored the selected difficulty**
      **3. The hint banner always said "1 and 100"**
      **4. The Too High / Too Low hints were backwards**
      **5. String vs. integer comparison on even attempts**
- [x] Explain what fixes you applied.
      **1. Difficulty ranges were swapped for Normal and Hard**
      Hard was actually easier than Normal — Hard used the range 1–50 while Normal went all the way to 1–100.
      So picking "Hard" gave you fewer numbers to choose from, which made it paradoxically simpler.

  **2. The "New Game" button ignored the selected difficulty**
  No matter what difficulty you had selected, clicking New Game always picked a secret number between
  1 and 100. The code had `random.randint(1, 100)` hardcoded instead of using the correct range.

  **3. The hint banner always said "1 and 100"**
  The info message at the top of the game read "Guess a number between 1 and 100" regardless of
  the difficulty. Easy players were told the wrong range, which was confusing.

  **4. The Too High / Too Low hints were backwards**
  When your guess was above the secret, the game told you to go _higher_. When you were below it,
  it said go _lower_. The messages were completely inverted, making it impossible to narrow down
  the answer by following the hints.

  **5. String vs. integer comparison on even attempts**
  On every even-numbered attempt, the secret number was secretly converted to a string before being
  compared to your guess. This broke the comparison entirely — Python compares strings
  lexicographically, so `"15" > "8"` evaluates to `False` (because `"1"` comes before `"8"`).
  This caused the hints to flip unpredictably depending on which attempt you were on.

  ### 🔧 Fixes Applied
  - **Swapped Normal/Hard ranges** back to their correct values: Easy = 1–20, Normal = 1–50, Hard = 1–100.
  - **Fixed the New Game button** to use `random.randint(low, high)` so the new secret always
    respects the currently selected difficulty.
  - **Fixed the info banner** to display `{low}` and `{high}` dynamically instead of hardcoded values.
  - **Moved `check_guess` to `logic_utils.py`** and rewrote it to always cast both values to `int`
    before comparing, which eliminates the string comparison bug entirely.
  - **Corrected the hint messages** so "Too High" now says "Go LOWER" and "Too Low" says "Go HIGHER".
  - **Added a FIXME comment** on the string-cast block in `app.py` to flag it as a known remaining
    issue for future cleanup.
  - All fixes were validated with pytest — **10/10 tests passing**.

## 📸 Demo

- [x] [Insert a screenshot of your fixed, winning game here]

![alt text](<Screenshot 2026-03-08 at 1.23.09 PM.png>)

![alt text](<Screenshot 2026-03-08 at 1.22.48 PM-1.png>)

## 🚀 Stretch Features

- [x] Challenge 1
      ![alt text](<Screenshot 2026-03-14 at 10.06.29 PM.png>)

- [ ] [If you choose to complete Challenge 4, insert a screenshot of your Enhanced Game UI here]
