"""
main.py — Entry point for the Smart Friction Logger CLI.

Run with:
    python3 main.py

Flow:
  1. Ask the user for a category and brief issue description
  2. Send that input to OpenAI for enrichment (title, description, category, severity)
  3. Save the structured result to data/logs/friction_log.jsonl
  4. Print a confirmation with the saved record
"""

import sys
from dotenv import load_dotenv

# Load OPENAI_API_KEY (and any other vars) from .env before importing src modules.
load_dotenv()

from src.logger import log_event
from src.insights import enrich_with_openai
from src.storage import save_event
from src.utils import current_timestamp, unique_id


def main():
    print("Smart Friction Logger")
    print("---------------------")

    # Step 1 — collect raw input from the user
    raw = log_event()

    # Step 2 — send to OpenAI and get structured fields back
    print("\nAnalysing with OpenAI...")
    try:
        enriched = enrich_with_openai(raw["category"], raw["raw_input"])
    except ValueError as e:
        print(f"\nError: {e}")
        sys.exit(1)

    # Step 3 — build the full record that will be saved
    record = {
        "id":           unique_id(),
        "timestamp":    current_timestamp(),
        "raw_category": raw["category"],
        "raw_input":    raw["raw_input"],
        "title":        enriched.get("title", ""),
        "description":  enriched.get("description", ""),
        "category":     enriched.get("category", ""),
        "severity":     enriched.get("severity", 3),
    }

    # Step 4 — save to disk
    saved_path = save_event(record)

    # Step 5 — show the user what was saved
    print("\nFriction event logged successfully!")
    print(f"Saved to: {saved_path}\n")
    print("--- Structured Report ---")
    print(f"  ID:          {record['id']}")
    print(f"  Timestamp:   {record['timestamp']}")
    print(f"  Title:       {record['title']}")
    print(f"  Category:    {record['category']}")
    print(f"  Severity:    {record['severity']} / 5")
    print(f"  Description: {record['description']}")
    print("-------------------------")


if __name__ == "__main__":
    main()
