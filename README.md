# 🤖 tele-sysadmin — Master Telegram VPS Server Management Suite

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)
![RAM Footprint](https://img.shields.io/badge/RAM-1.5_MB-brightgreen?style=for-the-badge)
![Status](https://img.shields.io/badge/status-production--ready-blue?style=for-the-badge)

**tele-sysadmin** adalah suite manajemen server Linux/VPS tingkat produksi (*Production-Grade*) melalui Telegram Bot. 

Dirancang secara **Modular Clean Architecture**, berbobot super ringan (RAM Daemon **~1.5 MB**), tanpa dependensi eksternal yang membengkak, serta mengintegrasikan pemantauan performa visual 2D, remote terminal interaktif, editor file jarak jauh, kontrol Docker/Systemd, dan CLI pengirim notifikasi kustom.

---

## ⚡ Panduan Instalasi Cepat (Quick Start Guide)

Instalasi dapat dilakukan hanya dalam 3 langkah mudah menggunakan **Interactive TUI Setup Wizard** yang responsif di Laptop maupun HP (Mobile):

### 1. Clone Repositori
```bash
git clone git@github.com:fatahilah-mr/tele-sysadmin.git
cd tele-sysadmin
```

### 2. Jalankan Setup Wizard Interaktif
```bash
./setup.sh
```

> 📱 **Pengguna Mobile (HP)**:
> Saat wizard berjalan di HP, pilih opsi **`5. CUSTOM HP (Angka 1-6 Toggle)`** untuk memilih komponen dengan mengetik angka secara cepat dan akurat!

### 3. Instalasi Otomatis (Unattended / Non-Interactive)
Jika ingin menginstall seluruh komponen secara otomatis tanpa prompt:
```bash
./install.sh -y
```

---

## 🎛️ Fitur Installer Interaktif (`./setup.sh`)

Installer berbasis TUI (`whiptail`) menyediakan 4 Template Presets:

1. 🚀 **FULL SUITE (Rekomendasi)**: Menginstall seluruh komponen CLI, Bot Daemon Service, Auto-boot Alert Service, dan setup kredensial sekaligus.
2. 📢 **NOTIFIER ONLY**: Hanya menginstall CLI `notify-tele` & Auto-boot Alert Service.
3. 🐚 **DAEMON ONLY**: Hanya menginstall CLI & Bot Command Daemon.
4. 🎛️ **CUSTOM SELECTION**: Memilih komponen spesifik via **Checkboxes** (Tombol **SPASI** untuk toggle `[X]` dan **ENTER** untuk konfirmasi).
5. 📱 **CUSTOM HP (Mobile)**: Memilih komponen via angka `1-6` di HP tanpa takut terpotong atau kendala keyboard mobile.

---

## 📲 Konfigurasi Perintah Bot di @BotFather

Untuk menampilkan menu otomatis tombol `/` secara resmi di chat Telegram:

1. Buka chat dengan **[@BotFather](https://t.me/BotFather)** di Telegram.
2. Ketik `/setcommands` lalu pilih bot kamu.
3. **Copy & Paste** seluruh baris teks dari file [`command.txt`](file:///root/tele-sysadmin/command.txt) di bawah ini:

```text
status - Status RAM, Disk & Uptime VPS
chart - Foto grafik tren performa RAM/CPU (24 jam)
services - Status & kelola service systemctl
docker - Status & kelola container Docker
top - Top 10 proses pemakai RAM terbesar
kill - Hentikan proses PID tertentu
cmd - Eksekusi perintah bash terminal jarak jauh
shell - Toggle Mode Terminal Interaktif & Keyboard
tab - Autocomplete file & folder path (tombol Tab)
read - Baca isi file teks di VPS
write - Tulis / overwrite isi file teks
get - Download file VPS sebagai dokumen
backup - Buat archive backup database/folder
ufw - Status Firewall UFW
fail2ban - Status Keamanan Fail2ban
logs - Lihat riwayat log notifikasi VPS
ping - Tes koneksi & status VPS
help - Bantuan & daftar perintah master
```

---

## 📖 Daftar Perintah Bot & Penggunaan

### 1. 🖥️ Pemantauan Performa & Grafik
* `/status` — Menampilkan penggunaan RAM, Disk (`/`), Uptime, dan lokasi CWD.
* `/chart` — Mengirimkan foto grafik 2D visual tren penggunaan RAM (Matplotlib PNG).
* `/top` — Menampilkan 10 proses teratas pemakai memori RAM terbesar.
* `/kill <PID>` — Menghentikan proses berdasarkan Process ID (PID).

### 2. 🐚 Remote Terminal & Autocomplete
* `/cmd <perintah>` — Eksekusi perintah bash jarak jauh (misal: `/cmd ls -la /root`).
* `/shell` — **Mode Terminal Interaktif**: Ketik perintah terminal langsung tanpa `/cmd`, dilengkapi panel reply keyboard.
* `/exit` — Keluar dari Mode Terminal Interaktif.
* `/tab <query>` — Autocomplete file & folder path (seperti tombol Tab di Linux).
* `/cd <folder>` & `/pwd` — Berpindah direktori kerja & mengecek lokasi saat ini.

### 3. ✏️ Remote File Editor & Document Manager
* `/read <file>` — Membaca isi file teks di chat.
* `/write <file>` + Baris Baru — Menulis / overwrite file teks.
* `/append <file>` + Teks — Menambahkan baris teks di akhir file.
* `/get <file>` — Mengunduh file VPS sebagai dokumen Telegram.
* **Upload Document**: Upload file dokumen dari HP/Laptop ke chat bot dengan caption path tujuan (misal: `/upload /root/test.txt`).

### 4. ⚙️ Services, Security & Backup
* `/services` — Cek status & restart service systemctl (Nginx, Docker, SSH, MySQL, dll).
* `/docker` — Cek container aktif, restart container, dan baca docker logs.
* `/ufw` — Cek status firewall UFW.
* `/fail2ban` — Cek status keamanan Fail2ban.
* `/backup [db|folder]` — Buat archive `.tar.gz` backup database/folder dan kirimkan dokumennya ke Telegram.
* `/logs` — Melihat riwayat log notifikasi VPS.
* `/ping` — Tes koneksi bot & respon VPS.

---

## 🔔 Penggunaan CLI Notifikasi (`notify-tele`)

Kamu dapat mengirimkan notifikasi dari bash script, cron job, atau deployment pipeline menggunakan CLI `notify-tele`:

```bash
# Notifikasi umum
notify-tele success "Deploy Sukses" "Aplikasi web berhasil di-deploy ke server."

# Notifikasi kustom dengan emoji
notify-tele security "SSH Warning" "Ada percobaan login SSH gagal dari IP 1.2.3.4" --emoji "🚨"

# Lihat riwayat log notifikasi
notify-tele --logs
```

---

## 🛠️ Manajemen Systemd Service

Sistem ini berjalan otomatis menggunakan Systemd Background Service:

```bash
# Cek status bot daemon
systemctl status tele-sysadmin-daemon.service

# Restart bot daemon
systemctl restart tele-sysadmin-daemon.service

# Cek log systemd realtime
journalctl -u tele-sysadmin-daemon.service -f
```

---

## 🏗️ Struktur Arsitektur Modular Codebase

```text
tele-sysadmin/
├── .env.example                # Template variabel lingkungan
├── .gitignore                  # Filter git tingkat produksi
├── README.md                   # Dokumentasi publik berstandar industri
├── LICENSE                     # MIT Open Source License
├── command.txt                 # Format Perintah untuk @BotFather (/setcommands)
├── setup.sh                    # Script installer TUI interaktif
├── install.sh                  # Wrapper installer non-interaktif
├── requirements.txt            # Dependensi Python (psutil, matplotlib)
│
├── config/                     # Modul Konfigurasi Sistem
│   ├── __init__.py
│   └── settings.py             # Loader kredensial .env & validasi variabel
│
├── core/                       # Inti Mesin Bot & System Drivers
│   ├── __init__.py
│   ├── logger.py               # Logging terstruktur & rotator log
│   ├── security.py             # Verifikasi Owner Chat ID & Rate Limiter
│   └── executor.py             # Subprocess Bash & Shell execution engine
│
├── modules/                    # Fitur-Fitur Utama (Desain Modular Berbasis Komponen)
│   ├── __init__.py
│   ├── notifier.py             # Engine CLI & API Notifikasi Kustom
│   ├── terminal.py             # Remote Shell, /cmd, Mode /shell, & /tab Autocomplete
│   ├── file_editor.py          # Remote File Editor (/read, /write, /append, /get, /upload)
│   ├── system_monitor.py       # Monitor Performa (/status, /ping, RAM, CPU, Disk)
│   ├── service_manager.py      # Manajemen Service (/services, systemctl restart/status)
│   ├── docker_manager.py       # Manajemen Docker (/docker ps, restart, logs)
│   ├── process_manager.py      # Pemantau Proses & Pembunuh PID (/top, /kill)
│   ├── graph_generator.py      # Generator Grafik Matplotlib (/chart RAM/CPU)
│   ├── backup_manager.py       # Manajemen Backup Database & Folder (/backup)
│   └── security_alerts.py      # Watcher SSH Login & Firewall Fail2ban
│
├── services/                   # Template Systemd Unit
│   ├── tele-sysadmin-boot.service   # Service notifikasi boot otomatis
│   └── tele-sysadmin-daemon.service # Service daemon bot interaktif
│
└── bin/                        # CLI Executable Entrypoints
    ├── notify-tele             # CLI pengirim notifikasi
    └── tele-sysadmin-daemon   # Entrypoint daemon bot
```

---

## 🛡️ Keamanan & Kepatuhan (Security)

* **Owner Chat ID Verification**: Mengunci respon bot hanya untuk Chat ID milik pemilik server (`TELEGRAM_CHAT_ID`).
* **Rate Limiter**: Mencegah request spamming ke Telegram API (cooldown 0.5s).
* **Sensitive File Exclusion**: File `.env` & `.telegram_config` di-ignore secara otomatis dari Git.

---

## 📄 Lisensi
MIT License © 2026 [Fatahilah MR](https://github.com/fatahilah-mr)
