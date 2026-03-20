"""
logger.py — Friction event capture.

Asks the user for the minimum information needed to log a friction event:
  1. Category  (e.g. "tooling", "process", "communication")
  2. A brief description of what went wrong

The raw input is returned as a dict and passed to insights.py for enrichment.
"""


def log_event() -> dict:
    """
    Prompt the user for a category and a brief issue description.
    Returns a dict with keys 'category' and 'raw_input'.
    """
    print("\n--- Log a Friction Event ---")

    category = input("Category (e.g. tooling, process, communication): ").strip()
    raw_input = input("Briefly describe the issue: ").strip()

    return {
        "category": category,
        "raw_input": raw_input,
    }
