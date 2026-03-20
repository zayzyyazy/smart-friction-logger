"""
patterns.py — Simple pattern detection for friction logs.

Reads all logged events and summarises:
  - Total log count
  - Entries grouped by category (count + average severity)
  - Most frequent keywords found in descriptions
"""

import json
import os
from collections import Counter

LOG_FILE = os.path.join("data", "logs", "friction_log.jsonl")

# Words to ignore when extracting keywords (too short or too common to be useful)
STOP_WORDS = {
    "the", "and", "for", "that", "with", "this", "from", "have", "not",
    "are", "was", "were", "but", "its", "can", "had", "has", "when",
    "then", "into", "also", "more", "very", "just", "been", "than",
    "too", "any", "all", "our",
}


def load_logs() -> list:
    """Read all entries from the JSONL log file."""
    if not os.path.exists(LOG_FILE):
        return []

    entries = []
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    entries.append(json.loads(line))
                except json.JSONDecodeError:
                    pass  # skip malformed lines
    return entries


def analyse_patterns() -> dict:
    """
    Read all logs and return a summary dict containing:
      - total: int
      - categories: {name: {count, avg_severity}}
      - top_keywords: [(word, count), ...]
    """
    entries = load_logs()

    if not entries:
        return {}

    total = len(entries)

    # --- Category breakdown ---
    category_counts = Counter()
    category_severity_sum = {}

    for entry in entries:
        cat = entry.get("category") or entry.get("raw_category") or "unknown"
        cat = cat.strip().lower()
        severity = entry.get("severity", 3)

        category_counts[cat] += 1
        category_severity_sum[cat] = category_severity_sum.get(cat, 0) + severity

    categories = {}
    for cat, count in category_counts.items():
        avg_sev = category_severity_sum[cat] / count
        categories[cat] = {"count": count, "avg_severity": round(avg_sev, 1)}

    # --- Keyword extraction ---
    word_counter = Counter()

    for entry in entries:
        text = entry.get("description", "") or entry.get("raw_input", "")
        for word in text.lower().split():
            # Strip punctuation from edges
            word = word.strip(".,!?;:\"'()[]{}")
            if len(word) >= 4 and word not in STOP_WORDS:
                word_counter[word] += 1

    top_keywords = word_counter.most_common(10)

    return {
        "total": total,
        "categories": categories,
        "top_keywords": top_keywords,
    }


def build_markdown_report(date_str: str, summary: dict = None, ai_insights: dict = None) -> str:
    """
    Build a weekly friction report as a markdown string.

    Parameters:
      date_str    — the date label for the report heading
      summary     — pre-computed pattern dict from analyse_patterns(); if None, it is computed here
      ai_insights — optional dict with keys: weekly_insight, patterns_observed, suggested_actions

    Returns the markdown text, or a short message if no logs exist.
    """
    if summary is None:
        summary = analyse_patterns()

    if not summary:
        return "# Weekly Friction Report\n\nNo logs found. Log some friction events first!\n"

    lines = []
    lines.append(f"# Weekly Friction Report — {date_str}\n")

    # Total
    lines.append(f"## Total Logs\n")
    lines.append(f"- **{summary['total']}** friction events recorded\n")

    # Categories
    lines.append(f"## Top Categories\n")
    sorted_cats = sorted(
        summary["categories"].items(),
        key=lambda x: x[1]["count"],
        reverse=True,
    )
    for cat, data in sorted_cats:
        lines.append(f"- **{cat}** — {data['count']} entries")

    lines.append("")

    # Severity
    lines.append(f"## Average Severity by Category\n")
    for cat, data in sorted_cats:
        lines.append(f"- **{cat}**: {data['avg_severity']} / 5")

    lines.append("")

    # Keywords
    lines.append(f"## Frequent Keywords\n")
    if summary["top_keywords"]:
        for word, count in summary["top_keywords"]:
            lines.append(f"- `{word}` ({count}x)")
    else:
        lines.append("- (no keywords found)")

    lines.append("")

    # Short rule-based summary
    lines.append(f"## Summary\n")
    top_cat, top_cat_data = sorted_cats[0]
    highest_sev_cat = max(sorted_cats, key=lambda x: x[1]["avg_severity"])
    top_keyword = summary["top_keywords"][0][0] if summary["top_keywords"] else None

    lines.append(f"- The most common friction category is **{top_cat}** ({top_cat_data['count']} entries).")
    lines.append(f"- The category with the highest average severity is **{highest_sev_cat[0]}** ({highest_sev_cat[1]['avg_severity']} / 5).")
    if top_keyword:
        lines.append(f"- The most frequent keyword in your logs is **{top_keyword}**.")

    lines.append("")

    # AI sections
    lines.append(f"## AI Weekly Insight\n")
    if ai_insights and ai_insights.get("weekly_insight"):
        lines.append(ai_insights["weekly_insight"])
    else:
        lines.append("AI insight could not be generated this time.")

    lines.append("")

    lines.append(f"## AI Observed Patterns\n")
    if ai_insights and ai_insights.get("patterns_observed"):
        for obs in ai_insights["patterns_observed"]:
            lines.append(f"- {obs}")
    else:
        lines.append("- (not available)")

    lines.append("")

    lines.append(f"## AI Suggested Actions\n")
    if ai_insights and ai_insights.get("suggested_actions"):
        for action in ai_insights["suggested_actions"]:
            lines.append(f"- {action}")
    else:
        lines.append("- (not available)")

    lines.append("")
    return "\n".join(lines)


def print_patterns():
    """Print a clean summary of detected patterns to the terminal."""
    summary = analyse_patterns()

    print("\n========== Friction Pattern Summary ==========\n")

    if not summary:
        print("No logs found. Log some friction events first!")
        print("\n==============================================\n")
        return

    # Total
    print(f"  Total logs: {summary['total']}\n")

    # Categories
    print("  --- Top Categories ---")
    sorted_cats = sorted(
        summary["categories"].items(),
        key=lambda x: x[1]["count"],
        reverse=True,
    )
    for cat, data in sorted_cats:
        bar = "#" * data["count"]
        print(f"  {cat:<20} {bar}  ({data['count']} entries, avg severity: {data['avg_severity']} / 5)")

    # Keywords
    print("\n  --- Frequent Keywords ---")
    if summary["top_keywords"]:
        for word, count in summary["top_keywords"]:
            print(f"  {word:<20} {count}x")
    else:
        print("  (no keywords found)")

    print("\n==============================================\n")
