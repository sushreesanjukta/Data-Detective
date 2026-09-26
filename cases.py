"""
cases.py
--------
This file stores all the "case files" for the Data Detective game.

Each case is just a Python dictionary. A case contains:
    - basic info (id, title, description, incident time window)
    - a list of suspects (each suspect is a dictionary of attributes)
    - a list of clues (each clue is tied to one attribute of the suspects)
    - the name of the real culprit
    - a closing explanation shown in the final report
    - which suspects/clues are used for Easy / Medium / Hard difficulty

Why is it built this way?
--------------------------
Every clue in this game is a "filter": it checks ONE attribute on a suspect
(for example, "was this suspect active during the incident?"). The real
culprit is always designed to match EVERY clue. Every innocent suspect is
designed to fail at least one clue that is used at the chosen difficulty.

This guarantees that no matter which difficulty the player picks, applying
all the clues for that difficulty to the suspects for that difficulty will
always leave exactly ONE suspect standing: the real culprit.

(This claim is actually tested automatically in test_logic.py.)
"""

# ---------------------------------------------------------------------------
# CASE 1: Missing Sales Dataset
# ---------------------------------------------------------------------------
CASE_1 = {
    "case_id": "1042",
    "title": "Missing Sales Dataset",
    "description": (
        "At 8:45 PM, the company's confidential quarterly sales dataset "
        "vanished from the shared server. IT logs show the file was deleted, "
        "not just moved. Someone with real access wanted it gone."
    ),
    "incident_window": "19:00 - 20:00",
    "culprit": "Rahul",
    "suspects": [
        {
            "name": "Rahul", "employee_id": "EMP-2247", "department": "Sales",
            "role": "Sales Manager", "login": "09:10", "logout": "20:15",
            "location_during_incident": "Server Room",
            "access": "High", "recent_activity": "Opened sales_data.xlsx at 19:40, then deleted it",
            "active_during_incident": True, "high_access": True,
            "entered_server_room": True, "id_ends_47": True,
            "suspicious_file_access": True, "suspicious_search": True,
        },
        {
            "name": "Ananya", "employee_id": "EMP-1108", "department": "Sales",
            "role": "Sales Analyst", "login": "09:00", "logout": "17:30",
            "location_during_incident": "At home",
            "access": "Medium", "recent_activity": "Logged out before the incident window",
            "active_during_incident": False, "high_access": False,
            "entered_server_room": False, "id_ends_47": False,
            "suspicious_file_access": False, "suspicious_search": False,
        },
        {
            "name": "Priya", "employee_id": "EMP-3390", "department": "HR",
            "role": "HR Executive", "login": "09:15", "logout": "19:50",
            "location_during_incident": "Office - Floor 2",
            "access": "Medium", "recent_activity": "Reviewed leave applications",
            "active_during_incident": True, "high_access": False,
            "entered_server_room": False, "id_ends_47": False,
            "suspicious_file_access": False, "suspicious_search": False,
        },
        {
            "name": "Arjun", "employee_id": "EMP-4471", "department": "IT",
            "role": "Data Engineer", "login": "10:00", "logout": "20:30",
            "location_during_incident": "Server Room",
            "access": "High", "recent_activity": "Ran a routine server backup",
            "active_during_incident": True, "high_access": True,
            "entered_server_room": True, "id_ends_47": False,
            "suspicious_file_access": False, "suspicious_search": False,
        },
        {
            "name": "Sneha", "employee_id": "EMP-5547", "department": "Marketing",
            "role": "Marketing Executive", "login": "09:30", "logout": "19:55",
            "location_during_incident": "Server Room",
            "access": "High", "recent_activity": "Searched 'how to permanently delete a file'",
            "active_during_incident": True, "high_access": True,
            "entered_server_room": True, "id_ends_47": True,
            "suspicious_file_access": True, "suspicious_search": False,
        },
    ],
    "clues": [
        {"id": "C1", "text": "The deleted file was accessed between 19:00 and 20:00.",
         "attribute": "active_during_incident"},
        {"id": "C2", "text": "Only employees with High Data Access could delete the file.",
         "attribute": "high_access"},
        {"id": "C3", "text": "The security camera recorded someone entering the server room at 19:35.",
         "attribute": "entered_server_room"},
        {"id": "C4", "text": "IT confirms the employee's login ID ended with '47'.",
         "attribute": "id_ends_47"},
        {"id": "C5", "text": "The audit log shows sales_data.xlsx was opened right before it was deleted.",
         "attribute": "suspicious_file_access"},
        {"id": "C6", "text": "The browser history shows a search for ways to permanently erase files.",
         "attribute": "suspicious_search"},
        {"id": "RH1", "text": "A colleague mentioned the suspect seemed tired that day.",
         "attribute": None, "red_herring": True},
    ],
    "difficulty_setup": {
        "Easy":   {"suspects": ["Rahul", "Ananya", "Priya"], "clues": ["C1", "C2", "C3"]},
        "Medium": {"suspects": ["Rahul", "Ananya", "Priya", "Arjun"], "clues": ["C1", "C2", "C3", "C4", "C5"]},
        "Hard":   {"suspects": ["Rahul", "Ananya", "Priya", "Arjun", "Sneha"],
                   "clues": ["C1", "C2", "C3", "C4", "C5", "C6", "RH1"]},
    },
    "explanation": (
        "Rahul had High Data Access, entered the server room during the incident "
        "window, his employee ID ended in '47', and the audit log shows he opened "
        "and deleted the sales file himself."
    ),
}

