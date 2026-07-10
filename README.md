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

### 1. One-line Remote Installation (Recommended)

You can run the installer directly from GitHub using `curl` or `wget` without cloning the repository:

```bash
curl -sSL https://raw.githubusercontent.com/yaochangyu/antigravity-statusline/main/install.sh | bash
```

### 2. Local Installation (For Developers)

If you plan to customize the statusline and want changes to sync via symlink, clone the repository and run the local installer:

```bash
git clone https://github.com/yaochangyu/antigravity-statusline.git
cd antigravity-statusline
chmod +x install.sh
./install.sh
```
