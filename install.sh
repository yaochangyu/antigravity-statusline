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
    # Local installation: create symlink
    echo "Creating symlink at $TARGET_FILE -> $SCRIPT_SRC..."
    rm -f "$TARGET_FILE"
    ln -s "$SCRIPT_SRC" "$TARGET_FILE"
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

echo -e "${GREEN}Installation successful!${NC}"
echo "Statusline script is installed and ready to be used by antigravity-cli."