# ---------------------------------------------------------------------------
# CASE 2: Stolen Customer Report
# ---------------------------------------------------------------------------
CASE_2 = {
    "case_id": "2093",
    "title": "Stolen Customer Report",
    "description": (
        "The customer database export, containing sensitive client contact "
        "details, was copied to an external drive and the original report was "
        "deleted from the shared drive at approximately 6:30 PM."
    ),
    "incident_window": "18:00 - 19:00",
    "culprit": "Vikram",
    "suspects": [
        {
            "name": "Vikram", "employee_id": "EMP-6647", "department": "IT",
            "role": "IT Support Engineer", "login": "08:45", "logout": "19:20",
            "location_during_incident": "Server Room",
            "access": "High", "recent_activity": "Plugged in a USB drive at 18:40, then deleted the report",
            "active_during_incident": True, "high_access": True,
            "entered_server_room": True, "id_ends_47": True,
            "suspicious_file_access": True, "suspicious_search": True,
        },
        {
            "name": "Meera", "employee_id": "EMP-7712", "department": "Customer Support",
            "role": "Support Executive", "login": "09:00", "logout": "17:45",
            "location_during_incident": "At home",
            "access": "Low", "recent_activity": "Logged out before the incident window",
            "active_during_incident": False, "high_access": False,
            "entered_server_room": False, "id_ends_47": False,
            "suspicious_file_access": False, "suspicious_search": False,
        },
        {
            "name": "Karan", "employee_id": "EMP-8801", "department": "Finance",
            "role": "Finance Executive", "login": "09:10", "logout": "18:50",
            "location_during_incident": "Office - Floor 1",
            "access": "Medium", "recent_activity": "Prepared monthly invoices",
            "active_during_incident": True, "high_access": False,
            "entered_server_room": False, "id_ends_47": False,
            "suspicious_file_access": False, "suspicious_search": False,
        },
        {
            "name": "Divya", "employee_id": "EMP-9047", "department": "Data",
            "role": "Data Analyst", "login": "10:00", "logout": "19:00",
            "location_during_incident": "Server Room",
            "access": "High", "recent_activity": "Reviewed dashboard metrics",
            "active_during_incident": True, "high_access": True,
            "entered_server_room": True, "id_ends_47": True,
            "suspicious_file_access": False, "suspicious_search": False,
        },
        {
            "name": "Rohit", "employee_id": "EMP-1147", "department": "Operations",
            "role": "Operations Executive", "login": "09:20", "logout": "18:55",
            "location_during_incident": "Server Room",
            "access": "High", "recent_activity": "Searched 'how to copy files to USB quickly'",
            "active_during_incident": True, "high_access": True,
            "entered_server_room": True, "id_ends_47": True,
            "suspicious_file_access": True, "suspicious_search": False,
        },
    ],
    "clues": [
        {"id": "C1", "text": "The customer report was last touched between 18:00 and 19:00.",
         "attribute": "active_during_incident"},
        {"id": "C2", "text": "Only employees with High Data Access could open the customer database.",
         "attribute": "high_access"},
        {"id": "C3", "text": "A security camera recorded someone entering the server room at 18:35.",
         "attribute": "entered_server_room"},
        {"id": "C4", "text": "IT confirms the employee's login ID ended with '47'.",
         "attribute": "id_ends_47"},
        {"id": "C5", "text": "A USB device was connected to the same computer right before the file vanished.",
         "attribute": "suspicious_file_access"},
        {"id": "C6", "text": "Browser history shows a search about copying files to a USB drive quickly.",
         "attribute": "suspicious_search"},
        {"id": "RH1", "text": "A suspect was seen arguing with a colleague earlier that morning.",
         "attribute": None, "red_herring": True},
    ],
    "difficulty_setup": {
        "Easy":   {"suspects": ["Vikram", "Meera", "Karan"], "clues": ["C1", "C2", "C3"]},
        "Medium": {"suspects": ["Vikram", "Meera", "Karan", "Divya"], "clues": ["C1", "C2", "C3", "C4", "C5"]},
        "Hard":   {"suspects": ["Vikram", "Meera", "Karan", "Divya", "Rohit"],
                   "clues": ["C1", "C2", "C3", "C4", "C5", "C6", "RH1"]},
    },
    "explanation": (
        "Vikram had High Data Access, was seen entering the server room during "
        "the incident window, his ID ended in '47', and logs confirm he plugged "
        "in a USB drive right before deleting the report."
    ),
}

