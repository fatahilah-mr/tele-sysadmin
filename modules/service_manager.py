import subprocess
from core.executor import escape_html

DEFAULT_SERVICES = ["nginx", "docker", "ssh", "sshd", "mysql", "mariadb", "postgresql", "redis", "apache2", "ufw", "fail2ban", "tele-sysadmin-daemon"]

def discover_active_services():
    services = set(DEFAULT_SERVICES)
    try:
        # Auto-discover active or failed services on the VPS
        res = subprocess.run(["systemctl", "list-units", "--type=service", "--state=running,failed", "--no-legend"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=5)
        for line in res.stdout.splitlines():
            parts = line.strip().split()
            if parts:
                srv_name = parts[0].replace(".service", "")
                services.add(srv_name)
    except Exception:
        pass
    return sorted(list(services))

def get_services_status():
    output = "<b>⚙️ Status Systemd Services:</b>\n\n"
    active_count = 0
    all_services = discover_active_services()

    for srv in all_services:
        try:
            res = subprocess.run(["systemctl", "is-active", srv], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            status = res.stdout.strip()
            if status == "active":
                active_count += 1
                icon = "🟢"
                output += f"{icon} <b>{srv}:</b> active ➔ <code>/service restart {srv}</code>\n"
            elif status == "failed":
                icon = "🔴"
                output += f"{icon} <b>{srv}:</b> FAILED ➔ <code>/service restart {srv}</code>\n"
        except Exception:
            pass

    output += f"\n<i>Total Service Active: {active_count}</i>"
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
