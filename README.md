# 📱 Telegram Notifier CLI (`notify-tele`)

Dokumentasi dan tool sederhana untuk mengirimkan **notifikasi kustom berdasarkan jenis/kategori** dari VPS langsung ke Telegram Bot kamu.

Tool ini sangat ringan (idle RAM 0 MB), berbasis Python standard library, dan dirancang agar mudah dipicu oleh pengguna (User) maupun AI Coding Assistant (Antigravity).

---

## 📂 Isi Folder

* `notify-tele` : Script utama (Python 3 executable).
* `install.sh` : Script installer otomatis untuk menyalin `notify-tele` ke `/usr/local/bin/`.
* `README.md` : Dokumentasi lengkap ini.

---

## 🚀 Cara Setup di VPS Baru (Migration / Clean Install)

Jika kamu berpindah ke VPS baru, cukup copy folder `/root/telegram-notifier` ini ke VPS baru, lalu jalankan:

```bash
cd /root/telegram-notifier
bash install.sh
```

Kemudian hubungkan ke Telegram Bot kamu:

```bash
notify-tele --set-config --token "BOT_TOKEN_KAMU" --chatid "CHAT_ID_KAMU"
```

*(Konfigurasi Token & Chat ID tersimpan aman di `~/.telegram_config`)*

---

## 📋 Panduan Penggunaan CLI

Format dasar perintah:
```bash
notify-tele [kategori] "[Judul]" "[Pesan Detail]"
```

### 1. Menggunakan Kategori Bawaan

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

### 2. Bebas Pakai Nama Kategori Apapun
Kamu tidak dibatasi oleh kategori di atas. Bebas membuat nama kategori sendiri:
```bash
notify-tele pembayaran "Invoice #1092" "Pembayaran diterima via Transfer BCA"
```

### 3. Menyisipkan Emoji Kustom (`--emoji`)
```bash
notify-tele gajian "Bonus Masuk" "Transfer sebesar Rp 5.000.000" --emoji "💰"
```

---

## 🤖 Penggunaan Oleh AI Agent (Antigravity)

Setiap kali kamu meminta AI Agent untuk mengerjakan tugas di VPS dan ingin mendapat notifikasi saat selesai, kamu tinggal bilang:

> *"Tolong kerjakan X, kalau sudah selesai kirim notifikasi ke Telegram ya."*

AI Agent akan otomatis mengeksekusi perintah CLI `notify-tele` di latar belakang server, dan notifikasi berformat HTML beserta timestamp server akan langsung masuk ke aplikasi Telegram kamu!

---

## ⚡ Detail Spesifikasi Teknis
* **Bahasa**: Python 3 (menggunakan modul bawaan `urllib.request` & `json`, tanpa perlu install `pip`).
* **Penggunaan Memori**: Idle 0 MB. Saat dipicu hanya ~10 MB selama 0.2 detik.
* **Format Pesan**: HTML Telegram Parse Mode.
