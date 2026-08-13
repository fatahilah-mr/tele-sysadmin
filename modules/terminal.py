import os
import glob
from core.executor import execute_bash_command, escape_html, strip_ansi

def autocomplete_path(query, session_cwd):
    query = query.strip()
    if not query:
        search_pattern = os.path.join(session_cwd, "*")
    elif query.startswith("/"):
        search_pattern = query + "*"
    else:
        search_pattern = os.path.join(session_cwd, query + "*")

    matches = glob.glob(search_pattern)
    matches.sort()
    
    if not matches:
        return "<i>Tidak ada file/folder yang cocok.</i>"

    output = f"<b>💡 Autocomplete / Suggestions ({len(matches)} hasil):</b>\n\n"
    for m in matches[:15]:
        is_dir = os.path.isdir(m)
        icon = "📁" if is_dir else "📄"
        rel_name = os.path.relpath(m, session_cwd) if m.startswith(session_cwd) else m
        if is_dir:
            cmd = f"cd {rel_name}"
            output += f"{icon} <code>{escape_html(rel_name)}/</code> ➔ Tap: <code>{escape_html(cmd)}</code>\n"
        else:
            cmd = f"/read {rel_name}"
            output += f"{icon} <code>{escape_html(rel_name)}</code> ➔ Tap: <code>{escape_html(cmd)}</code>\n"
    return output

def get_shell_keyboard():
    return {
        "keyboard": [
            [{"text": "ls -la"}, {"text": "pwd"}, {"text": "uptime"}],
            [{"text": "df -h"}, {"text": "free -h"}, {"text": "/tab"}],
            [{"text": "/chart"}, {"text": "/status"}, {"text": "/logs"}],
            [{"text": "/exit"}]
        ],
        "resize_keyboard": True,
        "is_persistent": True
    }
