import sys
import json
import os
import time
import subprocess
from datetime import datetime, timedelta

HOME_DIR = os.path.expanduser("~")
BASE_DIR = os.path.join(HOME_DIR, ".gemini", "antigravity-cli")
CACHE_FILE = os.path.join(BASE_DIR, "scratch", "statusline_cache.json")
LAST_STDIN = os.path.join(BASE_DIR, "scratch", "last_stdin.json")
VERSION = "1.0.1"
CACHE_TTL = 30  # 30 seconds
EXTRA_LIMIT = 20.00  # 預設額外限額為 $20.00 美元

def update_cache():
    try:
        use_shell = (os.name == 'nt')
        # 1. 取得今日花費 (daily) - Use --no-install to skip network checks
        daily_res = subprocess.run(["npx", "--no-install", "ccusage", "daily", "--json"], capture_output=True, text=True, timeout=10, shell=use_shell)
        daily_json = json.loads(daily_res.stdout) if daily_res.returncode == 0 else {}
        daily_data = daily_json.get("daily", []) if isinstance(daily_json, dict) else []
        
        # 2. 取得本月花費 (monthly) - Use --no-install to skip network checks
        monthly_res = subprocess.run(["npx", "--no-install", "ccusage", "monthly", "--json"], capture_output=True, text=True, timeout=10, shell=use_shell)
        monthly_json = json.loads(monthly_res.stdout) if monthly_res.returncode == 0 else {}
        monthly_data = monthly_json.get("monthly", []) if isinstance(monthly_json, dict) else []

        # 解析今日花費
        today_str = datetime.now().strftime("%Y-%m-%d")
        today_cost = 0.0
        for item in daily_data:
            if isinstance(item, dict) and item.get("period") == today_str and item.get("agent") == "all":
                today_cost = item.get("totalCost", 0.0)
                break
                
        # 解析本月花費
        month_str = datetime.now().strftime("%Y-%m")
        month_cost = 0.0
        for item in monthly_data:
            if isinstance(item, dict) and item.get("period") == month_str and item.get("agent") == "all":
                month_cost = item.get("totalCost", 0.0)
                break

        # 讀取現有快取以保留 session_start_time 及版本檢查狀態
        existing_cache = {}
        if os.path.exists(CACHE_FILE):
            try:
                with open(CACHE_FILE, "r") as f:
                    existing_cache = json.load(f)
            except:
                pass

        # 檢查更新 (每 24 小時一次)
        now = time.time()
        last_check = existing_cache.get("last_version_check", 0)
        update_available = existing_cache.get("update_available", False)
        
        if now - last_check > 86400:
            try:
                import urllib.request
                import re
                req = urllib.request.Request(
                    "https://raw.githubusercontent.com/yaochangyu/antigravity-statusline/main/statusline.py",
                    headers={'User-Agent': 'Mozilla/5.0'}
                )
                with urllib.request.urlopen(req, timeout=3) as response:
                    remote_code = response.read().decode('utf-8')
                    m = re.search(r'VERSION\s*=\s*["\']([^"\']+)["\']', remote_code)
                    if m:
                        remote_ver = m.group(1)
                        if remote_ver != VERSION:
                            update_available = True
                            
                            # 檢查 settings.json 中的 autoUpdate 設定
                            auto_update = False
                            try:
                                settings_path = os.path.join(BASE_DIR, "settings.json")
                                if os.path.exists(settings_path):
                                    with open(settings_path, 'r') as f_set:
                                        settings_data = json.load(f_set)
                                        auto_update = settings_data.get("statusLine", {}).get("autoUpdate", False)
                            except Exception:
                                pass
                                
                            if auto_update:
                                script_path = os.path.abspath(__file__)
                                # 若非軟連結才自動覆蓋，保護開發者工作區
                                if not os.path.islink(script_path):
                                    with open(script_path, "w", encoding="utf-8") as f_self:
                                        f_self.write(remote_code)
                                    update_available = False
                        else:
                            update_available = False
                last_check = now
            except Exception:
                pass

        cache_data = {
            "today_cost": today_cost,
            "month_cost": month_cost,
            "session_id": existing_cache.get("session_id"),
            "session_start_time": existing_cache.get("session_start_time"),
            "last_version_check": last_check,
            "update_available": update_available,
            "updated_at": now
        }
        
        os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
        with open(CACHE_FILE, "w") as f:
            json.dump(cache_data, f)
            
    except Exception as e:
        error_log = os.path.join(BASE_DIR, "scratch", "statusline_update_error.txt")
        with open(error_log, "w") as f:
            f.write(str(e))

