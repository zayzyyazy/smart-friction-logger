"""
storage.py — Local file persistence.

Saves friction event records as JSON Lines (one JSON object per line) in:
  data/logs/friction_log.jsonl

Each record contains both the original user input and the OpenAI-enriched fields.
"""

import json
import os

# Path to the log file, relative to the project root.
LOG_FILE = os.path.join("data", "logs", "friction_log.jsonl")


def save_event(event: dict) -> str:
    """
    Append a friction event dict to the JSONL log file.
    Creates the file if it doesn't exist yet.
    Returns the path of the file that was written to.
    """
    # Make sure the data/logs/ directory exists.
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

    # Append the event as a single JSON line.
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(event) + "\n")

    return LOG_FILE


REPORTS_DIR = os.path.join("reports", "weekly")


def save_report(content: str, date_str: str) -> str:
    """
    Save a markdown report string to reports/weekly/weekly_report_<date>.md.
    Creates the directory if it doesn't exist.
    Returns the path of the saved file.
    """
    os.makedirs(REPORTS_DIR, exist_ok=True)
    file_path = os.path.join(REPORTS_DIR, f"weekly_report_{date_str}.md")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    return file_path


def load_events() -> list:
    """
    Read all friction events from the JSONL log file.
    Returns a list of dicts, or an empty list if the file doesn't exist.
    """
    if not os.path.exists(LOG_FILE):
        return []

    events = []
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:  # skip blank lines
                events.append(json.loads(line))

    return events
