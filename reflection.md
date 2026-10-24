# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- hints are incorrect on the lower bound (when inputting 0 still gives a hint of lower)
- restart game doesn't work, need to refresh page
- hints incorrect on top end as well (100 was incorrect, said go lower 99 was incorrect hint was go higher)

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| 50    | go lower hint     | go higher hint  |score: 0                |
| 25    | go lower hint     | go higher hint  |score: 5     (0:50)     |
| 70     | go lower hint    | go higher hint  |score: 0                |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.

I used Claude Code in agent mode inside VS Code. I described the bugs I saw while playing, had it point me to the relevant code, and then had it made the fixes and write tests while I reviewed each change.

**Correct suggestion: why the hints were wrong**
- **What the AI suggested:** I reported that a guess of 0 said "Go LOWER" and a guess of 100 said "Go HIGHER". The AI traced this to two causes. In `check_guess`, the hint messages were swapped between the "Too High" and "Too Low" branches. Separately, `app.py` turned the secret into a string on every even attempt, so the game compared numbers as text, where `"100" < "50"`. It moved `check_guess` into `logic_utils.py`, swapped the messages back and converted both values to `int` before comparing.
- **Correct or not:** Correct. Both causes were real, and fixing only the swapped messages would have left wrong hints on even attempts.
- **How I verified it:** I had the AI write pytest cases that target the bug directly. `test_hint_direction_not_swapped` checks that 100 against a secret of 50 says "LOWER" and 0 says "HIGHER". `test_string_secret_compared_numerically` passes the secret as the string `"50"` and checks that 100 is still "Too High" and 9 is still "Too Low". Both pass. In a playthrough, guessing 50 against a lower secret showed "Go LOWER!" as expected.

**Incorrect / misleading suggestion: why the test import failed**
- **What the AI suggested:** When `pytest` couldn't import `logic_utils` from the `tests` folder, the AI said the cause was Python's import path not including the repo root. It added a `pytest.ini` with `pythonpath = .` and explained ways to import from a parent folder.
- **Correct or not:** Misleading. The `pytest.ini` is a reasonable setting, but it wasn't the real problem. I suspected I wasn't using my virtual environment. When the AI checked, plain `pytest` was running from a separate global Python 3.12 install, not the project's `.venv` (which uses Python 3.14 and has the project's packages). The AI's own test runs had worked only because it happened to use `python -m pytest`, which hid the real problem.
- **How I verified it:** The AI ran `which python pytest`, which showed `python` and `pytest` coming from two different global installs. Then I activated the venv (`.\.venv\Scripts\Activate.ps1`) and ran `pytest`. The import worked and the tests ran normally. The takeaway was to check which interpreter is actually running before trusting an explanation about import paths.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

**How I decided a bug was really fixed.** I only counted a bug as fixed when two things agreed: a pytest test aimed at that exact bug passed, and the game itself behaved correctly. A test passing on its own wasn't enough. The hint bug, for example, had two causes, and a test that only checked the swapped messages would have passed while hints were still wrong on even attempts. For every fix I also checked that the code ran without errors and that the earlier tests still gave the same result.

**Tests I ran and what they showed.**

| Test | Bug it targets | What it showed |
|------|----------------|----------------|
| `test_hint_direction_not_swapped` | Hints backwards at 0 and 100 | 100 vs. 50 now says "LOWER" and 0 vs. 50 says "HIGHER" |
| `test_string_secret_compared_numerically` | Secret compared as text on even attempts | 100 vs. `"50"` is "Too High"; text comparison would have said "Too Low" |
| `test_harder_difficulty_has_wider_range` | Hard (1–50) was easier than Normal | Ranges now grow Easy < Normal < Hard |
| `test_wrong_guess_always_loses_points` | "Too High" added 5 points on even attempts | Every wrong guess now costs 5 |
| `test_first_guess_win_scores_full_points` | First-guess win scored 80 | First-guess win scores 100, then 90, down to a minimum of 10 |
| `test_out_of_range_guess_rejected` | 0 was accepted as a guess | 0 and 101 are rejected; 1 and 100 are accepted |
| `test_non_integer_guess_rejected` | `3.7` was quietly turned into 3 | `abc`, `3.7`, `5.0`, empty and `None` are all rejected |
| `test_score_never_negative` | Score could go below 0 | A wrong guess at 0 or 3 points leaves the score at 0 |

The current result is 8 passed, 3 failed. The 3 failures are the starter tests (`test_winning_guess`, `test_guess_too_high`, `test_guess_too_low`). They compare `check_guess(...)` to a plain string like `"Win"`, but the function returns a pair like `("Win", "🎉 Correct!")`. In every case the outcome part is correct, so the failures come from how the tests are written, not from a game bug.

**Manual / game testing.** For the bugs in `app.py` (restart and attempt counting), the AI drove the real app without a browser using Streamlit's built-in test runner (`AppTest`). In that playthrough:
- `abc`, `3.7` and `0` were rejected without using an attempt.
- Guessing 10 twice used two attempts.
- Running out of all 8 attempts ended the game with a score of 0 instead of −40.
- New Game reset attempts, score, status and history without a page refresh.
- Switching to Hard started a new game with a secret inside 1–200.

**How AI helped with tests.** The AI wrote each targeted test right after making the matching fix, with a comment naming the bug it guards against. That helped me see what each fix was actually supposed to change. It also explained why the 3 starter tests fail: they expect one value, but `check_guess` returns two. And it helped me find that my `pytest` command was running outside the project's virtual environment, which is why the import had looked broken.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
