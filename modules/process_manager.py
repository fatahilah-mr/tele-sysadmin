import subprocess
from core.executor import escape_html

def get_top_processes(limit=10):
    try:
        cmd = f"ps aux --sort=-%mem | head -n {limit+1}"
        res = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=10)
        out = res.stdout.strip()
        return f"<b>🔝 Top Processes by Memory Usage:</b>\n<pre><code>{escape_html(out)}</code></pre>"
    except Exception as e:
        return f"Process Error: {e}"

def kill_process(pid_str):
    if not pid_str.isdigit():
        return "❌ PID harus berupa angka. Contoh: <code>/kill 1234</code>"
    try:
        res = subprocess.run(["kill", "-9", pid_str], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=5)
        if res.returncode == 0:
            return f"✅ Berhasil menghentikan proses PID {pid_str}."
        else:
            return f"❌ Gagal menghentikan PID {pid_str}: {escape_html(res.stdout.strip())}"
    except Exception as e:
        return f"❌ Error killing process: {e}"
