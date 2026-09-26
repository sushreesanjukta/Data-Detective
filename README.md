# Data Detective 🔍

## About

**Data Detective** is a desktop mystery game built entirely in Python and Tkinter. You play as a data analyst turned detective: a confidential company file has disappeared, and it's up to you to investigate employee records, cross-reference clues, and use simple data-analysis techniques (filtering, searching, comparing) to identify who deleted it.

It was built as a beginner/intermediate portfolio project to demonstrate practical Python skills — working with data structures, writing clean functions, building a GUI, and applying basic data-analysis logic — in a format that's more fun to show off than a plain script.

## Features

- 🕵️ **5 unique fictional cases** (Missing Sales Dataset, Stolen Customer Report, Deleted Attendance Records, Fake Transaction Investigation, Missing Financial Report), chosen at random each playthrough
- 🎚️ **3 difficulty levels** — Easy (3 suspects / 3 clues), Medium (4 suspects / 5 clues), Hard (5 suspects / 7 clues including a red herring)
- 📋 **Suspect profiles** with employee ID, department, role, login/logout times, location, access level, and recent activity
- 🔍 **Evidence tab** with clue cards tied directly to the underlying data
- 📊 **Data Analysis dashboard** — filter suspects by department, find who was active during the incident, find high-access employees, search by employee ID, compare login/logout times, and check who matches every clue at once
- 📝 **Notes tab** for jotting down your own reasoning
- 💡 **Progressive hint system** (costs points)
- 🚨 **Accusation system** with a full right/wrong outcome and explanation
- 🏆 **Scoring & ranking system** — Rookie → Junior → Data Detective → Master Data Detective
- 📄 **Save Investigation Report** — exports your final case report as a `.txt` file
- 🎨 Clean dark-themed UI designed to look like a detective + data-analytics dashboard
- ✅ **Every case is logic-verified** — a test script (`test_logic.py`) confirms all 5 cases are solvable at all 3 difficulty levels before you ever open the app

## Technologies Used

- Python 3
- Tkinter (GUI, including `ttk.Notebook` for tabs and `ttk.Combobox` for filters)
- `random` (case selection)
- `time` (investigation timer and fast-solve bonus)

No external libraries, database, or internet connection required.

## Project Structure

```
Data-Detective/
│
├── main.py          # Entry point — run this file to play
├── game_logic.py     # Case setup, clue filtering, data analysis, scoring
├── cases.py           # All 5 case files: suspects, clues, and solutions
├── ui.py               # All Tkinter screens and widgets
├── test_logic.py       # Automated checks that every case is solvable
├── README.md
└── assets/             # Place screenshots or icons here
```

## How to Run

```bash
git clone <repository-url>
cd Data-Detective
python main.py
```

Requires only a standard Python 3 installation (Tkinter ships with most Python installers by default). If you're on Linux and get a `No module named tkinter` error, install it with:

```bash
sudo apt-get install python3-tk
```

### Running the tests

Before playing, you can verify the game logic yourself:

```bash
python test_logic.py
```

This checks all 5 cases across all 3 difficulty levels and confirms each one narrows down to exactly one correct suspect.

## How to Play

1. From the main menu, click **Start Investigation** and choose a difficulty.
2. A random case loads with a short description of the incident.
3. Investigate using the dashboard tabs:
   - **📋 Suspects** — read each employee's profile.
   - **🔍 Evidence** — review every clue in the case.
   - **📊 Data Analysis** — run filters (department, access level, activity, employee ID search) to narrow down the suspect list yourself.
   - **📝 Notes** — write down your reasoning.
4. Use **💡 Hint** if you get stuck (this costs points).
5. When you're confident, go to **🚨 Accusation**, select a suspect, and click **MAKE ACCUSATION**.
6. See your Investigation Report with your score, accuracy, time taken, and detective rank. Save it as a `.txt` file if you'd like to keep it.

## How to Customize / Add New Cases

Every case lives in `cases.py` as a plain dictionary — no other file needs to change to add a new one.

A case needs:

- `case_id`, `title`, `description`, `incident_window`, `culprit` (the correct suspect's name)
- `suspects`: a list of suspect dictionaries. Give each suspect the standard fields (`name`, `employee_id`, `department`, `role`, `login`, `logout`, `location_during_incident`, `access`, `recent_activity`) plus boolean "clue attributes" (e.g. `active_during_incident`, `high_access`, `entered_server_room`, `id_ends_47`, `suspicious_file_access`, `suspicious_search`). **The culprit should be `True` on every clue attribute**; every innocent suspect should be `False` on at least one.
- `clues`: a list of clue dictionaries, each with an `id`, a display `text`, and an `attribute` matching one of the suspect boolean fields above (or `"red_herring": True` for flavor-only clues that don't eliminate anyone).
- `difficulty_setup`: which suspect names and clue ids are used for `"Easy"`, `"Medium"`, and `"Hard"`.
- `explanation`: the closing sentence shown in the final report.

Once you add a new case dictionary, append it to the `ALL_CASES` list at the bottom of `cases.py`, then run `python test_logic.py` to confirm it's solvable at every difficulty before playing it.

## GitHub Upload Steps

```bash
cd Data-Detective
git init
git add .
git commit -m "Initial commit: Data Detective game"
git branch -M main
git remote add origin <your-repository-url>
git push -u origin main
```

## Screenshots

*(Add your own screenshots here after running the game — see suggestions below.)*

- `assets/welcome_screen.png` — the main menu
- `assets/difficulty_screen.png` — difficulty selection cards
- `assets/dashboard_suspects.png` — the Suspects tab with employee cards
- `assets/dashboard_analysis.png` — the Data Analysis tab mid-filter
- `assets/case_solved.png` — the final Investigation Report on a correct accusation

## Future Improvements

- Sound effects for accusations and hints
- More cases and a case editor UI
- Online leaderboard
- Database integration for persistent player stats
- More advanced data-analysis visualizations (charts of access levels, timelines)
- AI-generated cases for infinite replayability

## Author

Created by [Your Name]