# ---------------------------------------------------------------------------
# CASE 3: Deleted Attendance Records
# ---------------------------------------------------------------------------
CASE_3 = {
    "case_id": "3157",
    "title": "Deleted Attendance Records",
    "description": (
        "A month's worth of employee attendance records disappeared from the "
        "HR system right before payroll was due, at around 5:15 PM."
    ),
    "incident_window": "17:00 - 18:00",
    "culprit": "Neha",
    "suspects": [
        {
            "name": "Neha", "employee_id": "EMP-3347", "department": "HR",
            "role": "HR Manager", "login": "08:30", "logout": "18:10",
            "location_during_incident": "Server Room",
            "access": "High", "recent_activity": "Opened attendance_master.xlsx at 17:20, then deleted it",
            "active_during_incident": True, "high_access": True,
            "entered_server_room": True, "id_ends_47": True,
            "suspicious_file_access": True, "suspicious_search": True,
        },
        {
            "name": "Suresh", "employee_id": "EMP-4402", "department": "Admin",
            "role": "Admin Assistant", "login": "09:00", "logout": "16:30",
            "location_during_incident": "At home",
            "access": "Low", "recent_activity": "Logged out before the incident window",
            "active_during_incident": False, "high_access": False,
            "entered_server_room": False, "id_ends_47": False,
            "suspicious_file_access": False, "suspicious_search": False,
        },
        {
            "name": "Pooja", "employee_id": "EMP-5510", "department": "HR",
            "role": "HR Trainee", "login": "09:30", "logout": "17:45",
            "location_during_incident": "Office - Floor 3",
            "access": "Medium", "recent_activity": "Filed new joiner paperwork",
            "active_during_incident": True, "high_access": False,
            "entered_server_room": False, "id_ends_47": False,
            "suspicious_file_access": False, "suspicious_search": False,
        },
        {
            "name": "Manish", "employee_id": "EMP-6647", "department": "IT",
            "role": "IT Engineer", "login": "09:00", "logout": "18:00",
            "location_during_incident": "Server Room",
            "access": "High", "recent_activity": "Fixed a printer connection issue",
            "active_during_incident": True, "high_access": True,
            "entered_server_room": True, "id_ends_47": True,
            "suspicious_file_access": False, "suspicious_search": False,
        },
        {
            "name": "Kavya", "employee_id": "EMP-7747", "department": "Payroll",
            "role": "Payroll Executive", "login": "09:15", "logout": "17:50",
            "location_during_incident": "Server Room",
            "access": "High", "recent_activity": "Searched 'how to recover a deleted spreadsheet'",
            "active_during_incident": True, "high_access": True,
            "entered_server_room": True, "id_ends_47": True,
            "suspicious_file_access": True, "suspicious_search": False,
        },
    ],
    "clues": [
        {"id": "C1", "text": "The attendance file was last touched between 17:00 and 18:00.",
         "attribute": "active_during_incident"},
        {"id": "C2", "text": "Only employees with High Data Access could edit the HR system.",
         "attribute": "high_access"},
        {"id": "C3", "text": "The security camera recorded someone entering the server room at 17:25.",
         "attribute": "entered_server_room"},
        {"id": "C4", "text": "IT confirms the employee's login ID ended with '47'.",
         "attribute": "id_ends_47"},
        {"id": "C5", "text": "The audit log shows attendance_master.xlsx was opened right before it was deleted.",
         "attribute": "suspicious_file_access"},
        {"id": "C6", "text": "Browser history shows a search about recovering deleted spreadsheets.",
         "attribute": "suspicious_search"},
        {"id": "RH1", "text": "A suspect mentioned feeling stressed about the payroll deadline.",
         "attribute": None, "red_herring": True},
    ],
    "difficulty_setup": {
        "Easy":   {"suspects": ["Neha", "Suresh", "Pooja"], "clues": ["C1", "C2", "C3"]},
        "Medium": {"suspects": ["Neha", "Suresh", "Pooja", "Manish"], "clues": ["C1", "C2", "C3", "C4", "C5"]},
        "Hard":   {"suspects": ["Neha", "Suresh", "Pooja", "Manish", "Kavya"],
                   "clues": ["C1", "C2", "C3", "C4", "C5", "C6", "RH1"]},
    },
    "explanation": (
        "Neha had High Data Access, entered the server room during the incident "
        "window, her ID ended in '47', and the audit log shows she opened and "
        "deleted the attendance file herself."
    ),
}

