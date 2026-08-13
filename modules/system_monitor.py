import subprocess
from datetime import datetime

def get_system_status(session_cwd="~"):
    try:
        uptime = subprocess.check_output(["uptime", "-p"]).decode().strip()
        free_out = subprocess.check_output(["free", "-h"]).decode()
        mem_line = [line for line in free_out.splitlines() if line.startswith("Mem:")][0].split()
        mem_total, mem_used, mem_avail = mem_line[1], mem_line[2], mem_line[6]

        df_out = subprocess.check_output(["df", "-h", "/"]).decode()
        disk_line = df_out.splitlines()[1].split()
        disk_total, disk_used, disk_avail, disk_pct = disk_line[1], disk_line[2], disk_line[3], disk_line[4]

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        status_text = (
            "<b>🖥️ Status VPS Debian:</b>\n\n"
            f"⏱️ <b>Uptime:</b> {uptime}\n"
            f"🧠 <b>RAM:</b> Terpakai {mem_used} / Total {mem_total} (Bebas: {mem_avail})\n"
            f"💾 <b>Disk (/):</b> Terpakai {disk_used} ({disk_pct}) / Total {disk_total} (Sisa: {disk_avail})\n"
            f"📂 <b>Shell Working Dir:</b> <code>{session_cwd}</code>\n\n"
            f"<i>Waktu Server: {now}</i>"
        )
        return status_text
    except Exception as e:
        return f"Gagal mengambil status VPS: {e}"
