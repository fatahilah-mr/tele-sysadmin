import os
import subprocess
from datetime import datetime
from modules.notifier import get_dynamic_server_info

def get_system_status(session_cwd="~"):
    try:
        server_identity = get_dynamic_server_info()
        uptime = subprocess.check_output(["uptime", "-p"]).decode().strip()
        free_out = subprocess.check_output(["free", "-h"]).decode()
        mem_line = [line for line in free_out.splitlines() if line.startswith("Mem:")][0].split()
        mem_total, mem_used, mem_avail = mem_line[1], mem_line[2], mem_line[6]

        df_out = subprocess.check_output(["df", "-h", "/"]).decode()
        disk_line = df_out.splitlines()[1].split()
        disk_total, disk_used, disk_avail, disk_pct = disk_line[1], disk_line[2], disk_line[3], disk_line[4]

        # Get Load Average & CPU Cores dynamically
        load_avg = os.getloadavg() if hasattr(os, "getloadavg") else (0.0, 0.0, 0.0)
        cpu_count = os.cpu_count() or 1

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        status_text = (
            f"<b>🖥️ Status Server ({server_identity}):</b>\n\n"
            f"⏱️ <b>Uptime:</b> {uptime}\n"
            f"⚡ <b>CPU Load (1/5/15m):</b> {load_avg[0]:.2f}, {load_avg[1]:.2f}, {load_avg[2]:.2f} ({cpu_count} Cores)\n"
            f"🧠 <b>RAM:</b> Terpakai {mem_used} / Total {mem_total} (Bebas: {mem_avail})\n"
            f"💾 <b>Disk (/):</b> Terpakai {disk_used} ({disk_pct}) / Total {disk_total} (Sisa: {disk_avail})\n"
            f"📂 <b>Working Dir:</b> <code>{session_cwd}</code>\n\n"
            f"<i>Waktu Server: {now}</i>"
        )
        return status_text
    except Exception as e:
        return f"Gagal mengambil status VPS: {e}"
