import subprocess
from core.executor import escape_html

def get_docker_status():
    try:
        res = subprocess.run(["docker", "ps", "--format", "table {{.Names}}\t{{.Status}}\t{{.Ports}}"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=10)
        if res.returncode != 0:
            return "<i>Docker tidak terinstall atau daemon tidak aktif.</i>"
        out = res.stdout.strip()
        if not out:
            return "<i>Tidak ada container Docker yang sedang berjalan.</i>"
        return f"<b>🐳 Docker Active Containers:</b>\n<pre><code>{escape_html(out)}</code></pre>"
    except Exception as e:
        return f"Docker Error: {e}"

def handle_docker_command(text):
    parts = text.strip().split()
    if len(parts) < 2:
        return get_docker_status()

    action = parts[1].lower()
    if action == "ps":
        return get_docker_status()
    elif action in ["restart", "stop", "logs"] and len(parts) >= 3:
        target = parts[2].strip()
        try:
            cmd = ["docker", action, target]
            if action == "logs":
                cmd = ["docker", "logs", "--tail", "50", target]
            res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=15)
            out = res.stdout.strip() or f"Docker {action} {target} executed."
            icon = "✅" if res.returncode == 0 else "❌"
            return f"{icon} <b>Docker {action} {target}:</b>\n<pre><code>{escape_html(out)}</code></pre>"
        except Exception as e:
            return f"❌ Docker Command Error: {e}"

    return get_docker_status()
