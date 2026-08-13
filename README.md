# 📱 Telegram Notifier Suite & Remote VPS Terminal (`notify-tele`)

Dokumentasi dan suite lengkap untuk:
1. Mengirim **notifikasi kustom berdasarkan jenis/kategori** dari VPS ke Telegram Bot.
2. Membaca **log notifikasi & status VPS secara interaktif**.
3. **Mengeksekusi perintah terminal VPS langsung dari Telegram Bot** (Remote Terminal / Shell via Telegram).

Tool ini sangat ringan (daemon RAM ~3 MB), berbasis Python standard library, dan dirancang agar mudah dipicu oleh pengguna (User) maupun AI Coding Assistant (Antigravity).

---

## 📂 Isi Folder

* `notify-tele` : Script CLI pengirim notifikasi.
* `tele-bot-daemon` : Daemon penerima & eksekutor perintah terminal dari Telegram.
* `install.sh` : Script installer otomatis.
* `telegram-boot-notify.service` : Systemd service notifikasi boot otomatis.
* `telegram-bot-daemon.service` : Systemd service daemon terminal interaktif.
* `README.md` : Dokumentasi lengkap ini.

---

## 🐚 Akses Terminal VPS Langsung dari Chat Telegram Bot

Kamu bisa mengeksekusi perintah bash / terminal VPS kamu langsung melalui chat Telegram:

### 1. Perintah Sekali Jalan (`/cmd`)
Gunakan format `/cmd <perintah>`:
* `/cmd ls -la` — Melihat isi folder saat ini.
* `/cmd systemctl status nginx` — Mengecek status service.
* `/cmd df -h` — Mengecek sisa disk.
* `/cmd free -h` — Mengecek penggunaan RAM.
* `/cd /root/projects` — Pindah ke direktori tertentu.
* `/pwd` — Melihat direktori kerja saat ini.

### 2. Mode Terminal Interaktif (`/shell`)
Ketik `/shell` di Telegram untuk mengaktifkan **Mode Terminal Interaktif**:
* Setelah aktif, **setiap teks** yang kamu ketik di Telegram akan dianggap sebagai perintah terminal dan langsung dieksekusi di VPS!
* Ketik `/shell` kembali atau `/exit` untuk mematikan mode ini.

### 3. Perintah Monitoring & System
* `/logs` atau `/logs 15` — Menampilkan riwayat log notifikasi VPS.
* `/status` — Menampilkan penggunaan RAM, Disk, Uptime & Waktu VPS.
* `/ping` — Mengecek status keaktifan VPS.

🔒 *Keamanan: Bot dikunci secara ketat dan HANYA akan merespon perintah yang dikirim oleh Chat ID milik kamu (`5743328578`).*

---

## 🚀 Cara Setup di VPS Baru (Migration / Clean Install)

Jika kamu berpindah ke VPS baru, cukup clone repo ini ke VPS baru, lalu jalankan:

```bash
git clone git@github.com:fatahilah-mr/telegram-notifier.git
cd telegram-notifier
bash install.sh
```

Kemudian hubungkan ke Telegram Bot kamu:

```bash
notify-tele --set-config --token "BOT_TOKEN_KAMU" --chatid "CHAT_ID_KAMU"
```

*(Konfigurasi Token & Chat ID tersimpan aman di `~/.telegram_config`)*

---

## ⚡ Detail Spesifikasi Teknis
* **Bahasa**: Python 3 (standard library).
* **Daemon RAM Usage**: Hanya **~1.5 MB - 3 MB** saja.
* **Security**: Strict Owner Chat ID Verification.
