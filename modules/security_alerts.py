import subprocess
from core.executor import escape_html

def check_ufw_status():
    try:
        res = subprocess.run(["ufw", "status", "verbose"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=5)
        out = res.stdout.strip()
        return f"<b>🛡️ Firewall (UFW) Status:</b>\n<pre><code>{escape_html(out)}</code></pre>"
    except Exception as e:
        return f"UFW Status Error: {e}"

def check_fail2ban_status():
    try:
        res = subprocess.run(["fail2ban-client", "status"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=5)
        if res.returncode != 0:
            return "<i>Fail2ban tidak terinstall/aktif di VPS ini.</i>"
        out = res.stdout.strip()
        return f"<b>🔒 Fail2ban Security Status:</b>\n<pre><code>{escape_html(out)}</code></pre>"
    except Exception as e:
        return f"Fail2ban Error: {e}"
