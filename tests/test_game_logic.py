from logic_utils import (
    check_guess,
    get_range_for_difficulty,
    parse_guess,
    update_score,
)

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == "Too Low"

def test_hint_direction_not_swapped():
    # Bug: a high guess said "Go HIGHER" and a low guess said "Go LOWER"
    outcome, message = check_guess(100, 50)
    assert outcome == "Too High"
    assert "LOWER" in message

    outcome, message = check_guess(0, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message

def test_string_secret_compared_numerically():
    # Bug: on even attempts the secret was a str, so "100" < "50" lexicographically
    outcome, message = check_guess(100, "50")
    assert outcome == "Too High"
    assert "LOWER" in message

    outcome, message = check_guess(9, "50")
    assert outcome == "Too Low"
    assert "HIGHER" in message

def test_harder_difficulty_has_wider_range():
    # Bug: Hard (1-50) had a smaller range than Normal (1-100)
    _, easy_high = get_range_for_difficulty("Easy")
    _, normal_high = get_range_for_difficulty("Normal")
    _, hard_high = get_range_for_difficulty("Hard")
    assert easy_high < normal_high < hard_high

def test_wrong_guess_always_loses_points():
    # Bug: "Too High" on an even attempt added 5 points instead of subtracting
    assert update_score(50, "Too High", 2) == 45
    assert update_score(50, "Too High", 3) == 45
    assert update_score(50, "Too Low", 2) == 45

def test_first_guess_win_scores_full_points():
    # Bug: off-by-one meant a first-guess win scored 80 instead of 100
    assert update_score(0, "Win", 1) == 100
    assert update_score(0, "Win", 2) == 90
    assert update_score(0, "Win", 50) == 10

def test_out_of_range_guess_rejected():
    # Bug: 0 and other out-of-range guesses were accepted
    ok, value, err = parse_guess("0", 1, 100)
    assert not ok and value is None and "between 1 and 100" in err

    ok, _, _ = parse_guess("101", 1, 100)
    assert not ok

    assert parse_guess("1", 1, 100) == (True, 1, None)
    assert parse_guess("100", 1, 100) == (True, 100, None)

def test_non_integer_guess_rejected():
    for raw in ["abc", "3.7", "5.0", "", None]:
        ok, value, _ = parse_guess(raw, 1, 100)
        assert not ok and value is None

def test_score_never_negative():
    assert update_score(0, "Too High", 1) == 0
    assert update_score(3, "Too Low", 1) == 0
