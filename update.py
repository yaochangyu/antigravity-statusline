#!/usr/bin/env python3
import os
import sys
import shutil

def main():
    print("Updating Antigravity Statusline script to the latest version...")
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    src_file = os.path.join(script_dir, "statusline.py")
    
    home_dir = os.path.expanduser("~")
    target_file = os.path.join(home_dir, ".gemini", "antigravity-cli", "scratch", "statusline.py")
    
    if os.path.exists(src_file):
        print(f"Copying latest statusline.py to {target_file}...")
        try:
            if os.path.exists(target_file):
                os.remove(target_file)
            shutil.copy(src_file, target_file)
            print("\033[0;32mUpdate successful!\033[0m")
        except Exception as e:
            print(f"Error copying file: {e}")
            sys.exit(1)
    else:
        print("Local statusline.py not found. Downloading the latest version from GitHub...")
        import urllib.request
        url = "https://raw.githubusercontent.com/yaochangyu/antigravity-statusline/main/statusline.py"
        try:
            with urllib.request.urlopen(url) as response, open(target_file, 'wb') as out_file:
                out_file.write(response.read())
            print(f"Downloaded latest statusline.py to {target_file}.")
            print("\033[0;32mUpdate successful!\033[0m")
        except Exception as e:
            print(f"Error downloading script: {e}")
            sys.exit(1)

if __name__ == "__main__":
    main()
