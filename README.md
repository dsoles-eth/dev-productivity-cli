# DevProductivity CLI

[![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![GitHub stars](https://img.shields.io/github/stars/dev-productivity/DevProductivity-CLI.svg)](https://github.com/dev-productivity/DevProductivity-CLI/stargazers)
[![PyPI version](https://badge.fury.io/py/dev-productivity-cli.svg)](https://badge.fury.io/py/dev-productivity-cli)

**DevProductivity CLI** is a comprehensive command-line interface tool designed to track development session times, categorize tasks, and analyze productivity patterns. Built for developers and engineering managers, it provides actionable insights into daily workflows using a robust Python backend with SQLite storage.

## Features

- **Session Tracking**: Start, pause, and stop development sessions with precise timing.
- **Task Classification**: Automatically categorize time spent based on Git commits and command-line usage.
- **Data Export**: Export productivity statistics to CSV or JSON formats for external analysis.
- **Shell History Parser**: Deep analysis of shell history to identify tool and command usage patterns.
- **Efficiency Scoring**: Calculates a weekly efficiency score based on output volume and session duration.
- **Focus Mode**: Enables dedicated focus sessions that suppress notifications and track uninterrupted work time.
- **Report Generation**: Automatically generates detailed weekly productivity summaries and actionable insights.

## Installation

DevProductivity CLI is available via PyPI. Ensure you have Python 3.8 or higher installed.

```bash
pip install dev-productivity-cli
```

## Quick Start

Get up and running in under a minute to start tracking your workflow.

```bash
# Initialize the tracker
dev-productivity init

# Start a development session
dev-productivity start "Feature Implementation"

# Pause (optional)
dev-productivity pause

# End the session
dev-productivity stop

# Generate a summary report
dev-productivity report --week
```

## Usage

The CLI offers various subcommands to manage your productivity data.

### Managing Sessions
```bash
# Start a new session with a specific tag
dev-productivity start "Bug Fixing - Issue #42"

# Pause the current active session
dev-productivity pause

# Resume a paused session
dev-productivity resume

# End the current session
dev-productivity stop
```

### Analysis & Reporting
```bash
# View your weekly productivity score
dev-productivity score

# Generate a PDF or Markdown report
dev-productivity report --format markdown --output weekly_summary.md

# View recent activity logs
dev-productivity logs --days 7
```

### Data Export
```bash
# Export all data to JSON
dev-productivity export --format json --output data.json

# Export summary statistics to CSV
dev-productivity export --format csv --output stats.csv
```

### Focus Mode
```bash
# Start a focus session (disables notifications via TTY)
dev-productivity focus --duration 90
```

## Architecture

The application follows a modular design pattern, ensuring maintainability and extensibility.

- **`session_timer`**: Handles the logic for tracking start/end times, including support for pausing and resuming active sessions.
- **`task_classifier`**: Analyzes recent Git commits and command history to assign categories to tracked time blocks.
-