def read_cache():
    if not os.path.exists(CACHE_FILE):
        return {}
    try:
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def get_git_status_str(cwd):
    if not cwd or not os.path.exists(cwd):
        return ""
    try:
        use_shell = (os.name == 'nt')
        # Optimized: run a single git status command to get branch, ahead/behind and dirty status in one process spawn
        status_res = subprocess.run(
            ["git", "-C", cwd, "status", "-b", "--porcelain"],
            capture_output=True, text=True, timeout=1, shell=use_shell
        )
        if status_res.returncode != 0:
            return ""
            
        lines = status_res.stdout.strip().splitlines()
        if not lines:
            return ""
            
        first_line = lines[0]
        if not first_line.startswith("##"):
            return ""
            
        status_part = first_line[2:].strip()
        
        ahead = 0
        behind = 0
        
        import re
        bracket_match = re.search(r'\[([^\]]+)\]', status_part)
        if bracket_match:
            bracket_content = bracket_match.group(1)
            ahead_match = re.search(r'ahead (\d+)', bracket_content)
            if ahead_match:
                ahead = int(ahead_match.group(1))
            behind_match = re.search(r'behind (\d+)', bracket_content)
            if behind_match:
                behind = int(behind_match.group(1))
            status_part = status_part[:bracket_match.start()].strip()
            
        if "..." in status_part:
            branch = status_part.split("...")[0].strip()
        else:
            branch = status_part
            
        dirty = "*" if len(lines) > 1 else ""
        dirty_str = f"\033[31m*\033[0m" if dirty else ""
        
        ahead_behind = ""
        ab_parts = []
        if ahead > 0:
            ab_parts.append(f"\033[36m⇡{ahead}\033[0m")
        if behind > 0:
            ab_parts.append(f"\033[31m⇣{behind}\033[0m")
        if ab_parts:
            ahead_behind = " \033[2m|\033[0m " + " ".join(ab_parts)
            
        return f"\033[2mbranch:\033[0m\033[36m{branch}\033[0m{dirty_str}{ahead_behind}"
    except Exception:
        pass
    return ""

def format_time(sec):
    if sec <= 0:
        return "0m"
    days = sec // 86400
    hours = (sec % 86400) // 3600
    mins = (sec % 3600) // 60
    
    if days > 0:
        return f"~{days}d{hours}h"
    elif hours > 0:
        return f"~{hours}h{mins}m"
    else:
        return f"~{mins}m"

def make_colored_bar(fraction, width=8):
    filled = int(round(fraction * width))
    filled = max(0, min(width, filled))
    empty = width - filled
    
    if fraction >= 1.0:
        # 紅色 (RED)
        bar = f"\033[31m" + "#" * filled + f"\033[0m"
    else:
        # 綠色 (GREEN)，未滿為灰色 (DIM)
        bar = f"\033[32m" + "#" * filled + f"\033[0m\033[2m" + "-" * empty + f"\033[0m"
        
    return f"\033[2m[\033[0m{bar}\033[2m]\033[0m"

def make_percentage_str(fraction):
    pct = int(round(fraction * 100))
    if fraction >= 1.0:
        return f"\033[31m{pct}%\033[0m"
    else:
        return f"\033[32m{pct}%\033[0m"

