import os
import sys
from datetime import datetime

PRIMARY_LOG_PATH = "/var/log/tele-sysadmin.log"
FALLBACK_LOG_PATH = os.path.expanduser("~/.tele_sysadmin.log")

def get_log_file():
    try:
        with open(PRIMARY_LOG_PATH, "a") as f:
            pass
        return PRIMARY_LOG_PATH
    except Exception:
        return FALLBACK_LOG_PATH

def write_log(status, category, title, message="", error_detail=""):
    log_path = get_log_file()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    clean_msg = message.replace("\n", " ") if message else ""
    
    log_line = f"[{now}] [{status}] [{category.upper()}] {title}"
    if clean_msg:
        log_line += f" | Msg: {clean_msg}"
    if error_detail:
        log_line += f" | Error: {error_detail}"
    log_line += "\n"

    try:
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(log_line)
    except Exception as e:
        print(f"Warning: Could not write to log file: {e}", file=sys.stderr)

def show_logs(lines=20):
    log_path = get_log_file()
    if not os.path.exists(log_path):
        return f"Belum ada log notifikasi yang tercatat di {log_path}."

    try:
        with open(log_path, "r", encoding="utf-8") as f:
            all_lines = f.readlines()
            recent = all_lines[-lines:] if len(all_lines) > lines else all_lines
            if not recent:
                return "<i>Log kosong.</i>"
            
            output = f"<b>📜 Riwayat Log Server ({log_path}):</b>\n\n"
            for l in recent:
                safe_l = l.strip().replace("<", "&lt;").replace(">", "&gt;")
                output += f"<code>{safe_l}</code>\n\n"
            return output
    except Exception as e:
        return f"Error reading log file: {e}"
