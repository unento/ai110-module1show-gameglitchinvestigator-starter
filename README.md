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
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [ ] Describe the game's purpose.
- [ ] Detail which bugs you found.
- [ ] Explain what fixes you applied.

## 📸 Demo Walkthrough

A sample game on **Normal** difficulty (range 1–100, 8 attempts). The secret number for this game is **63**.

1. User starts the app with `python -m streamlit run app.py`. The game shows "Guess a number between 1 and 100. Attempts left: 8". Score is 0.
2. User enters `abc` → the game shows "That is not a whole number." No attempt is used.
3. User enters a guess of 40 → "📈 Go HIGHER!" (Too Low). Attempts used: 1. The score stays at 0, because a wrong guess costs 5 points but the score can't drop below 0.
4. User enters a guess of 70 → "📉 Go LOWER!" (Too High). Attempts used: 2. Score: 0.
5. User enters 150 → "Guess must be between 1 and 100." No attempt is used.
6. User enters a guess of 55 → "📈 Go HIGHER!" (Too Low). Attempts used: 3. Score: 0.
7. User enters a guess of 63 → "🎉 Correct!", balloons appear, and the game shows "You won! The secret was 63. Final score: 70". A first-guess win is worth 100 points, minus 10 for each extra guess, so a win on attempt 4 earns 70.
8. User clicks Submit again → "You already won. Start a new game to play again." The game ignores further guesses.
9. User clicks **New Game 🔁** → a new secret is picked, and attempts, score and guess history all reset. No page refresh is needed.
10. User switches the difficulty to **Hard** → a new game starts automatically with the range 1–200 and 5 attempts.

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
# Paste your pytest output here, e.g.:
# pytest tests/
# ========================= X passed in 0.XXs =========================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
