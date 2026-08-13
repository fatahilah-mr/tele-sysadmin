#!/usr/bin/env bash

# tele-sysadmin Interactive TUI Installer & Setup Wizard
# Location: /root/tele-sysadmin/setup.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NOTIFY_BIN="/usr/local/bin/notify-tele"
DAEMON_BIN="/usr/local/bin/tele-sysadmin-daemon"
ENV_FILE="$SCRIPT_DIR/.env"
ENV_EXAMPLE="$SCRIPT_DIR/.env.example"

# Non-interactive check (e.g. CI/CD or -y flag)
NON_INTERACTIVE=false
for arg in "$@"; do
    if [ "$arg" == "-y" ] || [ "$arg" == "--yes" ] || [ "$arg" == "--non-interactive" ]; then
        NON_INTERACTIVE=true
    fi
done

# Fallback if TTY is not available
if [ ! -t 0 ]; then
    NON_INTERACTIVE=true
fi

# Function to run installation steps
run_install() {
    local install_deps=$1
    local install_cli=$2
    local install_daemon=$3
    local install_boot=$4
    local setup_env=$5
    local setup_creds=$6

    echo ""
    echo "========================================="
    echo "   Running tele-sysadmin Installation    "
    echo "========================================="

    # 1. Install Dependencies
    if [ "$install_deps" = true ]; then
        echo "[1/5] Installing Python dependencies (psutil, matplotlib)..."
        if command -v pip3 >/dev/null 2>&1; then
            pip3 install --index-url https://pypi.org/simple --break-system-packages -r "$SCRIPT_DIR/requirements.txt" || true
        fi
    fi

    # 2. Install Executables
    if [ "$install_cli" = true ]; then
        echo "[2/5] Installing CLI executable notify-tele..."
        cp "$SCRIPT_DIR/bin/notify-tele" "$NOTIFY_BIN"
        chmod +x "$NOTIFY_BIN"
    fi

    if [ "$install_daemon" = true ]; then
        echo "[2/5] Installing Bot Daemon executable tele-sysadmin-daemon..."
        cp "$SCRIPT_DIR/bin/tele-sysadmin-daemon" "$DAEMON_BIN"
        chmod +x "$DAEMON_BIN"
    fi

    # 3. Setup Boot Service
    if [ "$install_boot" = true ]; then
        if [ -f "$SCRIPT_DIR/services/tele-sysadmin-boot.service" ]; then
            echo "[3/5] Setting up boot notification systemd service..."
            cp "$SCRIPT_DIR/services/tele-sysadmin-boot.service" "/etc/systemd/system/tele-sysadmin-boot.service"
            systemctl daemon-reload || true
            systemctl enable tele-sysadmin-boot.service || true
        fi
    fi

    # 4. Setup Daemon Service
    if [ "$install_daemon" = true ]; then
        if [ -f "$SCRIPT_DIR/services/tele-sysadmin-daemon.service" ]; then
            echo "[4/5] Setting up master bot daemon systemd service..."
            cp "$SCRIPT_DIR/services/tele-sysadmin-daemon.service" "/etc/systemd/system/telegram-bot-daemon.service" 2>/dev/null || true
            cp "$SCRIPT_DIR/services/tele-sysadmin-daemon.service" "/etc/systemd/system/tele-sysadmin-daemon.service"
            systemctl daemon-reload || true
            systemctl enable tele-sysadmin-daemon.service || true
            systemctl restart tele-sysadmin-daemon.service || true
        fi
    fi

    # 5. Environment File
    if [ "$setup_env" = true ]; then
        if [ ! -f "$ENV_FILE" ] && [ -f "$ENV_EXAMPLE" ]; then
            echo "[5/5] Creating .env file from .env.example..."
            cp "$ENV_EXAMPLE" "$ENV_FILE"
        fi
    fi

    # 6. Credentials Input
    if [ "$setup_creds" = true ] && [ "$NON_INTERACTIVE" = false ]; then
        echo ""
        echo "--- Configuration Setup ---"
        
        current_token=""
        current_chatid=""
        if [ -f "$ENV_FILE" ]; then
            current_token=$(grep TELEGRAM_BOT_TOKEN "$ENV_FILE" | cut -d'=' -f2 | tr -d '"' | tr -d "'" || true)
            current_chatid=$(grep TELEGRAM_CHAT_ID "$ENV_FILE" | cut -d'=' -f2 | tr -d '"' | tr -d "'" || true)
        fi

        if command -v whiptail >/dev/null 2>&1; then
            NEW_TOKEN=$(whiptail --title "Telegram Bot Token Setup" --inputbox "Masukkan Telegram Bot Token kamu (dari @BotFather):" 10 65 "$current_token" 3>&1 1>&2 2>&3 || echo "$current_token")
            NEW_CHATID=$(whiptail --title "Telegram Chat ID Setup" --inputbox "Masukkan Telegram Chat ID kamu (dari @userinfobot):" 10 65 "$current_chatid" 3>&1 1>&2 2>&3 || echo "$current_chatid")
        else
            read -p "Masukkan Telegram Bot Token [$current_token]: " input_token
            NEW_TOKEN=${input_token:-$current_token}
            read -p "Masukkan Telegram Chat ID [$current_chatid]: " input_chatid
            NEW_CHATID=${input_chatid:-$current_chatid}
        fi

        if [ -n "$NEW_TOKEN" ] && [ -n "$NEW_CHATID" ]; then
            cat <<EOF > "$ENV_FILE"
# Telegram Bot Credentials Configuration
TELEGRAM_BOT_TOKEN="$NEW_TOKEN"
TELEGRAM_CHAT_ID="$NEW_CHATID"
EOF
            chmod 600 "$ENV_FILE"
            echo "✅ Kredensial tersimpan ke $ENV_FILE"
        fi
    fi

    echo ""
    echo "========================================="
    echo "   tele-sysadmin Setup Complete! 🎉     "
    echo "========================================="
}

