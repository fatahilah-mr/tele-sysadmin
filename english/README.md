# 🤖 tele-sysadmin — Master Telegram VPS Server Management Suite

[![Read in Indonesian](https://img.shields.io/badge/Language-Indonesian-red?style=for-the-badge&logo=google-translate)](../README.md)
![Python Version](https://img.shields.io/badge/python-3.10%2B-blue?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)
![RAM Footprint](https://img.shields.io/badge/RAM-1.5_MB-brightgreen?style=for-the-badge)
![Status](https://img.shields.io/badge/status-production--ready-blue?style=for-the-badge)

**tele-sysadmin** is a production-grade Linux VPS server management suite via Telegram Bot. 

Built with a **Modular Clean Architecture**, super lightweight footprint (Daemon RAM usage **~1.5 MB**), zero bloated external dependencies, visual 2D performance tracking, interactive remote terminal, remote file editor, Docker/Systemd management, and customizable CLI notification engine.

---

## ⚡ Quick Start Installation Guide

Installation can be completed in 3 easy steps using the responsive **Interactive TUI Setup Wizard** on Laptop or Mobile devices:

### 1. Clone Repository
```bash
git clone git@github.com:fatahilah-mr/tele-sysadmin.git
cd tele-sysadmin
```

### 2. Run Interactive Setup Wizard
```bash
./setup.sh
```

> 📱 **Mobile Users (Smartphone)**:
> When running the wizard on mobile devices, select option **`5. CUSTOM HP (Numeric 1-6 Toggle)`** to quickly and accurately toggle components by typing numbers!

### 3. Automated Non-Interactive Installation
To automatically install all components silently without prompts:
```bash
./install.sh -y
```

---

## 🎛️ Interactive Setup Wizard Features (`./setup.sh`)

The TUI installer (`whiptail`) offers 4 Preset Templates:

1. 🚀 **FULL SUITE (Recommended)**: Installs all CLI tools, Bot Daemon Service, Auto-boot Alert Service, and configures credentials.
2. 📢 **NOTIFIER ONLY**: Installs only the `notify-tele` CLI tool & Auto-boot Alert Service.
3. 🐚 **DAEMON ONLY**: Installs only the CLI tool & Bot Command Daemon.
4. 🎛️ **CUSTOM SELECTION**: Select specific components via **Checkboxes** (Press **SPACEBAR** to toggle `[X]` and **ENTER** to confirm).
5. 📱 **CUSTOM HP (Mobile)**: Select components via numbers `1-6` on mobile SSH clients.

---

## 📲 @BotFather Command Menu Configuration

To officially register the command menu (`/` button) in Telegram:

1. Open a chat with **[@BotFather](https://t.me/BotFather)** on Telegram.
2. Type `/setcommands` and select your bot.
3. **Copy & Paste** all lines from the [`command.txt`](../command.txt) file below:

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

## 📖 Bot Commands Reference & Usage

### 1. 🖥️ Performance & Visual Charts
* `/status` — Displays RAM usage, Disk (`/`), Uptime, and current working directory.
* `/chart` — Sends a visual 2D RAM usage trend chart photo (Matplotlib PNG).
* `/top` — Displays top 10 memory-consuming processes.
* `/kill <PID>` — Terminates a process by its Process ID (PID).

### 2. 🐚 Remote Terminal & Autocomplete
* `/cmd <command>` — Executes remote bash commands (e.g. `/cmd ls -la /root`).
* `/shell` — **Interactive Terminal Mode**: Type terminal commands directly without `/cmd`, equipped with a custom reply keyboard.
* `/exit` — Exits Interactive Terminal Mode.
* `/tab <query>` — Autocompletes file & folder paths (like Linux Tab key).
* `/cd <folder>` & `/pwd` — Navigates working directory & checks current path.

### 3. ✏️ Remote File Editor & Document Manager
* `/read <file>` — Reads text file content directly in chat.
* `/write <file>` + New Lines — Writes / overwrites a text file.
* `/append <file>` + Text — Appends text lines to the end of a file.
* `/get <file>` — Downloads a server file directly as a Telegram document.
* **Upload Document**: Upload document files from mobile/laptop with a target path caption (e.g. `/upload /root/test.txt`).

### 4. ⚙️ Services, Security & Backup
* `/services` — Checks status & restarts systemctl services (Nginx, Docker, SSH, MySQL, etc.).
* `/docker` — Checks active containers, restarts containers, and views docker logs.
* `/ufw` — Checks UFW firewall status.
* `/fail2ban` — Checks Fail2ban security status.
* `/backup [db|folder]` — Creates `.tar.gz` archive of databases/folders and sends the document to Telegram.
* `/logs` — Views notification log history.
* `/ping` — Tests bot connection & server response.

---

## 🔔 CLI Notification Usage (`notify-tele`)

You can send notifications from bash scripts, cron jobs, or deployment pipelines using the `notify-tele` CLI:

```bash
# Basic notification
notify-tele success "Deployment Complete" "Web app deployed successfully."

# Custom notification with emoji
notify-tele security "SSH Warning" "Failed SSH login attempt from IP 1.2.3.4" --emoji "🚨"

# View notification history
notify-tele --logs
```

---

## 🛠️ Systemd Service Management

The bot runs automatically in the background using Systemd Services:

```bash
# Check bot daemon status
systemctl status tele-sysadmin-daemon.service

# Restart bot daemon
systemctl restart tele-sysadmin-daemon.service

# View realtime systemd logs
journalctl -u tele-sysadmin-daemon.service -f
```

---

## 🏗️ Modular Codebase Architecture

```text
tele-sysadmin/
├── .env.example                # Environment variables template
├── .gitignore                  # Production gitignore
├── README.md                   # Indonesian main documentation
├── english/
│   └── README.md               # English documentation
├── LICENSE                     # MIT Open Source License
├── command.txt                 # BotFather command list (/setcommands)
├── setup.sh                    # Interactive TUI setup wizard
├── install.sh                  # Non-interactive installer wrapper
├── requirements.txt            # Python dependencies (psutil, matplotlib)
│
├── config/                     # Configuration Module
│   ├── __init__.py
│   └── settings.py             # Kredensial loader & env validator
│
├── core/                       # Core Engine & System Drivers
│   ├── __init__.py
│   ├── logger.py               # Structured logger & log history
│   ├── security.py             # Owner Chat ID verification & Rate Limiter
│   └── executor.py             # Subprocess Bash & Shell execution engine
│
├── modules/                    # Main Feature Modules
│   ├── __init__.py
│   ├── notifier.py             # Notification CLI & API Engine
│   ├── terminal.py             # Remote Shell, /cmd, /shell mode, & /tab Autocomplete
│   ├── file_editor.py          # Remote File Editor (/read, /write, /append, /get, /upload)
│   ├── system_monitor.py       # Performance Monitor (/status, /ping, RAM, CPU, Disk)
│   ├── service_manager.py      # Service Manager (/services, systemctl restart/status)
│   ├── docker_manager.py       # Docker Manager (/docker ps, restart, logs)
│   ├── process_manager.py      # Process Monitor & PID Killer (/top, /kill)
│   ├── graph_generator.py      # Matplotlib Graph Generator (/chart RAM/CPU)
│   ├── backup_manager.py       # Backup Manager (/backup)
│   └── security_alerts.py      # Security Alerts Watcher (UFW / Fail2ban)
│
├── services/                   # Systemd Unit Templates
│   ├── tele-sysadmin-boot.service   # Auto boot notification service
│   └── tele-sysadmin-daemon.service # Master bot daemon service
│
└── bin/                        # CLI Executable Entrypoints
    ├── notify-tele             # Notification CLI executable
    └── tele-sysadmin-daemon   # Bot daemon executable
```

---

## 🛡️ Security & Compliance

* **Owner Chat ID Verification**: Restricts bot access strictly to the server owner (`TELEGRAM_CHAT_ID`).
* **Rate Limiter**: Prevents request spamming to the Telegram API (0.5s cooldown).
* **Sensitive File Exclusion**: `.env` & `.telegram_config` are strictly ignored by Git.

---

## 📄 License
MIT License © 2026 [Fatahilah MR](https://github.com/fatahilah-mr)
