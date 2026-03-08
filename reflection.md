# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

---When I started the game, I chose Easy difficulty, and this option says Range 1 to 20, but the instructions says "Guess a number between 1 and 100**,"** so I realized that the difficulty doesn't change the range.

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
  --Claude.
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- What the AI suggested me:
  --Claude suggested me that we can fix a bug with the lower an high number validation, cause it has a bug and was hardcoded.
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
  -- Claude always suggested me the correct answer also, after Claude fix the error I validated change per change before accept all the changes.

- How you verified the result in the code or game:
  -- With the test cases that Claude help me and playing the game many times.

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
  -- Running the testscases, and testing the game.
- Describe at least one test you ran (manual or using pytest) :
  -- Creating new games, playing in all the Difficultis, and verify the results with the hints too.
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?
  -- Yes Claude help me to design the test and also I asked for feedback and explanation for each test case that was added.

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
  -- Becasue Sreamlit doesn't keep the value on the variables.

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
  -- Streamlit always run the whole app.py so you need to use a session_state for keeping values that you will need to evaluate after.

- What change did you make that finally gave the game a stable secret number?

-- Fixing the check_guess , the game was more stable at the begining.

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  -- Always use a Plan Mode, so you can verifing the code before do the changes.
  - This could be a testing habit, a prompting strategy, or a way you used Git.
    -- yes.
- What is one thing you would do differently next time you work with AI on a coding task?

-- Ask to Clauder to review the whole code to get more context first, then try the app myself, after that, compares my bugs with the bugs that claude can find easily, and implement an action plan for fixing.

- In one or two sentences, describe how this project changed the way you think about AI generated code.

-- I'll use AI for some time, and I think AI help us to solve problems fastly, but we have to take the control always.
