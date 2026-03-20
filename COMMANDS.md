# Commands Reference

Quick reference for running and managing the Smart Friction Logger.

---

## Project Setup

```bash
# Create a virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## Running the App

```bash
# Launch the main menu (default)
python3 main.py

# Log a new friction event interactively
python3 main.py --log

# Show detected friction patterns
python3 main.py --patterns

# Generate a weekly insight report
python3 main.py --report
```

---

## Terminal Aliases

These shortcuts are set up in your shell config (`~/.zshrc`):

```bash
frictionlog        # Same as: python3 main.py --log
frictionreport     # Same as: python3 main.py --report
frictionpatterns   # Same as: python3 main.py --patterns
```

> You also have a Mac Automator app that launches logging without opening a terminal.

---

## Git Commands

```bash
# Check what files have changed
git status

# Stage all changes
git add .

# Commit with a message
git commit -m "your message here"

# Push to GitHub
git push

# Pull latest changes
git pull
```

---

## Troubleshooting

```bash
# Check your Python version (needs 3.8+)
python3 --version

# Confirm you're in the virtual environment
which python3

# Reinstall dependencies if something breaks
pip install -r requirements.txt --force-reinstall

# See recent log entries
cat data/logs/friction_log.jsonl

# List generated reports
ls reports/weekly/
```
