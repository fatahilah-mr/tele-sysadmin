import subprocess
from core.executor import escape_html

COMMON_SERVICES = ["nginx", "docker", "ssh", "mysql", "postgresql", "tele-sysadmin-daemon"]

def get_services_status():
    output = "<b>⚙️ Status Systemd Services:</b>\n\n"
    for srv in COMMON_SERVICES:
        try:
            res = subprocess.run(["systemctl", "is-active", srv], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            status = res.stdout.strip()
            icon = "🟢" if status == "active" else "🔴"
            output += f"{icon} <b>{srv}:</b> {status} ➔ Tap restart: <code>/service restart {srv}</code>\n"
        except Exception:
            output += f"❓ <b>{srv}:</b> unknown\n"
    return output

def handle_service_command(text):
    parts = text.strip().split()
    if len(parts) < 3:
        return get_services_status()

    action = parts[1].lower()
    service_name = parts[2].strip()

    if action in ["restart", "start", "stop", "status"]:
        try:
            res = subprocess.run(["systemctl", action, service_name], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=15)
            out = res.stdout.strip() or f"Service {service_name} {action} completed."
            icon = "✅" if res.returncode == 0 else "❌"
            return f"{icon} <b>Systemctl {action} {service_name}:</b>\n<pre><code>{escape_html(out)}</code></pre>"
        except Exception as e:
            return f"❌ Error executing service command: {e}"
    return get_services_status()