# ---------------------------------------------------------------------------
# CASE 4: Fake Transaction Investigation
# ---------------------------------------------------------------------------
CASE_4 = {
    "case_id": "4268",
    "title": "Fake Transaction Investigation",
    "description": (
        "Auditors discovered a batch of fake transactions inserted into the "
        "finance system, and the original transaction log was deleted around "
        "3:45 PM to hide the trail."
    ),
    "incident_window": "15:00 - 16:00",
    "culprit": "Aditya",
    "suspects": [
        {
            "name": "Aditya", "employee_id": "EMP-8847", "department": "Finance",
            "role": "Finance Executive", "login": "09:00", "logout": "16:30",
            "location_during_incident": "Server Room",
            "access": "High", "recent_activity": "Opened transactions_log.xlsx at 15:30, then deleted it",
            "active_during_incident": True, "high_access": True,
            "entered_server_room": True, "id_ends_47": True,
            "suspicious_file_access": True, "suspicious_search": True,
        },
        {
            "name": "Ritu", "employee_id": "EMP-9902", "department": "Finance",
            "role": "Accountant", "login": "09:15", "logout": "14:30",
            "location_during_incident": "At home",
            "access": "Medium", "recent_activity": "Logged out before the incident window",
            "active_during_incident": False, "high_access": False,
            "entered_server_room": False, "id_ends_47": False,
            "suspicious_file_access": False, "suspicious_search": False,
        },
        {
            "name": "Sameer", "employee_id": "EMP-1015", "department": "Audit",
            "role": "Internal Auditor", "login": "09:30", "logout": "15:50",
            "location_during_incident": "Office - Floor 4",
            "access": "Medium", "recent_activity": "Reviewed last quarter's audit trail",
            "active_during_incident": True, "high_access": False,
            "entered_server_room": False, "id_ends_47": False,
            "suspicious_file_access": False, "suspicious_search": False,
        },
        {
            "name": "Nisha", "employee_id": "EMP-2247", "department": "IT",
            "role": "Data Engineer", "login": "09:45", "logout": "16:00",
            "location_during_incident": "Server Room",
            "access": "High", "recent_activity": "Ran a scheduled database sync",
            "active_during_incident": True, "high_access": True,
            "entered_server_room": True, "id_ends_47": True,
            "suspicious_file_access": False, "suspicious_search": False,
        },
        {
            "name": "Yash", "employee_id": "EMP-3347", "department": "Compliance",
            "role": "Compliance Officer", "login": "09:00", "logout": "15:55",
            "location_during_incident": "Server Room",
            "access": "High", "recent_activity": "Searched 'how to alter transaction timestamps'",
            "active_during_incident": True, "high_access": True,
            "entered_server_room": True, "id_ends_47": True,
            "suspicious_file_access": True, "suspicious_search": False,
        },
    ],
    "clues": [
        {"id": "C1", "text": "The transaction log was last touched between 15:00 and 16:00.",
         "attribute": "active_during_incident"},
        {"id": "C2", "text": "Only employees with High Data Access could edit the finance system.",
         "attribute": "high_access"},
        {"id": "C3", "text": "The security camera recorded someone entering the server room at 15:20.",
         "attribute": "entered_server_room"},
        {"id": "C4", "text": "IT confirms the employee's login ID ended with '47'.",
         "attribute": "id_ends_47"},
        {"id": "C5", "text": "The audit log shows transactions_log.xlsx was opened right before it was deleted.",
         "attribute": "suspicious_file_access"},
        {"id": "C6", "text": "Browser history shows a search about altering transaction timestamps.",
         "attribute": "suspicious_search"},
        {"id": "RH1", "text": "A suspect had recently asked for a transfer to another department.",
         "attribute": None, "red_herring": True},
    ],
    "difficulty_setup": {
        "Easy":   {"suspects": ["Aditya", "Ritu", "Sameer"], "clues": ["C1", "C2", "C3"]},
        "Medium": {"suspects": ["Aditya", "Ritu", "Sameer", "Nisha"], "clues": ["C1", "C2", "C3", "C4", "C5"]},
        "Hard":   {"suspects": ["Aditya", "Ritu", "Sameer", "Nisha", "Yash"],
                   "clues": ["C1", "C2", "C3", "C4", "C5", "C6", "RH1"]},
    },
    "explanation": (
        "Aditya had High Data Access, entered the server room during the incident "
        "window, his ID ended in '47', and the audit log shows he opened and "
        "deleted the transaction log himself."
    ),
}

