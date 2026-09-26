"""
ui.py
-----
All the tkinter GUI code lives here. game_logic.py and cases.py do the
"thinking" - this file is only responsible for drawing screens and reacting
to button clicks.

The app is built as one class, DataDetectiveApp, which owns a single root
window and swaps out "screen" frames as the player moves through the game:

    Welcome -> How to Play
            -> Difficulty Select -> Dashboard (Suspects / Evidence /
               Analysis / Notes / Accusation) -> Report -> (restart)
"""

import time
import tkinter as tk
from tkinter import ttk, messagebox

import game_logic as gl
from cases import ALL_CASES

# ---------------------------------------------------------------------------
# COLOR THEME - dark "detective + data analytics" look
# ---------------------------------------------------------------------------
BG_DARK = "#12161f"
BG_PANEL = "#1b2130"
BG_CARD = "#232a3d"
ACCENT = "#e0a72c"       # detective gold
ACCENT_2 = "#4fb0ff"     # data-analytics blue
TEXT_MAIN = "#f2f2f2"
TEXT_MUTED = "#9aa3b5"
GOOD = "#5bd18a"
BAD = "#e0605c"

FONT_TITLE = ("Georgia", 26, "bold")
FONT_HEADING = ("Segoe UI", 16, "bold")
FONT_BODY = ("Segoe UI", 11)
FONT_BODY_BOLD = ("Segoe UI", 11, "bold")
FONT_SMALL = ("Segoe UI", 9)
FONT_MONO = ("Consolas", 11)


