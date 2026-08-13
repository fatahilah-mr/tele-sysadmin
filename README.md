# 🤖 tele-sysadmin — Master Telegram VPS Server Management Suite

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-production--ready-brightgreen)

**tele-sysadmin** adalah suite manajemen server Linux/VPS tingkat produksi (*Production-Grade*) melalui Telegram Bot. 

Dirancang secara **Modular Clean Architecture**, berbobot super ringan (RAM Daemon **~1.5 MB**), tanpa dependensi eksternal yang membengkak, serta mengintegrasikan pemantauan performa visual, eksekusi terminal jarak jauh, editor file interaktif, kontrol Docker/Systemd, dan notifikasi kustom.

---

## 🏗️ Struktur Arsitektur Modular Codebase

```text
tele-sysadmin/
├── .env.example                # Template variabel lingkungan
├── .gitignore                  # Filter git tingkat produksi
├── README.md                   # Dokumentasi publik berstandar industri
├── install.sh                  # Script installer otomatis 1-klik
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

## ⚡ Fitur-Fitur Utama

### 1. 🎛️ Remote VPS Terminal & Autocomplete
* `/cmd <perintah>` — Eksekusi perintah bash jarak jauh.
* `/shell` — **Mode Terminal Interaktif**: Ketik perintah langsung di chat tanpa `/cmd`, dilengkapi panel keyboard interaktif di bawah chat.
* `/tab <query>` — Autocomplete file & folder seperti tombol Tab di Linux.
* `/cd <folder>` & `/pwd` — Pindah & cek lokasi direktori kerja.

### 2. ✏️ Remote File Editor & Document Transfer
* `/read <file>` — Baca isi file teks langsung di chat.
* `/write <file>` + Isi — Tulis/overwrite file teks.
* `/append <file>` + Teks — Tambahkan baris di akhir file.
* `/get <file>` — Unduh file VPS sebagai dokumen Telegram.
* **Upload File**: Upload file dokumen dari HP/Laptop ke bot dengan caption path tujuan untuk simpan/overwrite file di VPS.

### 3. 📊 System & Service Management
* `/status` — Metrik performa (RAM, Disk, Uptime, Time).
* `/chart` — Foto grafik tren penggunaan RAM (Matplotlib 2D).
* `/services` — Cek & restart service systemctl (Nginx, Docker, SSH, MySQL, dll).
* `/docker` — Cek status container, restart, dan baca logs Docker.
* `/top` & `/kill <PID>` — Cek 10 proses teratas pemakai RAM & hentikan PID.
* `/ufw` & `/fail2ban` — Cek status firewall & keamanan Fail2ban.
* `/backup` — Buat archive backup database/folder otomatis.

---

## 🚀 Cara Install & Migration (1-Klik)

### 1. Clone & Install
```bash
git clone git@github.com:fatahilah-mr/tele-sysadmin.git
cd tele-sysadmin
bash install.sh
```

### 2. Konfigurasi Token & Chat ID
Edit file `.env` atau jalankan:
```bash
notify-tele --set-config --token "BOT_TOKEN_KAMU" --chatid "CHAT_ID_KAMU"
```

---

## 🛡️ Keamanan & Kepatuhan (Security)
* **Owner Chat ID Verification**: Mengunci respon bot hanya untuk Chat ID milik pemilik server.
* **Rate Limiter**: Mencegah request spamming ke Telegram API.
* **Sensitive File Exclusion**: File `.env` & `.telegram_config` di-ignore secara otomatis dari Git.

---

## 📄 Lisensi
MIT License © 2026 tele-sysadmin