# ---------------------------------------------------------------------------
# CASE 5: Missing Financial Report
# ---------------------------------------------------------------------------
CASE_5 = {
    "case_id": "5389",
    "title": "Missing Financial Report",
    "description": (
        "The annual financial report, due for a board meeting the next morning, "
        "was deleted from the shared drive at approximately 9:10 PM."
    ),
    "incident_window": "21:00 - 22:00",
    "culprit": "Kabir",
    "suspects": [
        {
            "name": "Kabir", "employee_id": "EMP-4447", "department": "Finance",
            "role": "Senior Analyst", "login": "10:00", "logout": "21:40",
            "location_during_incident": "Server Room",
            "access": "High", "recent_activity": "Opened annual_report.xlsx at 21:15, then deleted it",
            "active_during_incident": True, "high_access": True,
            "entered_server_room": True, "id_ends_47": True,
            "suspicious_file_access": True, "suspicious_search": True,
        },
        {
            "name": "Tanvi", "employee_id": "EMP-5502", "department": "Finance",
            "role": "Junior Analyst", "login": "10:15", "logout": "20:00",
            "location_during_incident": "At home",
            "access": "Medium", "recent_activity": "Logged out before the incident window",
            "active_during_incident": False, "high_access": False,
            "entered_server_room": False, "id_ends_47": False,
            "suspicious_file_access": False, "suspicious_search": False,
        },
        {
            "name": "Farhan", "employee_id": "EMP-6610", "department": "IT",
            "role": "IT Admin", "login": "10:30", "logout": "21:30",
            "location_during_incident": "Office - Floor 1",
            "access": "Medium", "recent_activity": "Monitored server uptime dashboards",
            "active_during_incident": True, "high_access": False,
            "entered_server_room": False, "id_ends_47": False,
            "suspicious_file_access": False, "suspicious_search": False,
        },
        {
            "name": "Ishita", "employee_id": "EMP-7747", "department": "Data",
            "role": "Data Scientist", "login": "10:45", "logout": "21:50",
            "location_during_incident": "Server Room",
            "access": "High", "recent_activity": "Trained a forecasting model",
            "active_during_incident": True, "high_access": True,
            "entered_server_room": True, "id_ends_47": True,
            "suspicious_file_access": False, "suspicious_search": False,
        },
        {
            "name": "Varun", "employee_id": "EMP-8847", "department": "Operations",
            "role": "Operations Manager", "login": "10:00", "logout": "21:45",
            "location_during_incident": "Server Room",
            "access": "High", "recent_activity": "Searched 'how to shred a file permanently'",
            "active_during_incident": True, "high_access": True,
            "entered_server_room": True, "id_ends_47": True,
            "suspicious_file_access": True, "suspicious_search": False,
        },
    ],
    "clues": [
        {"id": "C1", "text": "The financial report was last touched between 21:00 and 22:00.",
         "attribute": "active_during_incident"},
        {"id": "C2", "text": "Only employees with High Data Access could open the report.",
         "attribute": "high_access"},
        {"id": "C3", "text": "The security camera recorded someone entering the server room at 21:20.",
         "attribute": "entered_server_room"},
        {"id": "C4", "text": "IT confirms the employee's login ID ended with '47'.",
         "attribute": "id_ends_47"},
        {"id": "C5", "text": "The audit log shows annual_report.xlsx was opened right before it was deleted.",
         "attribute": "suspicious_file_access"},
        {"id": "C6", "text": "Browser history shows a search about shredding a file permanently.",
         "attribute": "suspicious_search"},
        {"id": "RH1", "text": "A suspect was overheard complaining about working late.",
         "attribute": None, "red_herring": True},
    ],
    "difficulty_setup": {
        "Easy":   {"suspects": ["Kabir", "Tanvi", "Farhan"], "clues": ["C1", "C2", "C3"]},
        "Medium": {"suspects": ["Kabir", "Tanvi", "Farhan", "Ishita"], "clues": ["C1", "C2", "C3", "C4", "C5"]},
        "Hard":   {"suspects": ["Kabir", "Tanvi", "Farhan", "Ishita", "Varun"],
                   "clues": ["C1", "C2", "C3", "C4", "C5", "C6", "RH1"]},
    },
    "explanation": (
        "Kabir had High Data Access, entered the server room during the incident "
        "window, his ID ended in '47', and the audit log shows he opened and "
        "deleted the annual report himself."
    ),
}

# A list of every case in the game. new cases can be appended here.
ALL_CASES = [CASE_1, CASE_2, CASE_3, CASE_4, CASE_5]

# Progressive hints shown for ANY case, in order (general detective advice).
GENERIC_HINTS = [
    "Hint 1: Check who had access to the deleted file.",
    "Hint 2: Look at the employees who were active during the incident window.",
    "Hint 3: Compare access level, server room entry, and login ID together.",
    "Hint 4: One suspect matches almost every clue but not all of them. Keep checking.",
]