class DataDetectiveApp:
    """The main application class - one instance runs the whole game."""

    def __init__(self, root):
        self.root = root
        self.root.title("Data Detective")
        self.root.geometry("1000x700")
        self.root.minsize(900, 620)
        self.root.configure(bg=BG_DARK)

        # ---- Game state (reset every new game via self.reset_game_state) ----
        self.case = None
        self.difficulty = "Medium"
        self.suspects = []
        self.clues = []
        self.clues_reviewed = set()   # ids of clues the player has opened
        self.hints_used = 0
        self.hint_index = 0
        self.notes_text_widget = None
        self.start_time = None
        self.last_report = ""

        # Container that holds whichever "screen" frame is currently visible.
        self.container = tk.Frame(self.root, bg=BG_DARK)
        self.container.pack(fill="both", expand=True)

        self.show_welcome_screen()

    # -----------------------------------------------------------------
    # SCREEN MANAGEMENT HELPERS
    # -----------------------------------------------------------------
    def clear_container(self):
        """Remove every widget currently shown so a new screen can be drawn."""
        for widget in self.container.winfo_children():
            widget.destroy()

    def reset_game_state(self):
        self.case = None
        self.suspects = []
        self.clues = []
        self.clues_reviewed = set()
        self.hints_used = 0
        self.hint_index = 0
        self.start_time = None

    # -----------------------------------------------------------------
    # SCREEN 1: WELCOME
    # -----------------------------------------------------------------
    def show_welcome_screen(self):
        self.clear_container()

        wrapper = tk.Frame(self.container, bg=BG_DARK)
        wrapper.pack(expand=True)

        tk.Label(wrapper, text="🔍 DATA DETECTIVE", font=FONT_TITLE,
                 fg=ACCENT, bg=BG_DARK).pack(pady=(40, 5))
        tk.Label(wrapper, text="Can you solve the case?", font=FONT_BODY,
                 fg=TEXT_MUTED, bg=BG_DARK).pack(pady=(0, 40))

        button_style = {
            "font": FONT_HEADING, "width": 22, "height": 1,
            "bg": BG_CARD, "fg": TEXT_MAIN, "activebackground": ACCENT,
            "activeforeground": BG_DARK, "bd": 0, "cursor": "hand2",
        }

        tk.Button(wrapper, text="🕵️  Start Investigation", **button_style,
                  command=self.show_difficulty_screen).pack(pady=8)
        tk.Button(wrapper, text="📖  How to Play", **button_style,
                  command=self.show_how_to_play_screen).pack(pady=8)
        tk.Button(wrapper, text="🚪  Exit", **button_style,
                  command=self.root.quit).pack(pady=8)

        tk.Label(wrapper, text="A Python + Tkinter portfolio project",
                 font=FONT_SMALL, fg=TEXT_MUTED, bg=BG_DARK).pack(pady=(50, 0))

    # -----------------------------------------------------------------
    # SCREEN 2: HOW TO PLAY
    # -----------------------------------------------------------------
    def show_how_to_play_screen(self):
        self.clear_container()

        wrapper = tk.Frame(self.container, bg=BG_DARK)
        wrapper.pack(fill="both", expand=True, padx=40, pady=30)

        tk.Label(wrapper, text="📖 How to Play", font=FONT_HEADING,
                 fg=ACCENT, bg=BG_DARK).pack(anchor="w", pady=(0, 15))

        instructions = (
            "You are a Data Detective. A company file has been deleted, and "
            "several employees are suspects.\n\n"
            "1. Open the Suspects tab to review each employee's profile.\n"
            "2. Open the Evidence tab to read every clue in the case.\n"
            "3. Use the Data Analysis tab to filter and cross-check suspects "
            "(by department, access level, activity during the incident, and "
            "employee ID).\n"
            "4. Write down your reasoning in the Notes tab.\n"
            "5. When you are confident, go to the Accusation tab and select "
            "the suspect you believe is guilty.\n\n"
            "Careful - a wrong accusation costs points, and using hints "
            "costs points too. Solve it fast and correctly for the highest "
            "detective rank!"
        )
        tk.Label(wrapper, text=instructions, font=FONT_BODY, fg=TEXT_MAIN,
                 bg=BG_DARK, justify="left", wraplength=880).pack(anchor="w")

        tk.Button(wrapper, text="⬅ Back", font=FONT_BODY_BOLD, bg=BG_CARD,
                  fg=TEXT_MAIN, bd=0, cursor="hand2", padx=20, pady=8,
                  command=self.show_welcome_screen).pack(anchor="w", pady=30)

    # -----------------------------------------------------------------
    # SCREEN 3: DIFFICULTY SELECT
    # -----------------------------------------------------------------
    def show_difficulty_screen(self):
        self.clear_container()

        wrapper = tk.Frame(self.container, bg=BG_DARK)
        wrapper.pack(expand=True)

        tk.Label(wrapper, text="Choose Your Difficulty", font=FONT_HEADING,
                 fg=ACCENT, bg=BG_DARK).pack(pady=(30, 25))

        levels = [
            ("🟢 Easy", "Easy", "3 suspects, 3 clues - a gentle first case."),
            ("🟡 Medium", "Medium", "4 suspects, 5 clues - some misleading info."),
            ("🔴 Hard", "Hard", "5-6 suspects, 7+ clues, includes red herrings."),
        ]

        for label, value, description in levels:
            card = tk.Frame(wrapper, bg=BG_CARD, padx=20, pady=14)
            card.pack(pady=8, fill="x", padx=60)

            tk.Label(card, text=label, font=FONT_BODY_BOLD, fg=TEXT_MAIN,
                     bg=BG_CARD).pack(anchor="w")
            tk.Label(card, text=description, font=FONT_SMALL, fg=TEXT_MUTED,
                     bg=BG_CARD).pack(anchor="w", pady=(2, 8))
            tk.Button(card, text=f"Play {value}", font=FONT_BODY_BOLD,
                      bg=BG_DARK, fg=ACCENT, bd=0, cursor="hand2", padx=14,
                      pady=6, command=lambda v=value: self.start_new_case(v)
                      ).pack(anchor="w")

        tk.Button(wrapper, text="⬅ Back", font=FONT_BODY_BOLD, bg=BG_CARD,
                  fg=TEXT_MAIN, bd=0, cursor="hand2", padx=20, pady=8,
                  command=self.show_welcome_screen).pack(pady=20)

    # -----------------------------------------------------------------
    # STARTING A CASE
    # -----------------------------------------------------------------
    def start_new_case(self, difficulty):
        """Pick a random case, set it up for the chosen difficulty, and
        move to the investigation dashboard."""
        self.reset_game_state()
        self.difficulty = difficulty
        self.case = gl.pick_random_case()
        self.suspects = gl.get_suspects_for_case(self.case, difficulty)
        self.clues = gl.get_clues_for_case(self.case, difficulty)
        self.start_time = time.time()

        self.show_dashboard_screen()

    # -----------------------------------------------------------------
    # SCREEN 4: INVESTIGATION DASHBOARD (tabs)
    # -----------------------------------------------------------------
    def show_dashboard_screen(self):
        self.clear_container()

        # ---- Top case banner ----
        banner = tk.Frame(self.container, bg=BG_PANEL)
        banner.pack(fill="x")

        tk.Label(banner, text=f"CASE #{self.case['case_id']}  —  {self.case['title']}",
                  font=FONT_HEADING, fg=ACCENT, bg=BG_PANEL
                  ).pack(side="left", padx=20, pady=12)
        tk.Label(banner, text=f"Difficulty: {self.difficulty}", font=FONT_BODY,
                 fg=TEXT_MUTED, bg=BG_PANEL).pack(side="right", padx=20)

        desc = tk.Label(self.container, text=self.case["description"],
                         font=FONT_BODY, fg=TEXT_MAIN, bg=BG_DARK,
                         justify="left", wraplength=960)
        desc.pack(fill="x", padx=20, pady=(10, 5))

        # ---- Tabs (Notebook) ----
        style = ttk.Style()
        style.theme_use("default")
        style.configure("TNotebook", background=BG_DARK, borderwidth=0)
        style.configure("TNotebook.Tab", background=BG_CARD, foreground=TEXT_MAIN,
                        padding=[14, 8], font=FONT_BODY_BOLD)
        style.map("TNotebook.Tab", background=[("selected", ACCENT)],
                  foreground=[("selected", BG_DARK)])

        notebook = ttk.Notebook(self.container)
        notebook.pack(fill="both", expand=True, padx=15, pady=10)

        suspects_tab = tk.Frame(notebook, bg=BG_DARK)
        evidence_tab = tk.Frame(notebook, bg=BG_DARK)
        analysis_tab = tk.Frame(notebook, bg=BG_DARK)
        notes_tab = tk.Frame(notebook, bg=BG_DARK)
        accusation_tab = tk.Frame(notebook, bg=BG_DARK)

        notebook.add(suspects_tab, text="📋 Suspects")
        notebook.add(evidence_tab, text="🔍 Evidence")
        notebook.add(analysis_tab, text="📊 Data Analysis")
        notebook.add(notes_tab, text="📝 Notes")
        notebook.add(accusation_tab, text="🚨 Accusation")

        self.build_suspects_tab(suspects_tab)
        self.build_evidence_tab(evidence_tab)
        self.build_analysis_tab(analysis_tab)
        self.build_notes_tab(notes_tab)
        self.build_accusation_tab(accusation_tab)

        # ---- Bottom bar: hint button + quit to menu ----
        bottom = tk.Frame(self.container, bg=BG_DARK)
        bottom.pack(fill="x", pady=(0, 10), padx=15)

        tk.Button(bottom, text="💡 Hint (-10 pts)", font=FONT_BODY_BOLD,
                  bg=BG_CARD, fg=ACCENT, bd=0, cursor="hand2", padx=14, pady=6,
                  command=self.use_hint).pack(side="left")

        tk.Button(bottom, text="🏠 Quit to Menu", font=FONT_BODY, bg=BG_DARK,
                  fg=TEXT_MUTED, bd=0, cursor="hand2",
                  command=self.confirm_quit_to_menu).pack(side="right")

    def confirm_quit_to_menu(self):
        if messagebox.askyesno("Quit Investigation",
                                "Leave this case and return to the main menu?"):
            self.show_welcome_screen()

    # ---- Tab: Suspects ----------------------------------------------
    def build_suspects_tab(self, parent):
        canvas_frame = tk.Frame(parent, bg=BG_DARK)
        canvas_frame.pack(fill="both", expand=True, padx=10, pady=10)

        for suspect in self.suspects:
            card = tk.Frame(canvas_frame, bg=BG_CARD, padx=14, pady=10)
            card.pack(fill="x", pady=6)

            header = f"{suspect['name']}  —  {suspect['role']} ({suspect['department']})"
            tk.Label(card, text=header, font=FONT_BODY_BOLD, fg=ACCENT_2,
                     bg=BG_CARD).pack(anchor="w")

            details = (
                f"Employee ID: {suspect['employee_id']}   |   "
                f"Access Level: {suspect['access']}\n"
                f"Login: {suspect['login']}   Logout: {suspect['logout']}   |   "
                f"Location during incident: {suspect['location_during_incident']}\n"
                f"Recent activity: {suspect['recent_activity']}"
            )
            tk.Label(card, text=details, font=FONT_BODY, fg=TEXT_MAIN,
                     bg=BG_CARD, justify="left").pack(anchor="w", pady=(4, 0))

    # ---- Tab: Evidence -------------------------------------------------
    def build_evidence_tab(self, parent):
        wrapper = tk.Frame(parent, bg=BG_DARK)
        wrapper.pack(fill="both", expand=True, padx=10, pady=10)

        tk.Label(wrapper, text=f"Incident window: {self.case['incident_window']}",
                 font=FONT_BODY_BOLD, fg=TEXT_MUTED, bg=BG_DARK).pack(anchor="w",
                                                                       pady=(0, 8))

        for i, clue in enumerate(self.clues, start=1):
            card = tk.Frame(wrapper, bg=BG_CARD, padx=14, pady=10)
            card.pack(fill="x", pady=5)

            tag = " (possibly irrelevant)" if clue.get("red_herring") else ""
            tk.Label(card, text=f"🔎 Evidence #{i}{tag}", font=FONT_BODY_BOLD,
                     fg=ACCENT, bg=BG_CARD).pack(anchor="w")
            tk.Label(card, text=clue["text"], font=FONT_BODY, fg=TEXT_MAIN,
                     bg=BG_CARD, justify="left", wraplength=880
                     ).pack(anchor="w", pady=(2, 0))

            # Mark this clue as "reviewed" the moment its card is built,
            # since the player can see it as soon as they open this tab.
            self.clues_reviewed.add(clue["id"])

    # ---- Tab: Data Analysis --------------------------------------------
    def build_analysis_tab(self, parent):
        wrapper = tk.Frame(parent, bg=BG_DARK)
        wrapper.pack(fill="both", expand=True, padx=10, pady=10)

        # --- Controls row ---
        controls = tk.Frame(wrapper, bg=BG_DARK)
        controls.pack(fill="x", pady=(0, 10))

        tk.Label(controls, text="Filter by department:", font=FONT_BODY,
                 fg=TEXT_MAIN, bg=BG_DARK).grid(row=0, column=0, sticky="w",
                                                 padx=(0, 6))
        departments = sorted(set(s["department"] for s in self.suspects))
        dept_var = tk.StringVar(value=departments[0] if departments else "")
        dept_menu = ttk.Combobox(controls, textvariable=dept_var,
                                  values=departments, state="readonly", width=15)
        dept_menu.grid(row=0, column=1, padx=(0, 10))

        tk.Button(controls, text="Filter", font=FONT_BODY_BOLD, bg=BG_CARD,
                  fg=ACCENT, bd=0, cursor="hand2", padx=10,
                  command=lambda: self.run_analysis("department", dept_var.get())
                  ).grid(row=0, column=2, padx=(0, 20))

        tk.Label(controls, text="Search Employee ID:", font=FONT_BODY,
                 fg=TEXT_MAIN, bg=BG_DARK).grid(row=0, column=3, sticky="w",
                                                 padx=(0, 6))
        id_var = tk.StringVar()
        id_entry = tk.Entry(controls, textvariable=id_var, width=14)
        id_entry.grid(row=0, column=4, padx=(0, 10))
        tk.Button(controls, text="Search", font=FONT_BODY_BOLD, bg=BG_CARD,
                  fg=ACCENT, bd=0, cursor="hand2", padx=10,
                  command=lambda: self.run_analysis("id", id_var.get())
                  ).grid(row=0, column=5)

        # --- Quick-action buttons ---
        quick_actions = tk.Frame(wrapper, bg=BG_DARK)
        quick_actions.pack(fill="x", pady=(0, 10))

        quick_buttons = [
            ("Active during incident", lambda: self.run_analysis("active", None)),
            ("High access employees", lambda: self.run_analysis("high_access", None)),
            ("Unusual activity", lambda: self.run_analysis("unusual", None)),
            ("Compare login/logout", lambda: self.run_analysis("compare", None)),
            ("Suspects matching ALL clues", lambda: self.run_analysis("all_clues", None)),
        ]
        for text, cmd in quick_buttons:
            tk.Button(quick_actions, text=text, font=FONT_SMALL, bg=BG_CARD,
                      fg=TEXT_MAIN, bd=0, cursor="hand2", padx=8, pady=4,
                      command=cmd).pack(side="left", padx=4)

        # --- Results box ---
        tk.Label(wrapper, text="Results:", font=FONT_BODY_BOLD, fg=ACCENT_2,
                 bg=BG_DARK).pack(anchor="w")

        self.analysis_output = tk.Text(wrapper, height=16, bg=BG_PANEL,
                                        fg=TEXT_MAIN, font=FONT_MONO, bd=0,
                                        wrap="word")
        self.analysis_output.pack(fill="both", expand=True, pady=(4, 0))
        self.analysis_output.insert("1.0", "Run a filter above to see results here.")
        self.analysis_output.config(state="disabled")

    def run_analysis(self, mode, value):
        """Runs one of the data-analysis operations and prints the result."""
        lines = []

        if mode == "department":
            results = gl.filter_by_department(self.suspects, value or "")
            lines.append(f"Employees in '{value}' department: {len(results)}\n")
            for s in results:
                lines.append(f"  - {s['name']} ({s['role']})")

        elif mode == "id":
            results = gl.search_by_employee_id(self.suspects, value or "")
            lines.append(f"Employees matching ID search '{value}': {len(results)}\n")
            for s in results:
                lines.append(f"  - {s['name']} ({s['employee_id']})")

        elif mode == "active":
            results = gl.filter_active_during_incident(self.suspects)
            lines.append(f"Employees active during incident: {len(results)}\n")
            for s in results:
                lines.append(f"  - {s['name']} (login {s['login']} - logout {s['logout']})")

        elif mode == "high_access":
            results = gl.filter_high_access(self.suspects)
            lines.append(f"High access employees: {len(results)}\n")
            for s in results:
                lines.append(f"  - {s['name']} ({s['access']} access)")

        elif mode == "unusual":
            results = gl.find_unusual_activity(self.suspects)
            lines.append(f"Employees with unusual activity: {len(results)}\n")
            for s in results:
                lines.append(f"  - {s['name']}: {s['recent_activity']}")

        elif mode == "compare":
            results = gl.compare_login_logout(self.suspects)
            lines.append("Login / Logout comparison:\n")
            for name, login, logout in results:
                lines.append(f"  - {name:10s} login {login}   logout {logout}")

        elif mode == "all_clues":
            matches = gl.get_matching_suspects(self.suspects, self.clues)
            lines.append(f"Employees matching all clues: {len(matches)}\n")
            for s in matches:
                lines.append(f"  - {s['name']}")
            if len(matches) == 1:
                lines.append(f"\nPossible suspect:\n  {matches[0]['name']}")

        else:
            lines.append("Unknown analysis type.")

        self.analysis_output.config(state="normal")
        self.analysis_output.delete("1.0", "end")
        self.analysis_output.insert("1.0", "\n".join(lines))
        self.analysis_output.config(state="disabled")

    # ---- Tab: Notes ------------------------------------------------------
    def build_notes_tab(self, parent):
        wrapper = tk.Frame(parent, bg=BG_DARK)
        wrapper.pack(fill="both", expand=True, padx=10, pady=10)

        tk.Label(wrapper, text="Write your detective notes here:",
                 font=FONT_BODY_BOLD, fg=ACCENT_2, bg=BG_DARK).pack(anchor="w")

        self.notes_text_widget = tk.Text(wrapper, bg=BG_PANEL, fg=TEXT_MAIN,
                                          font=FONT_BODY, wrap="word", bd=0)
        self.notes_text_widget.pack(fill="both", expand=True, pady=(6, 0))

    # ---- Tab: Accusation ---------------------------------------------
    def build_accusation_tab(self, parent):
        wrapper = tk.Frame(parent, bg=BG_DARK)
        wrapper.pack(fill="both", expand=True, padx=10, pady=10)

        tk.Label(wrapper, text="Who do you believe is responsible?",
                 font=FONT_BODY_BOLD, fg=ACCENT_2, bg=BG_DARK).pack(anchor="w",
                                                                     pady=(0, 10))

        self.accusation_var = tk.StringVar(value="")
        for suspect in self.suspects:
            tk.Radiobutton(wrapper, text=f"{suspect['name']} ({suspect['role']})",
                            variable=self.accusation_var, value=suspect["name"],
                            font=FONT_BODY, fg=TEXT_MAIN, bg=BG_DARK,
                            selectcolor=BG_CARD, activebackground=BG_DARK,
                            activeforeground=TEXT_MAIN
                            ).pack(anchor="w", pady=3)

        tk.Button(wrapper, text="🚨 MAKE ACCUSATION", font=FONT_HEADING,
                  bg=ACCENT, fg=BG_DARK, bd=0, cursor="hand2", padx=16, pady=8,
                  command=self.make_accusation).pack(pady=25)

    # -----------------------------------------------------------------
    # HINTS
    # -----------------------------------------------------------------
    def use_hint(self):
        hint = gl.get_hint(self.hint_index)
        if hint is None:
            messagebox.showinfo("No More Hints", "There are no more hints for this case.")
            return

        self.hints_used += 1
        self.hint_index += 1
        messagebox.showinfo("💡 Hint", hint)

    # -----------------------------------------------------------------
    # ACCUSATION HANDLING
    # -----------------------------------------------------------------
    def make_accusation(self):
        accused_name = self.accusation_var.get()
        if not accused_name:
            messagebox.showwarning("No Suspect Selected",
                                    "Please select a suspect before making an accusation.")
            return

        is_correct = (accused_name == self.case["culprit"])
        accused_suspect = next(s for s in self.suspects if s["name"] == accused_name)

        seconds_taken = int(time.time() - self.start_time) if self.start_time else 0
        score = gl.calculate_final_score(
            clues_reviewed_count=len(self.clues_reviewed),
            hints_used=self.hints_used,
            accusation_correct=is_correct,
            seconds_taken=seconds_taken,
        )
        accuracy = gl.calculate_accuracy(
            clues_reviewed_count=len(self.clues_reviewed),
            total_clues=len(self.clues),
            accusation_correct=is_correct,
        )
        rank = gl.get_rank(score)

        if is_correct:
            matched_clue_ids = gl.clues_matched_by_suspect(accused_suspect, self.clues)
            self.show_result_screen(
                success=True, accused_name=accused_name, score=score,
                accuracy=accuracy, rank=rank, seconds_taken=seconds_taken,
                matched_clue_ids=matched_clue_ids,
            )
        else:
            self.show_result_screen(
                success=False, accused_name=accused_name, score=score,
                accuracy=accuracy, rank=rank, seconds_taken=seconds_taken,
                matched_clue_ids=[],
            )

    # -----------------------------------------------------------------
    # SCREEN 5: RESULT / REPORT
    # -----------------------------------------------------------------
    def show_result_screen(self, success, accused_name, score, accuracy, rank,
                            seconds_taken, matched_clue_ids):
        self.clear_container()

        wrapper = tk.Frame(self.container, bg=BG_DARK)
        wrapper.pack(expand=True, fill="both", padx=40, pady=30)

        if success:
            tk.Label(wrapper, text="🎉 CASE SOLVED!", font=FONT_TITLE,
                     fg=GOOD, bg=BG_DARK).pack(pady=(10, 15))
        else:
            tk.Label(wrapper, text="❌ WRONG SUSPECT", font=FONT_TITLE,
                     fg=BAD, bg=BG_DARK).pack(pady=(10, 15))
            explanation = (
                f"{accused_name} is innocent. The evidence does not fully "
                f"line up - review the clues again in the Evidence and "
                f"Data Analysis tabs."
            )
            tk.Label(wrapper, text=explanation, font=FONT_BODY, fg=TEXT_MAIN,
                     bg=BG_DARK, wraplength=880, justify="left").pack(pady=(0, 15))

        minutes = seconds_taken // 60
        seconds = seconds_taken % 60
        time_str = f"{minutes:02d}:{seconds:02d}"

        report_lines = [
            "════════════════════════════",
            "      INVESTIGATION REPORT",
            "════════════════════════════",
            "",
            f"Case: #{self.case['case_id']}",
            f"Case Type: {self.case['title']}",
            f"Difficulty: {self.difficulty}",
            "",
            f"Suspect Identified: {accused_name}",
            "",
        ]

        if success:
            report_lines.append("Evidence Matched:")
            for clue in self.clues:
                if clue["id"] in matched_clue_ids or clue.get("red_herring"):
                    mark = "✓" if clue["id"] in matched_clue_ids else "•"
                    report_lines.append(f"  {mark} {clue['text']}")
            report_lines.append("")
            report_lines.append(f"Explanation: {self.case['explanation']}")
        else:
            report_lines.append(f"Correct Suspect: {self.case['culprit']}")
            report_lines.append(f"Explanation: {self.case['explanation']}")

        report_lines += [
            "",
            f"Final Score: {score}",
            f"Accuracy: {accuracy}%",
            f"Time Taken: {time_str}",
            "",
            "Detective Rank:",
            f"{rank.upper()}",
            "",
            "════════════════════════════",
        ]
        self.last_report = "\n".join(report_lines)

        report_box = tk.Text(wrapper, height=18, bg=BG_PANEL, fg=TEXT_MAIN,
                              font=FONT_MONO, bd=0, wrap="word")
        report_box.pack(fill="both", expand=True, pady=(0, 15))
        report_box.insert("1.0", self.last_report)
        report_box.config(state="disabled")

        button_row = tk.Frame(wrapper, bg=BG_DARK)
        button_row.pack(fill="x")

        button_style = {
            "font": FONT_BODY_BOLD, "bg": BG_CARD, "fg": TEXT_MAIN, "bd": 0,
            "cursor": "hand2", "padx": 14, "pady": 8,
        }

        if not success:
            tk.Button(button_row, text="🔎 Keep Investigating", **button_style,
                      command=self.show_dashboard_screen).pack(side="left", padx=4)

        tk.Button(button_row, text="📄 Save Investigation Report", **button_style,
                  command=self.save_report_to_file).pack(side="left", padx=4)
        tk.Button(button_row, text="🔁 New Case", **button_style,
                  command=self.show_difficulty_screen).pack(side="left", padx=4)
        tk.Button(button_row, text="🏠 Main Menu", **button_style,
                  command=self.show_welcome_screen).pack(side="left", padx=4)

    # -----------------------------------------------------------------
    # SAVE REPORT
    # -----------------------------------------------------------------
    def save_report_to_file(self):
        filename = f"investigation_report_case_{self.case['case_id']}.txt"
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(self.last_report)
            messagebox.showinfo("Report Saved", f"Report saved as '{filename}' "
                                                  f"in the current folder.")
        except OSError as error:
            messagebox.showerror("Save Failed", f"Could not save the report:\n{error}")


def run_app():
    """Create the root window and start the Data Detective game."""
    root = tk.Tk()
    app = DataDetectiveApp(root)
    root.mainloop()
