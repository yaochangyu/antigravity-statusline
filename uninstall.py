#!/usr/bin/env python3
import os
import sys
import json

def main():
    print("Uninstalling Antigravity Statusline script...")
    
    # 1. Paths
    home_dir = os.path.expanduser("~")
    target_file = os.path.join(home_dir, ".gemini", "antigravity-cli", "scratch", "statusline.py")
    
    # Remove file
    if os.path.exists(target_file):
        print(f"Removing {target_file}...")
        try:
            os.remove(target_file)
        except Exception as e:
            print(f"Error removing file: {e}")
    else:
        print("statusline.py is not installed at the target path.")

    # 2. Configure settings.json
    settings_file = os.path.join(home_dir, ".gemini", "antigravity-cli", "settings.json")
    if os.path.exists(settings_file):
        print(f"Removing statusLine configuration from {settings_file}...")
        try:
            with open(settings_file, "r", encoding="utf-8") as f:
                settings_data = json.load(f)
            
            if "statusLine" in settings_data:
                del settings_data["statusLine"]
                with open(settings_file, "w", encoding="utf-8") as f:
                    json.dump(settings_data, f, indent=2)
                print("Configuration removed from settings.json.")
            else:
                print("No statusLine configuration found in settings.json.")
        except Exception as e:
            print(f"Failed to update settings.json: {e}")
            
    print("\033[0;32mUninstallation successful!\033[0m")

if __name__ == "__main__":
    main()
