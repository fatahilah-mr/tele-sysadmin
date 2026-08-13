# 📱 Telegram Notifier Suite & Bot Commands (`notify-tele`)

Dokumentasi dan suite lengkap untuk:
1. Mengirim **notifikasi kustom berdasarkan jenis/kategori** dari VPS ke Telegram Bot.
2. Membaca **log notifikasi & status VPS secara interaktif langsung dari chat Telegram Bot** (tanpa perlu membuka VPS).

Tool ini sangat ringan (daemon RAM ~3 MB), berbasis Python standard library, dan dirancang agar mudah dipicu oleh pengguna (User) maupun AI Coding Assistant (Antigravity).

---

## 📂 Isi Folder

* `notify-tele` : Script CLI pengirim notifikasi.
* `tele-bot-daemon` : Daemon penerima perintah interaktif dari Telegram.
* `install.sh` : Script installer otomatis.
* `telegram-boot-notify.service` : Systemd service notifikasi boot otomatis.
* `telegram-bot-daemon.service` : Systemd service daemon bot interaktif.
* `README.md` : Dokumentasi lengkap ini.

---

## 🤖 Perintah Interaktif Langsung dari Telegram Bot

Kamu bisa mengetikkan perintah berikut langsung di obrolan Bot Telegram kamu di HP/Desktop:

| Perintah | Deskripsi |
| :--- | :--- |
| `/logs` atau `/logs 15` | Menampilkan riwayat log notifikasi VPS terbaru |
| `/status` | Menampilkan penggunaan RAM, Disk (/), Uptime & Waktu VPS |
| `/ping` | Mengecek apakah VPS aktif & merespon |
| `/help` | Menampilkan menu bantuan perintah |

🔒 *Keamanan: Bot hanya akan merespon perintah yang dikirim oleh Chat ID milik kamu.*

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

## 📋 Panduan Penggunaan CLI di VPS

Format dasar perintah:
```bash
notify-tele [kategori] "[Judul]" "[Pesan Detail]"
```

### Kategori Bawaan

| Kategori | Emoji | Contoh Perintah |
| :--- | :---: | :--- |
| `success` | ✅ | `notify-tele success "Backup OK" "Database berhasil di-backup."` |
| `error` | ❌ | `notify-tele error "Build Error" "Terdapat syntax error pada index.js."` |
| `warning` | ⚠️ | `notify-tele warning "RAM Menipis" "Penggunaan RAM mencapai 90%."` |
| `info` | ℹ️ | `notify-tele info "Update Info" "Server akan maintenance jam 12 malam."` |
| `task` | 🚀 | `notify-tele task "Refactor Finished" "Semua file telah diperbarui."` |
| `deploy` | 🎉 | `notify-tele deploy "Deploy Selesai" "App v2.0 live di production."` |
| `security` | 🔒 | `notify-tele security "SSH Alert" "Login baru terdeteksi dari IP X."` |
| `database` | 🗄️ | `notify-tele database "Migration Done" "Tabel users berhasil di-migrate."` |
| `backup` | 💾 | `notify-tele backup "Auto Backup" "Snapshot VPS tersimpan."` |
| `cron` | ⏰ | `notify-tele cron "Clean Temp" "File temp berhasil dibersihkan."` |
| `server` | 🖥️ | `notify-tele server "Reboot Done" "Server selesai dipulihkan."` |

---

## ⚡ Detail Spesifikasi Teknis
* **Bahasa**: Python 3 (standard library).
* **Daemon RAM Usage**: Hanya **~3 MB** saja.
* **Security**: Enforces Chat ID verification.
