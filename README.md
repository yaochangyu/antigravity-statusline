# Antigravity Statusline

[English](README.md) | [繁體中文](README.zh-TW.md)

A customizable Python statusline script for `antigravity-cli` (and Claude Code environments) that displays Git branch information, API rate limits, real-time spent costs, session duration, and active agent skills.

## Features

- **Git Status**: Displays the current branch, dirty status (`*`), and ahead/behind commits.
- **Rate Limits**: Shows used quotas and resets for 5-hour and Weekly limits with custom progress bars.
- **Cost Monitoring**: Shows today's and this month's cumulative API costs directly (no arbitrary limits).
- **Active Skills**: Dynamically parses the session transcript to show the currently running skill (e.g. `write-yaochangyu-style`).
- **ANSI Colors**: Consistent visual color schemes matching premium dark/gray themes.

## Installation

Run the installation script to create a symlink from this directory to the active `.gemini` configurations directory:

```bash
chmod +x install.sh
./install.sh
```
