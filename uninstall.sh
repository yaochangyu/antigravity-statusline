#!/bin/bash
set -e

# ANSI color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo "Uninstalling Antigravity Statusline script..."

# 1. Remove the installed script
TARGET_FILE="$HOME/.gemini/antigravity-cli/scratch/statusline.py"
if [ -f "$TARGET_FILE" ] || [ -L "$TARGET_FILE" ]; then
    echo "Removing $TARGET_FILE..."
    rm -f "$TARGET_FILE"
else
    echo "statusline.py is not installed at $TARGET_FILE."
fi

# 2. Remove configuration from settings.json
SETTINGS_FILE="$HOME/.gemini/antigravity-cli/settings.json"
if [ -f "$SETTINGS_FILE" ]; then
    echo "Removing statusLine configuration from $SETTINGS_FILE..."
    python3 -c "
import json, os
path = os.path.expanduser('~/.gemini/antigravity-cli/settings.json')
try:
    with open(path, 'r') as f:
        data = json.load(f)
    if 'statusLine' in data:
        del data['statusLine']
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)
        print('Configuration removed from settings.json.')
    else:
        print('No statusLine configuration found in settings.json.')
except Exception as e:
    print('Failed to update settings.json:', e)
"
fi

echo -e "${GREEN}Uninstallation successful!${NC}"
