"""
main.py — Entry point for the Smart Friction Logger CLI.

Run with:
    python3 main.py              → interactive menu
    python3 main.py --log        → immediately start logging a friction event
    python3 main.py --patterns   → immediately show pattern analysis
    python3 main.py --report     → immediately generate weekly report

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
from src.patterns import print_patterns, build_markdown_report, analyse_patterns
from src.insights import generate_ai_insights
from src.storage import save_report
from src.utils import today_str


def log_friction_event():
    """Collect, enrich, and save a new friction event."""
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


def generate_weekly_report():
    """Build and save the weekly markdown report, including AI insights."""
    date = today_str()

    # Read logs once and share the result with both the report builder and the AI call
    summary = analyse_patterns()

    if not summary:
        print("\nNo logs found. Log some friction events first!")
        return

    # Try to get AI insights — fall back gracefully if it fails
    print("\nGenerating AI insights...")
    ai_insights = None
    try:
        ai_insights = generate_ai_insights(summary)
        print("AI insights ready.")
    except Exception as e:
        print(f"  (AI insights unavailable: {e})")

    # Build and save the report
    report = build_markdown_report(date, summary=summary, ai_insights=ai_insights)
    saved_path = save_report(report, date)
    print("\nWeekly report generated successfully!")
    print(f"Saved to: {saved_path}\n")


def show_menu():
    """Display the interactive menu and handle the user's choice."""
    print("Smart Friction Logger")
    print("---------------------")
    print("1) Log a friction event")
    print("2) View patterns")
    print("3) Generate weekly report")
    print()

    choice = input("Select an option (1, 2, or 3): ").strip()

    if choice == "1":
        log_friction_event()
    elif choice == "2":
        print_patterns()
    elif choice == "3":
        generate_weekly_report()
    else:
        print("Invalid choice. Please run again and enter 1, 2, or 3.")


def main():
    # Check if a CLI argument was passed (sys.argv[0] is always the script name,
    # so sys.argv[1] is the first real argument, e.g. --log)
    if len(sys.argv) > 1:
        arg = sys.argv[1]

        if arg == "--log":
            # Skip the menu and go straight to logging a friction event
            log_friction_event()

        elif arg == "--patterns":
            # Skip the menu and go straight to pattern analysis
            print_patterns()

        elif arg == "--report":
            # Skip the menu and go straight to weekly report generation
            generate_weekly_report()

        else:
            # Unknown flag — let the user know what's valid
            print(f"Unknown argument: {arg}")
            print("Usage:")
            print("  python3 main.py            → interactive menu")
            print("  python3 main.py --log       → log a friction event")
            print("  python3 main.py --patterns  → view pattern analysis")
            print("  python3 main.py --report    → generate weekly report")
            sys.exit(1)

    else:
        # No argument provided — fall back to the interactive menu
        show_menu()


if __name__ == "__main__":
    main()
