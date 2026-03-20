# Smart Friction Logger

A local, CLI-based tool for recording and understanding daily friction events —
the small annoyances, blockers, and repeated pain points in your workflow.
No web app, no database, no cloud. Just Python and plain local files.

---

## What is it?

You run the app from your terminal, describe a friction event (e.g. "slow deploy pipeline again"),
and the logger saves it locally. Over time it detects recurring patterns and produces
a plain-text weekly insight report so you can spot what's actually slowing you down.

---

## MVP Scope

- [x] Project scaffold (folders, modules, entry point)
- [x] Log a friction event interactively (category, description, severity, timestamp)
- [x] Save events as JSON lines in `data/logs/`
- [x] Detect simple recurring patterns (same category / keyword frequency)
- [x] Generate a weekly plain-text report saved to `reports/weekly/`

---

## Folder Structure

```
smart-friction-logger/
├── main.py               # Entry point — run this
├── requirements.txt      # Python dependencies
├── src/
│   ├── __init__.py
│   ├── logger.py         # Captures friction events from the user
│   ├── storage.py        # Reads/writes local log files
│   ├── patterns.py       # Detects recurring friction themes
│   ├── insights.py       # Generates weekly reports
│   └── utils.py          # Shared helpers (timestamps, paths, etc.)
├── data/
│   ├── logs/             # Raw daily log files (JSON lines)
│   └── processed/        # Logs moved here after analysis
├── reports/
│   └── weekly/           # Generated weekly insight reports
└── tests/                # Unit tests for each module
```

---

## Setup

```bash
# 1. Create a virtual environment
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
python3 main.py
```

---

## Planned Future Steps

1. **Interactive logger** — prompt for event description, category, and severity
2. **Daily log files** — one JSON-lines file per day in `data/logs/`
3. **Pattern detection** — count recurring categories and keywords week-over-week
4. **Weekly reports** — human-readable Markdown/text summary saved to `reports/weekly/`
5. **CLI menu** — choose between "log event", "show patterns", "generate report"
6. **Optional tagging** — add free-form tags to events for richer filtering
