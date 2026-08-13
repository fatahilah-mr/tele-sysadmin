import sys
import json
import urllib.request
from datetime import datetime
from core.logger import write_log

CATEGORIES = {
    "success":  {"emoji": "✅", "header": "SUCCESS / SELESAI"},
    "error":    {"emoji": "❌", "header": "ERROR / GAGAL"},
    "warning":  {"emoji": "⚠️", "header": "WARNING / PERINGATAN"},
    "info":     {"emoji": "ℹ️", "header": "INFO"},
    "task":     {"emoji": "🚀", "header": "TASK COMPLETED"},
    "deploy":   {"emoji": "🎉", "header": "DEPLOYMENT STATUS"},
    "security": {"emoji": "🔒", "header": "SECURITY ALERT"},
    "database": {"emoji": "🗄️", "header": "DATABASE NOTIFICATION"},
    "db":       {"emoji": "🗄️", "header": "DATABASE NOTIFICATION"},
    "backup":   {"emoji": "💾", "header": "BACKUP STATUS"},
    "cron":     {"emoji": "⏰", "header": "CRON JOB RESULT"},
    "server":   {"emoji": "🖥️", "header": "SERVER STATUS"},
    "billing":  {"emoji": "💳", "header": "BILLING & PAYMENT"},
    "build":    {"emoji": "🏗️", "header": "BUILD STATUS"},
    "alert":    {"emoji": "🚨", "header": "EMERGENCY ALERT"},
    "system":   {"emoji": "⚙️", "header": "SYSTEM NOTIFICATION"},
    "update":   {"emoji": "🔄", "header": "SYSTEM UPDATE"},
    "test":     {"emoji": "🧪", "header": "TEST RESULT"},
    "bot":      {"emoji": "🤖", "header": "BOT ACTION"},
}

def send_notification(category, title, message, bot_token, chat_id, custom_emoji=None):
    cat_key = category.lower()
    if cat_key in CATEGORIES:
        cat_info = CATEGORIES[cat_key]
        emoji = custom_emoji or cat_info["emoji"]
        header = cat_info["header"]
    else:
        emoji = custom_emoji or "🔔"
        header = category.upper()

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    html_text = f"{emoji} <b>[{header}] {title}</b>\n\n"
    if message:
        html_text += f"{message}\n\n"
    html_text += f"<i>⏱️ {now} | Server: Debian VPS</i>"

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": html_text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})

    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            if res_data.get("ok"):
                print("Notification sent successfully!")
                write_log("SENT", category, title, message)
                return True
            else:
                err_msg = str(res_data)
                print(f"Failed to send notification: {err_msg}", file=sys.stderr)
                write_log("FAILED", category, title, message, error_detail=err_msg)
                return False
    except Exception as e:
        print(f"Error sending notification: {e}", file=sys.stderr)
        write_log("FAILED", category, title, message, error_detail=str(e))
        return False
