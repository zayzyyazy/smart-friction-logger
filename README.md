# Smart Friction Logger

A local CLI tool for tracking and understanding the small friction events that slow down your workflow — slow pipelines, repeated blockers, confusing tooling. Log them fast, spot the patterns, and get AI-generated suggestions on what to fix.

---

## Why I Built It

I kept running into the same annoyances at the terminal and losing track of what was actually costing me the most time. I wanted a way to log these moments quickly — without opening a browser or switching apps — and then see a weekly summary of what kept coming up. This project is that tool.

---

## Core Features

- **Quick logging** — describe a friction event in plain text; OpenAI structures it into a title, description, category, and severity score (1–5)
- **Local JSONL storage** — every event is saved as a JSON line in `data/logs/`; no database, no cloud
- **Pattern detection** — identifies recurring categories and frequently mentioned keywords across your logs
- **Weekly reports** — generates a Markdown report saved to `reports/weekly/`, including an AI-written insights section with suggested actions
- **Flexible CLI** — interactive menu or direct flags (`--log`, `--patterns`, `--report`)
- **Terminal aliases** — `frictionlog`, `frictionreport`, `frictionpatterns` for quick access from anywhere
- **Mac Automator launcher** — log events without opening a terminal window

> Logs and generated reports are kept local and are excluded from Git via `.gitignore`.

---

## How It Works

1. You run `python3 main.py --log` (or use the `frictionlog` alias)
2. You pick a category and describe the friction in plain text
3. The input is sent to the OpenAI API, which returns a structured record: title, description, category, and severity
4. The record is saved as a line in `data/logs/friction_log.jsonl`
5. When you run `--report`, the app reads all logs, analyses patterns, sends a summary to OpenAI for insights, and writes a weekly Markdown report to `reports/weekly/`

---

## Tech Stack

| Layer | Tool |
|---|---|
| Language | Python 3.8+ |
| AI enrichment | OpenAI API (GPT) |
| Storage | JSONL flat files |
| Config | python-dotenv |
| CLI | sys.argv / argparse |

---

## Project Structure

```
smart-friction-logger/
├── main.py               # Entry point — run this
├── requirements.txt      # Python dependencies
├── COMMANDS.md           # Full command and alias reference
├── src/
│   ├── logger.py         # Collects raw friction input from the user
│   ├── storage.py        # Reads and writes local log and report files
│   ├── patterns.py       # Detects recurring categories and keywords
│   ├── insights.py       # Calls OpenAI to enrich events and generate insights
│   └── utils.py          # Shared helpers (timestamps, IDs, paths)
├── data/
│   └── logs/             # Raw event logs in JSONL format (gitignored)
└── reports/
    └── weekly/           # Generated weekly reports in Markdown (gitignored)
```

---

## How to Run Locally

**Requirements:** Python 3.8+, an OpenAI API key

```bash
# 1. Clone the repo
git clone https://github.com/your-username/smart-friction-logger.git
cd smart-friction-logger

# 2. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add your OpenAI API key
echo "OPENAI_API_KEY=your-key-here" > .env

# 5. Run the app
python3 main.py
```

---

## Example Commands

```bash
# Interactive menu (choose log / patterns / report)
python3 main.py

# Log a new friction event
python3 main.py --log

# View detected patterns across all logs
python3 main.py --patterns

# Generate and save this week's report
python3 main.py --report
```

If you set up the terminal aliases from `COMMANDS.md`:

```bash
frictionlog        # log a new event
frictionpatterns   # view patterns
frictionreport     # generate weekly report
```

> See [COMMANDS.md](COMMANDS.md) for the full reference including alias setup, troubleshooting, and git shortcuts.

---

## Example Workflow

```
$ frictionlog

Category: tooling
Describe the friction: The dev container takes 4 minutes to rebuild every time I switch branches.

Analysing with OpenAI...

--- Structured Report ---
  Title:       Slow dev container rebuild on branch switch
  Category:    tooling
  Severity:    4 / 5
  Description: Dev container rebuild takes ~4 minutes on each branch switch,
               interrupting flow and adding significant wait time per session.
-------------------------

$ frictionreport

Generating AI insights...
Weekly report generated successfully!
Saved to: reports/weekly/2026-03-20.md
```

The saved report includes a frequency table of categories, a keyword summary, and an AI-generated "What to do about it" section.

---

## What I Learned

- How to use the OpenAI API for structured data extraction from free-form text
- How to design a CLI tool with both an interactive menu and direct flag-based entry points
- How to store and query append-only JSONL logs without a database
- How to keep personal data (logs, reports) out of version control with `.gitignore`
- How to wire up terminal aliases and a Mac Automator launcher for frictionless access to a tool I actually use daily

---

## Future Improvements

- Add a `--since` flag to filter logs by date range before generating a report
- Support multiple log files (one per day) and auto-merge for pattern analysis
- Export reports to PDF or send a weekly digest by email
- Add a simple tag system (`#deploy`, `#meeting`) for more granular filtering
- Build a lightweight web view to browse logs and reports in a browser
