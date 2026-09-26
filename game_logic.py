"""
game_logic.py
-------------
This file contains all the "brains" of the game: picking a random case,
setting up suspects/clues for a chosen difficulty, filtering suspects using
clues, running the data-analysis tools, and calculating the score/rank.

No tkinter code lives here on purpose - this file could be tested and reused
completely on its own (for example, from test_logic.py).
"""

import random
from cases import ALL_CASES, GENERIC_HINTS


# ---------------------------------------------------------------------------
# CASE SETUP
# ---------------------------------------------------------------------------

def pick_random_case():
    """Return one random case dictionary from cases.py."""
    return random.choice(ALL_CASES)


def get_suspects_for_case(case, difficulty):
    """
    Return the list of suspect dictionaries that should be used for the
    given difficulty ("Easy", "Medium", or "Hard").
    """
    names_for_difficulty = case["difficulty_setup"][difficulty]["suspects"]
    all_suspects = case["suspects"]

    # Keep only the suspects whose name is in this difficulty's suspect list.
    selected = [s for s in all_suspects if s["name"] in names_for_difficulty]
    return selected


def get_clues_for_case(case, difficulty):
    """
    Return the list of clue dictionaries that should be shown for the given
    difficulty ("Easy", "Medium", or "Hard").
    """
    clue_ids_for_difficulty = case["difficulty_setup"][difficulty]["clues"]
    all_clues = case["clues"]

    selected = [c for c in all_clues if c["id"] in clue_ids_for_difficulty]
    return selected


# ---------------------------------------------------------------------------
# CLUE FILTERING (the actual detective logic)
# ---------------------------------------------------------------------------

def suspect_matches_clue(suspect, clue):
    """
    Check whether one suspect matches one clue.

    Every real clue has an "attribute" field naming a key in the suspect
    dictionary that should be True for the guilty suspect (for example,
    "high_access" or "entered_server_room"). Red-herring clues have
    attribute=None and are treated as flavor text that does not eliminate
    anyone.
    """
    if clue.get("red_herring"):
        return True  # Red herrings never eliminate a suspect.

    attribute = clue["attribute"]
    return bool(suspect.get(attribute, False))


def get_matching_suspects(suspects, clues):
    """
    Given a list of suspects and a list of clues, return only the suspects
    who match EVERY clue. In a well-formed case, this list will contain
    exactly one suspect: the real culprit.
    """
    matching = []
    for suspect in suspects:
        if all(suspect_matches_clue(suspect, clue) for clue in clues):
            matching.append(suspect)
    return matching


def clues_matched_by_suspect(suspect, clues):
    """Return the list of clue ids that this suspect actually matches."""
    return [clue["id"] for clue in clues if suspect_matches_clue(suspect, clue)]


# ---------------------------------------------------------------------------
# DATA ANALYSIS TOOLS (the "Data Analyst" part of the portfolio project)
# ---------------------------------------------------------------------------

def filter_by_department(suspects, department):
    """Return suspects who belong to the given department (case-insensitive)."""
    department = department.strip().lower()
    return [s for s in suspects if s["department"].lower() == department]


def filter_active_during_incident(suspects):
    """Return suspects who were active/present during the incident window."""
    return [s for s in suspects if s["active_during_incident"]]


def filter_high_access(suspects):
    """Return suspects with High data access."""
    return [s for s in suspects if s["access"] == "High"]


def search_by_employee_id(suspects, partial_id):
    """Return suspects whose employee ID contains the given text."""
    partial_id = partial_id.strip().lower()
    return [s for s in suspects if partial_id in s["employee_id"].lower()]


def find_unusual_activity(suspects):
    """
    Return suspects whose 'recent_activity' looks unusual/suspicious.
    We treat any suspect who entered the server room OR accessed the file
    right before it disappeared as showing unusual activity.
    """
    return [
        s for s in suspects
        if s["entered_server_room"] or s["suspicious_file_access"]
    ]


def compare_login_logout(suspects):
    """
    Return a simple list of (name, login, logout) tuples, useful for
    displaying a comparison table in the UI.
    """
    return [(s["name"], s["login"], s["logout"]) for s in suspects]


# ---------------------------------------------------------------------------
# HINT SYSTEM
# ---------------------------------------------------------------------------

def get_hint(hint_index):
    """
    Return the hint text for the given index (0-based).
    If there are no more hints, return None.
    """
    if 0 <= hint_index < len(GENERIC_HINTS):
        return GENERIC_HINTS[hint_index]
    return None


# ---------------------------------------------------------------------------
# SCORING SYSTEM
# ---------------------------------------------------------------------------

# Point values used throughout the game - kept in one place so they are easy
# to tune.
POINTS_CORRECT_ACCUSATION = 100
POINTS_PER_CLUE_REVIEWED = 10
POINTS_WRONG_ACCUSATION = -50
POINTS_PER_HINT_USED = -10
BONUS_FAST_SOLVE_SECONDS = 90   # Solve within this many seconds for a bonus.
BONUS_FAST_SOLVE_POINTS = 20


def calculate_final_score(clues_reviewed_count, hints_used, accusation_correct,
                           seconds_taken):
    """
    Calculate the final detective score using the rules described in the
    project brief. Returns an integer score.
    """
    score = 0
    score += clues_reviewed_count * POINTS_PER_CLUE_REVIEWED
    score += hints_used * POINTS_PER_HINT_USED

    if accusation_correct:
        score += POINTS_CORRECT_ACCUSATION
        if seconds_taken <= BONUS_FAST_SOLVE_SECONDS:
            score += BONUS_FAST_SOLVE_POINTS
    else:
        score += POINTS_WRONG_ACCUSATION

    # Never let the score go below zero - it just feels bad in a report.
    return max(score, 0)


def calculate_accuracy(clues_reviewed_count, total_clues, accusation_correct):
    """
    Return an accuracy percentage (0-100) combining how many clues were
    actually reviewed with whether the final accusation was correct.
    """
    if total_clues == 0:
        clue_accuracy = 0
    else:
        clue_accuracy = (clues_reviewed_count / total_clues) * 100

    accusation_bonus = 100 if accusation_correct else 0

    # Average the two so both investigation effort and the final answer count.
    accuracy = (clue_accuracy + accusation_bonus) / 2
    return round(min(accuracy, 100))


def get_rank(score):
    """Return the detective rank title for a given score."""
    if score >= 150:
        return "Master Data Detective"
    elif score >= 100:
        return "Data Detective"
    elif score >= 50:
        return "Junior Detective"
    else:
        return "Rookie Detective"
