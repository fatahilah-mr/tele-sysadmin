import os
import subprocess
from datetime import datetime
from core.executor import escape_html

def create_backup(target_type="db"):
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = os.path.expanduser("~/backups")
    os.makedirs(backup_dir, exist_ok=True)

    if target_type in ["db", "database"]:
        backup_file = os.path.join(backup_dir, f"backup_db_{now}.tar.gz")
        # Backup /var/lib or dump
        cmd = f"tar -czf {backup_file} /root/tele-sysadmin/ 2>/dev/null || true"
        try:
            res = subprocess.run(cmd, shell=True, timeout=30)
            size = os.path.getsize(backup_file) if os.path.exists(backup_file) else 0
            return True, f"✅ Backup database/config berhasil disimpan ke <code>{backup_file}</code> ({size/1024:.1f} KB).", backup_file
        except Exception as e:
            return False, f"❌ Error backup: {e}", None
    else:
        backup_file = os.path.join(backup_dir, f"backup_full_{now}.tar.gz")
        cmd = f"tar -czf {backup_file} /root/tele-sysadmin/ 2>/dev/null || true"
        try:
            res = subprocess.run(cmd, shell=True, timeout=30)
            size = os.path.getsize(backup_file) if os.path.exists(backup_file) else 0
            return True, f"✅ Backup folder berhasil disimpan ke <code>{backup_file}</code> ({size/1024:.1f} KB).", backup_file
        except Exception as e:
            return False, f"❌ Error backup: {e}", None
