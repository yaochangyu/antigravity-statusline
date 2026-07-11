#!/usr/bin/env python3
import os
import sys
import shutil
import json

def main():
    print("Installing Antigravity Statusline script...")
    
    # 1. Paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    src_file = os.path.join(script_dir, "statusline.py")
    
    home_dir = os.path.expanduser("~")
    target_dir = os.path.join(home_dir, ".gemini", "antigravity-cli", "scratch")
    os.makedirs(target_dir, exist_ok=True)
    
    target_file = os.path.join(target_dir, "statusline.py")
    
    # 2. Copy file
    if os.path.exists(src_file):
        print(f"Copying statusline.py to {target_file}...")
        try:
            if os.path.exists(target_file):
                os.remove(target_file)
            shutil.copy(src_file, target_file)
        except Exception as e:
            print(f"Error copying file: {e}")
            sys.exit(1)
    else:
        # Fallback to download if run from elsewhere
        print("Local statusline.py not found. Downloading from GitHub...")
        import urllib.request
        url = "https://raw.githubusercontent.com/yaochangyu/antigravity-statusline/main/statusline.py"
        try:
            with urllib.request.urlopen(url) as response, open(target_file, 'wb') as out_file:
                out_file.write(response.read())
            print(f"Downloaded statusline.py to {target_file}.")
        except Exception as e:
            print(f"Error downloading script: {e}")
            sys.exit(1)

    # 3. Configure settings.json
    settings_file = os.path.join(home_dir, ".gemini", "antigravity-cli", "settings.json")
    print(f"Configuring statusLine in {settings_file}...")
    
    # Determine default python command based on OS
    python_cmd = "python" if os.name == 'nt' else "python3"
    
    # Use standard Unix/Windows path string in settings.json
    command_str = f"{python_cmd} ~/.gemini/antigravity-cli/scratch/statusline.py"
    
    settings_data = {}
    if os.path.exists(settings_file):
        try:
            with open(settings_file, "r", encoding="utf-8") as f:
                settings_data = json.load(f)
        except Exception:
            pass
            
    settings_data["statusLine"] = {
        "type": "command",
        "command": command_str,
        "enabled": True,
        "autoUpdate": True
    }
    
    try:
        with open(settings_file, "w", encoding="utf-8") as f:
            json.dump(settings_data, f, indent=2)
        print("\033[0;32mInstallation successful!\033[0m")
        print("Statusline script is installed and configured in settings.json.")
    except Exception as e:
        print(f"Error writing settings: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
