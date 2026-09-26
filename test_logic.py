"""
test_logic.py
-------------
A small, dependency-free test script that verifies the game logic BEFORE
the UI is built. Run it with:

    python test_logic.py

It checks, for every case and every difficulty level, that applying all of
that difficulty's clues to that difficulty's suspects leaves exactly ONE
suspect standing, and that this suspect is the correct culprit.

This is not a fancy test framework - just plain asserts, which is perfect
for a beginner-friendly portfolio project.
"""

from cases import ALL_CASES
from game_logic import (
    get_suspects_for_case,
    get_clues_for_case,
    get_matching_suspects,
    calculate_final_score,
    calculate_accuracy,
    get_rank,
)

DIFFICULTIES = ["Easy", "Medium", "Hard"]


def test_all_cases_are_solvable():
    failures = []

    for case in ALL_CASES:
        for difficulty in DIFFICULTIES:
            suspects = get_suspects_for_case(case, difficulty)
            clues = get_clues_for_case(case, difficulty)
            matches = get_matching_suspects(suspects, clues)

            match_names = [s["name"] for s in matches]

            if len(matches) != 1:
                failures.append(
                    f"[{case['title']} / {difficulty}] Expected exactly 1 match, "
                    f"got {len(matches)}: {match_names}"
                )
            elif matches[0]["name"] != case["culprit"]:
                failures.append(
                    f"[{case['title']} / {difficulty}] Matched wrong suspect: "
                    f"{matches[0]['name']} (expected {case['culprit']})"
                )
            else:
                print(f"OK  -> {case['title']:30s} [{difficulty:6s}] "
                      f"-> {matches[0]['name']} "
                      f"({len(suspects)} suspects, {len(clues)} clues)")

    if failures:
        print("\nFAILURES:")
        for f in failures:
            print(" -", f)
        raise AssertionError(f"{len(failures)} case/difficulty combos failed.")
    else:
        print("\nAll cases are solvable at all difficulties. Logic OK.")


def test_scoring():
    # Correct, fast, no hints -> should get full bonus.
    score = calculate_final_score(clues_reviewed_count=3, hints_used=0,
                                   accusation_correct=True, seconds_taken=30)
    assert score == 3 * 10 + 100 + 20, f"Unexpected score: {score}"

    # Wrong accusation should subtract 50 but never go negative overall in
    # this small example (3 clues * 10 = 30, minus 50 = -20 -> clamped to 0).
    score = calculate_final_score(clues_reviewed_count=3, hints_used=0,
                                   accusation_correct=False, seconds_taken=200)
    assert score == 0, f"Expected clamped score of 0, got {score}"

    # Rank thresholds.
    assert get_rank(0) == "Rookie Detective"
    assert get_rank(60) == "Junior Detective"
    assert get_rank(120) == "Data Detective"
    assert get_rank(150) == "Master Data Detective"

    # Accuracy should be between 0 and 100.
    acc = calculate_accuracy(clues_reviewed_count=5, total_clues=5, accusation_correct=True)
    assert acc == 100, f"Expected 100, got {acc}"

    print("Scoring logic OK.")


if __name__ == "__main__":
    test_all_cases_are_solvable()
    test_scoring()