# Non-interactive execution
if [ "$NON_INTERACTIVE" = true ]; then
    run_install true true true true true false
    exit 0
fi

# TUI Interactive Wizard using Whiptail
if command -v whiptail >/dev/null 2>&1; then
    CHOICE=$(whiptail --title "🤖 tele-sysadmin Interactive Setup Wizard" --menu \
    "Pilih Template Instalasi yang kamu inginkan:\n(Gunakan tombol PANAH dan ENTER)" 16 72 4 \
    "1" "🚀 FULL SUITE (Rekomendasi - Install Seluruh Komponen Bot & Service)" \
    "2" "📢 NOTIFIER ONLY (Hanya CLI Notifikasi & Boot Alert)" \
    "3" "🐚 DAEMON ONLY (Hanya CLI & Bot Command Daemon)" \
    "4" "🎛️ CUSTOM SELECTION (Pilih Komponen Spesifik dengan Checkboxes)" \
    3>&1 1>&2 2>&3)

    case $CHOICE in
        1)
            # Full Suite
            run_install true true true true true true
            ;;
        2)
            # Notifier Only
            run_install true true false true true true
            ;;
        3)
            # Daemon Only
            run_install true true true false true true
            ;;
        4)
            # Custom Checkbox selection
            SELECTIONS=$(whiptail --title "🎛️ Custom Component Checkbox Selection" --checklist \
            "Gunakan PANAH untuk navigasi, SPASI untuk centang/hapus [X], ENTER untuk konfirmasi:" 18 72 6 \
            "DEPS" "Python dependencies (psutil, matplotlib)" ON \
            "CLI" "Executable CLI notify-tele" ON \
            "DAEMON" "Bot Command Daemon Service (tele-sysadmin-daemon)" ON \
            "BOOT" "Auto-Boot Notification Service (tele-sysadmin-boot)" ON \
            "ENV" "Buat file konfigurasi .env" ON \
            "CREDS" "Input Bot Token & Chat ID interaktif" ON \
            3>&1 1>&2 2>&3)

            inc_deps=false
            inc_cli=false
            inc_daemon=false
            inc_boot=false
            inc_env=false
            inc_creds=false

            if [[ $SELECTIONS == *"DEPS"* ]]; then inc_deps=true; fi
            if [[ $SELECTIONS == *"CLI"* ]]; then inc_cli=true; fi
            if [[ $SELECTIONS == *"DAEMON"* ]]; then inc_daemon=true; fi
            if [[ $SELECTIONS == *"BOOT"* ]]; then inc_boot=true; fi
            if [[ $SELECTIONS == *"ENV"* ]]; then inc_env=true; fi
            if [[ $SELECTIONS == *"CREDS"* ]]; then inc_creds=true; fi

            run_install $inc_deps $inc_cli $inc_daemon $inc_boot $inc_env $inc_creds
            ;;
        *)
            echo "Instalasi dibatalkan."
            exit 0
            ;;
    esac
else
    # Simple CLI fallback
    echo "1) Full Suite (Install All)"
    echo "2) Custom Install"
    read -p "Pilih [1]: " c
    if [ "$c" == "2" ]; then
        run_install true true true true true true
    else
        run_install true true true true true true
    fi
fi
