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

# 2. Get script source path
SCRIPT_SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/statusline.py"

if [ ! -f "$SCRIPT_SRC" ]; then
    echo -e "${RED}Error: statusline.py not found in the current directory.${NC}"
    exit 1
fi

# 3. Create target scratch directory
TARGET_DIR="$HOME/.gemini/antigravity-cli/scratch"
mkdir -p "$TARGET_DIR"

# 4. Create symlink
TARGET_LINK="$TARGET_DIR/statusline.py"
echo "Creating symlink at $TARGET_LINK -> $SCRIPT_SRC..."
rm -f "$TARGET_LINK"
ln -s "$SCRIPT_SRC" "$TARGET_LINK"

echo -e "${GREEN}Installation successful!${NC}"
echo "Statusline script is linked and ready to be used by antigravity-cli."
