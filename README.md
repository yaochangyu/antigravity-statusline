# Antigravity Statusline

[English](README.md) | [繁體中文](README.zh-TW.md)

A customizable Python statusline script for `antigravity-cli` (and Claude Code environments) that displays Git branch information, API rate limits, real-time spent costs, session duration, and active agent skills.

![Antigravity Statusline Demo](demo.png)

## Features

- **Git Status**: Displays the current branch, dirty status (`*`), and ahead/behind commits.
- **Rate Limits**: Shows used quotas and resets for 5-hour and Weekly limits with custom progress bars.
- **Cost Monitoring**: Shows today's and this month's cumulative API costs directly (no arbitrary limits).
- **Active Skills**: Dynamically parses the session transcript to show the currently running skill (e.g. `write-yaochangyu-style`).
- **ANSI Colors**: Consistent visual color schemes matching premium dark/gray themes.

## Prerequisites

- **Python 3**: The statusline renderer requires Python 3. You can verify if it's installed by running `python3 --version`.
  - On Ubuntu/Debian: `sudo apt update && sudo apt install -y python3`
  - On macOS: `brew install python`
  - On Windows (WSL): `sudo apt install python3`

## Installation

### 1. One-line Remote Installation (Recommended)

You can run the installer directly from GitHub using `curl` or `wget` without cloning the repository:

```bash
curl -sSL https://raw.githubusercontent.com/yaochangyu/antigravity-statusline/main/install.sh | bash
```

### 2. Local Installation (For Developers)

If you plan to customize the statusline, clone the repository and run the local installer (which copies the script to your configuration directory):

```bash
git clone https://github.com/yaochangyu/antigravity-statusline.git
cd antigravity-statusline
chmod +x install.sh
./install.sh
```

## How It Works & Configuration

By default, `antigravity-cli` reads its settings from `~/.gemini/antigravity-cli/settings.json`. To execute a custom statusline script, the `"statusLine"` block must be configured to point to `statusline.py`.

The `install.sh` script automatically configures this for you. If you wish to configure it manually, add the following to your `settings.json`:

```json
{
  "statusLine": {
    "type": "command",
    "command": "python3 ~/.gemini/antigravity-cli/scratch/statusline.py",
    "enabled": true
  }
}
```

## Update

To update the statusline script to the latest version, simply run the installation command again (either remote one-liner or `./install.sh`). It will automatically fetch/overwrite the existing file with the latest version.

## Uninstallation

### 1. One-line Remote Uninstallation
You can run the uninstaller directly from GitHub:

```bash
curl -sSL https://raw.githubusercontent.com/yaochangyu/antigravity-statusline/main/uninstall.sh | bash
```

### 2. Local Uninstallation
If you cloned the repository, run the uninstaller script:

```bash
./uninstall.sh
```