def parse_transcript(transcript_path):
    tool_calls = 0
    steps = 0
    last_prompt = "none"
    active_skill = None
    
    if transcript_path and not os.path.exists(transcript_path):
        norm_path = transcript_path.replace("\\", "/")
        if "antigravity" in norm_path and "antigravity-cli" not in norm_path:
            alt_norm = norm_path.replace("/antigravity/", "/antigravity-cli/")
            alt_path = os.path.normpath(alt_norm)
            if os.path.exists(alt_path):
                transcript_path = alt_path
                
    if not transcript_path or not os.path.exists(transcript_path):
        return tool_calls, steps, last_prompt, active_skill
        
    try:
        import re
        skill_re = re.compile(r"<SKILL>The user has explicitly invoked the \(([^)]+)\) skill")
        html_re = re.compile(r'<[^>]+>')
        
        with open(transcript_path, "r", errors="ignore") as f:
            for line in f:
                if not line.startswith('{'):
                    continue
                steps += 1
                
                # Fast pre-filtering: skip json.loads if the line does not contain keywords
                has_tool_calls = "tool_calls" in line
                has_user_input = "USER_INPUT" in line
                if not (has_tool_calls or has_user_input):
                    continue
                    
                try:
                    data = json.loads(line)
                    if has_tool_calls:
                        t_calls = data.get("tool_calls", [])
                        if isinstance(t_calls, list):
                            tool_calls += len(t_calls)
                            for tc in t_calls:
                                if tc.get("name") == "view_file":
                                    args = tc.get("args", {})
                                    if args.get("IsSkillFile") is True or str(args.get("IsSkillFile")).lower() == "true":
                                        path = args.get("AbsolutePath", "")
                                        if path:
                                            parts = path.replace("\\", "/").split("/")
                                            if len(parts) >= 2:
                                                active_skill = parts[-2]
                                                
                    if has_user_input and data.get("type") == "USER_INPUT":
                        content = data.get("content", "")
                        if content:
                            last_prompt = content.strip().replace("\n", " ")
                            m = skill_re.search(content)
                            if m:
                                active_skill = m.group(1)
                except:
                    pass
    except Exception:
        pass
        
    if last_prompt != "none":
        last_prompt = html_re.sub('', last_prompt).strip()
        
    if len(last_prompt) > 15:
        last_prompt = last_prompt[:15] + "..."
    return tool_calls, steps, last_prompt, active_skill

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--update-cache":
        update_cache()
        return

    # 1. 讀取 stdin (Optimized: non-blocking select on TTY)
    stdin_data = {}
    try:
        if not sys.stdin.isatty():
            raw_stdin = sys.stdin.read()
            if raw_stdin.strip():
                stdin_data = json.loads(raw_stdin)
                with open(LAST_STDIN, "w") as f:
                    json.dump(stdin_data, f, indent=2)
        else:
            if os.name != 'nt':
                import select
                # Use 0.0 timeout instead of 0.1 to avoid blocking when run interactively
                if select.select([sys.stdin], [], [], 0.0)[0]:
                    raw_stdin = sys.stdin.read()
                    if raw_stdin.strip():
                        stdin_data = json.loads(raw_stdin)
                        with open(LAST_STDIN, "w") as f:
                            json.dump(stdin_data, f, indent=2)
    except Exception:
        pass

    # 2. 檢查與讀取快取
    cache = read_cache()
    need_update = False
    
    if not cache:
        need_update = True
        cache = {
            "today_cost": 0.0,
            "month_cost": 0.0,
            "session_id": None,
            "session_start_time": None
        }
    elif time.time() - cache.get("updated_at", 0) > CACHE_TTL:
        need_update = True

    # 處理 session 啟動時間
    session_id = stdin_data.get("session_id", "default")
    session_start_time = cache.get("session_start_time")
    cached_session_id = cache.get("session_id")
    
    if not cached_session_id or cached_session_id != session_id or not session_start_time:
        session_start_time = time.time()
        cache["session_id"] = session_id
        cache["session_start_time"] = session_start_time
        try:
            with open(CACHE_FILE, "w") as f:
                json.dump(cache, f)
        except:
            pass

    if need_update:
        script_path = os.path.abspath(__file__)
        subprocess.Popen([sys.executable, script_path, "--update-cache"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # 3. 取得各行內容
    cwd = stdin_data.get("cwd") or os.getcwd()
    
    # --- 第一行 ---
    line1 = get_git_status_str(cwd)
    
    # --- 第二行 ---
    version = stdin_data.get("version", "4.15.2")
    model_name = stdin_data.get("model", {}).get("display_name", "Unknown")
    
    # 決定使用哪組額度
    model_id_lower = stdin_data.get("model", {}).get("id", "").lower()
    is_gemini = "gemini" in model_id_lower
    
    quota = stdin_data.get("quota", {})
    
    # 5h 額度
    q_5h_key = "gemini-5h" if is_gemini else "3p-5h"
    q_5h = quota.get(q_5h_key, {})
    rem_5h = q_5h.get("remaining_fraction", 1.0)
    reset_5h = q_5h.get("reset_in_seconds", 0)
    used_5h = 1.0 - rem_5h
    bar_5h = make_colored_bar(used_5h, 8)
    pct_5h_str = make_percentage_str(used_5h)
    time_5h = format_time(reset_5h)
    
    # Weekly 額度
    q_wk_key = "gemini-weekly" if is_gemini else "3p-weekly"
    q_wk = quota.get(q_wk_key, {})
    rem_wk = q_wk.get("remaining_fraction", 1.0)
    reset_wk = q_wk.get("reset_in_seconds", 0)
    used_wk = 1.0 - rem_wk
    bar_wk = make_colored_bar(used_wk, 8)
    pct_wk_str = make_percentage_str(used_wk)
    time_wk = format_time(reset_wk)
    
    # 費用額度 (對應今日與本月累計花費)
    today_cost = cache.get("today_cost", 0.0)
    month_cost = cache.get("month_cost", 0.0)
    
    agent_state = stdin_data.get("agent_state", "idle")
    session_mins = int((time.time() - session_start_time) // 60)
    
    # --- 第三行 ---
    transcript_path = stdin_data.get("transcript_path", "")
    tool_calls, steps, last_prompt, active_skill = parse_transcript(transcript_path)
    
    # Context 百分比
    ctx_win = stdin_data.get("context_window", {})
    ctx_pct_val = ctx_win.get("used_percentage", 0.0) / 100.0 if isinstance(ctx_win, dict) else 0.0
    bar_ctx = make_colored_bar(ctx_pct_val, 10)
    pct_ctx_str = make_percentage_str(ctx_pct_val)
    
    artifact_count = stdin_data.get("artifact_count", 0)
    
    # 格式化輸出，加上漂亮的 ANSI 顏色
    f_line1 = line1
    
    star_5h = "*" if rem_5h < 1.0 else ""
    star_wk = "*" if rem_wk < 1.0 else ""
    
    f_model = f"\033[2mModel:\033[0m \033[36m{model_name}\033[0m"
    f_5h = f"\033[2m5h:\033[0m{bar_5h}{pct_5h_str}{star_5h}\033[2m({time_5h})\033[0m"
    f_wk = f"\033[2mwk:\033[0m{bar_wk}{pct_wk_str}{star_wk}\033[2m({time_wk})\033[0m"
    f_today = f"\033[2mtoday:\033[0m\033[32m${today_cost:.2f}\033[0m"
    f_month = f"\033[2mmonth:\033[0m\033[32m${month_cost:.2f}\033[0m"
    
    state_color = "31" if agent_state in ["working", "thinking"] else "37"
    f_state = f"\033[{state_color}m{agent_state}\033[0m"
    
    update_available = cache.get("update_available", False)
    f_session = f"\033[2msession:\033[0m\033[32m{session_mins}m\033[0m"
    if update_available:
        f_session += " \033[33;1m(🌟Update Available)\033[0m"
    
    line2 = f"  {f_model} \033[2m|\033[0m {f_5h} {f_wk} {f_today} {f_month} \033[2m|\033[0m {f_state} \033[2m|\033[0m {f_session}"
    
    # --- 第三行 ---
    f_ctx = f"\033[2mctx:\033[0m{bar_ctx}{pct_ctx_str}"
    f_stats = f"\033[2mTools:\033[0m\033[35m{tool_calls}\033[0m \033[2m| Artifacts:\033[0m\033[35m{artifact_count}\033[0m \033[2m| Steps:\033[0m\033[35m{steps}\033[0m"
    
    if active_skill:
        f_skill = f"\033[2mskill:\033[0m\033[36m{active_skill}\033[0m"
        line3 = f"  {f_skill} \033[2m|\033[0m {f_ctx} \033[2m|\033[0m {f_stats}"
    else:
        line3 = f"  {f_ctx} \033[2m|\033[0m {f_stats}"
    
    if f_line1:
        print(f"{f_line1}\n{line2}\n{line3}")
    else:
        print(f"{line2}\n{line3}")

if __name__ == "__main__":
    main()
