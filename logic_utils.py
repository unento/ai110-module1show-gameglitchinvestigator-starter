def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    # FIX: AI flagged during the refactor that Hard (1-50) was easier than
    # Normal; I approved the fix and the AI chose 1-200.
    if difficulty == "Hard":
        return 1, 200
    return 1, 100


def parse_guess(raw: str, low: int | None = None, high: int | None = None):
    """
    Parse user input into an int guess, rejecting values outside [low, high].

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    # FIX: I decided only whole numbers count as valid; AI removed the
    # float conversion that silently turned "3.7" into 3.
    try:
        value = int(raw)
    except ValueError:
        return False, None, "That is not a whole number."

    # FIX: I noticed 0 was accepted as a guess; AI added this bounds check
    # and passed the difficulty's range in from app.py.
    if low is not None and high is not None and not low <= value <= high:
        return False, None, f"Guess must be between {low} and {high}."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    # FIX: I reported wrong hints at 0 and 100; AI traced it to a str secret
    # being compared as text, so both values are now compared as ints.
    guess = int(guess)
    secret = int(secret)

    if guess == secret:
        return "Win", "🎉 Correct!"
    # FIX: AI found the hint messages were swapped between these branches;
    # I had it move check_guess into logic_utils.py and fix them in agent mode.
    if guess > secret:
        return "Too High", "📉 Go LOWER!"
    return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """
    Update score based on outcome and attempt number.

    attempt_number is 1-based: a win on the first guess earns 100 points,
    minus 10 per extra guess (minimum 10). Every wrong guess costs 5,
    but the score never drops below 0.
    """
    # FIX: AI spotted an off-by-one that gave a first-guess win 80 points;
    # I asked it to fix it so a first-guess win scores 100.
    if outcome == "Win":
        points = 100 - 10 * (attempt_number - 1)
        if points < 10:
            points = 10
        return current_score + points

    # FIX: AI flagged that "Too High" added 5 points on even attempts; I
    # kept the -5 penalty for every wrong guess and added the floor at 0.
    if outcome in ("Too High", "Too Low"):
        return max(0, current_score - 5)

    return current_score
