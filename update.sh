#!/bin/bash
set -e

# ANSI color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo "Updating Antigravity Statusline script to the latest version..."

# 1. Get script paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd || pwd)"
SCRIPT_SRC="$SCRIPT_DIR/statusline.py"

TARGET_DIR="$HOME/.gemini/antigravity-cli/scratch"
mkdir -p "$TARGET_DIR"
TARGET_FILE="$TARGET_DIR/statusline.py"

# 2. Update file
if [ -f "$SCRIPT_SRC" ]; then
    # Local update: copy file
    echo "Copying latest statusline.py to $TARGET_FILE..."
    rm -f "$TARGET_FILE"
    cp "$SCRIPT_SRC" "$TARGET_FILE"
else
    # Standalone/remote update: download the file directly
    echo "Local statusline.py not found. Downloading the latest version from GitHub..."
    if command -v curl &> /dev/null; then
        curl -sSL "https://raw.githubusercontent.com/yaochangyu/antigravity-statusline/main/statusline.py" -o "$TARGET_FILE"
    elif command -v wget &> /dev/null; then
        wget -qO "$TARGET_FILE" "https://raw.githubusercontent.com/yaochangyu/antigravity-statusline/main/statusline.py"
    else
        echo -e "${RED}Error: Neither curl nor wget is installed.${NC}"
        exit 1
    fi
    echo "Downloaded latest statusline.py to $TARGET_FILE."
fi

echo -e "${GREEN}Update successful!${NC}"
