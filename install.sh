#!/bin/bash
set -e

# ANSI color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo "Installing Antigravity Statusline script..."

# 1. Check for Python 3
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed or not in PATH.${NC}"
    exit 1
fi

# 2. Get script paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd || pwd)"
SCRIPT_SRC="$SCRIPT_DIR/statusline.py"

# 3. Create target scratch directory
TARGET_DIR="$HOME/.gemini/antigravity-cli/scratch"
mkdir -p "$TARGET_DIR"
TARGET_FILE="$TARGET_DIR/statusline.py"

# 4. Install file
if [ -f "$SCRIPT_SRC" ]; then
    # Local installation: copy file
    echo "Copying statusline.py to $TARGET_FILE..."
    rm -f "$TARGET_FILE"
    cp "$SCRIPT_SRC" "$TARGET_FILE"
else
    # Standalone/remote installation: download the file directly
    echo "Local statusline.py not found. Downloading from GitHub..."
    if command -v curl &> /dev/null; then
        curl -sSL "https://raw.githubusercontent.com/yaochangyu/antigravity-statusline/main/statusline.py" -o "$TARGET_FILE"
    elif command -v wget &> /dev/null; then
        wget -qO "$TARGET_FILE" "https://raw.githubusercontent.com/yaochangyu/antigravity-statusline/main/statusline.py"
    else
        echo -e "${RED}Error: Neither curl nor wget is installed.${NC}"
        exit 1
    fi
    echo "Downloaded statusline.py to $TARGET_FILE."
fi

# 5. Configure settings.json in antigravity-cli
SETTINGS_FILE="$HOME/.gemini/antigravity-cli/settings.json"
echo "Configuring statusLine in $SETTINGS_FILE..."
python3 -c "
import json, os
path = os.path.expanduser('~/.gemini/antigravity-cli/settings.json')
os.makedirs(os.path.dirname(path), exist_ok=True)
try:
    with open(path, 'r') as f:
        data = json.load(f)
except Exception:
    data = {}
data['statusLine'] = {
    'type': 'command',
    'command': 'python3 ' + os.path.expanduser('~/.gemini/antigravity-cli/scratch/statusline.py'),
    'enabled': True
}
with open(path, 'w') as f:
    json.dump(data, f, indent=2)
"

echo -e "${GREEN}Installation successful!${NC}"
echo "Statusline script is installed and configured in settings.json."
