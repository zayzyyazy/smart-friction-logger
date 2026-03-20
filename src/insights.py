"""
insights.py — OpenAI enrichment and (future) weekly report generation.

Current role:
  - enrich_with_openai(): takes raw user input and asks OpenAI to produce a
    structured friction report (title, description, category, severity 1-5).

Future role:
  - generate_weekly_report(): consume detected patterns and write a plain-text
    weekly summary to reports/weekly/.
"""

import os
from openai import OpenAI
from src.utils import parse_json_safely


def enrich_with_openai(category: str, raw_input: str) -> dict:
    """
    Send the user's raw category and issue description to OpenAI.

    Returns a dict with:
      - title       (str)  short title for the friction event
      - description (str)  improved, clearer version of the issue
      - category    (str)  cleaned / normalised category label
      - severity    (int)  1 (minor) to 5 (critical)

    Raises ValueError if the API key is missing or the response is unusable.
    """

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY is not set. "
            "Add it to your .env file and make sure python-dotenv is installed."
        )

    client = OpenAI(api_key=api_key)

    # The prompt tells the model exactly what shape of JSON we expect.
    prompt = f"""You are helping log a friction event — something that slowed someone down at work.

The user provided:
  Category: {category}
  Description: {raw_input}

Return ONLY a JSON object with these four fields:
  "title"       — a short, clear title (max 10 words)
  "description" — an improved, specific version of the user's description
  "category"    — a cleaned, lowercase single-word or short-phrase category label
  "severity"    — an integer from 1 (minor nuisance) to 5 (critical blocker)

Example output:
{{
  "title": "CI pipeline fails silently on merge",
  "description": "The CI pipeline fails without surfacing error logs, making it hard to diagnose broken builds.",
  "category": "tooling",
  "severity": 3
}}

Return only the JSON object — no extra text."""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type": "json_object"},  # guarantees valid JSON output
        messages=[
            {"role": "user", "content": prompt}
        ],
    )

    raw_json = response.choices[0].message.content
    result = parse_json_safely(raw_json)

    if result is None:
        raise ValueError(f"OpenAI returned something that isn't valid JSON:\n{raw_json}")

    # Make sure severity is an integer in the expected range.
    try:
        result["severity"] = int(result["severity"])
        result["severity"] = max(1, min(5, result["severity"]))
    except (KeyError, ValueError, TypeError):
        result["severity"] = 3  # default to middle if something is wrong

    return result


def generate_weekly_report(patterns: list) -> str:
    """Placeholder: will build and return a formatted weekly insight report string."""
    return ""
