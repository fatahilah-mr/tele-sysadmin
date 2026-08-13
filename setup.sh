#!/usr/bin/env bash

# tele-sysadmin Mobile-Responsive Interactive Installer
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

if [ ! -t 0 ]; then
    NON_INTERACTIVE=true
fi

# Calculate dynamic terminal bounds (Mobile Responsive)
calc_dimensions() {
    local raw_cols=$(tput cols 2>/dev/null || echo 45)
    local raw_lines=$(tput lines 2>/dev/null || echo 20)

    BOX_WIDTH=$(( raw_cols - 4 ))
    if [ $BOX_WIDTH -gt 60 ]; then BOX_WIDTH=60; fi
    if [ $BOX_WIDTH -lt 36 ]; then BOX_WIDTH=36; fi

    BOX_HEIGHT=$(( raw_lines - 2 ))
    if [ $BOX_HEIGHT -gt 20 ]; then BOX_HEIGHT=20; fi
    if [ $BOX_HEIGHT -lt 12 ]; then BOX_HEIGHT=12; fi

    MENU_HEIGHT=$(( BOX_HEIGHT - 7 ))
    if [ $MENU_HEIGHT -lt 4 ]; then MENU_HEIGHT=4; fi
}

# Core installation logic
run_install() {
    local install_deps=$1
    local install_cli=$2
    local install_daemon=$3
    local install_boot=$4
    local setup_env=$5
    local setup_creds=$6

    clear 2>/dev/null || true
    echo "========================================="
    echo "   tele-sysadmin Installation Running   "
    echo "========================================="

    # 1. Install Dependencies
    if [ "$install_deps" = true ]; then
        echo "[1/5] Installing Python dependencies..."
        if command -v pip3 >/dev/null 2>&1; then
            pip3 install --index-url https://pypi.org/simple --break-system-packages -r "$SCRIPT_DIR/requirements.txt" || true
        fi
    fi

    # 2. Install Executables
    if [ "$install_cli" = true ]; then
        echo "[2/5] Installing CLI notify-tele..."
        cp "$SCRIPT_DIR/bin/notify-tele" "$NOTIFY_BIN"
        chmod +x "$NOTIFY_BIN"
    fi

    if [ "$install_daemon" = true ]; then
        echo "[2/5] Installing Bot Daemon tele-sysadmin-daemon..."
        cp "$SCRIPT_DIR/bin/tele-sysadmin-daemon" "$DAEMON_BIN"
        chmod +x "$DAEMON_BIN"
    fi

    # 3. Setup Boot Service
    if [ "$install_boot" = true ]; then
        if [ -f "$SCRIPT_DIR/services/tele-sysadmin-boot.service" ]; then
            echo "[3/5] Setting up boot notification service..."
            cp "$SCRIPT_DIR/services/tele-sysadmin-boot.service" "/etc/systemd/system/tele-sysadmin-boot.service"
            systemctl daemon-reload || true
            systemctl enable tele-sysadmin-boot.service || true
        fi
    fi

    # 4. Setup Daemon Service
    if [ "$install_daemon" = true ]; then
        if [ -f "$SCRIPT_DIR/services/tele-sysadmin-daemon.service" ]; then
            echo "[4/5] Setting up bot daemon service..."
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

    # 6. Credentials Setup
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
            calc_dimensions
            TMP_TOKEN=$(mktemp)
            TMP_CHATID=$(mktemp)
            whiptail --title "Bot Token Setup" --inputbox "Masukkan Bot Token dari @BotFather:" $BOX_HEIGHT $BOX_WIDTH "$current_token" 2> "$TMP_TOKEN" || echo "$current_token" > "$TMP_TOKEN"
            whiptail --title "Chat ID Setup" --inputbox "Masukkan Chat ID dari @userinfobot:" $BOX_HEIGHT $BOX_WIDTH "$current_chatid" 2> "$TMP_CHATID" || echo "$current_chatid" > "$TMP_CHATID"
            
            NEW_TOKEN=$(cat "$TMP_TOKEN")
            NEW_CHATID=$(cat "$TMP_CHATID")
            rm -f "$TMP_TOKEN" "$TMP_CHATID"
        else
            read -p "Bot Token [$current_token]: " input_token
            NEW_TOKEN=${input_token:-$current_token}
            read -p "Chat ID [$current_chatid]: " input_chatid
            NEW_CHATID=${input_chatid:-$current_chatid}
        fi

        if [ -n "$NEW_TOKEN" ] && [ -n "$NEW_CHATID" ]; then
            cat <<EOF > "$ENV_FILE"
# Telegram Bot Credentials Configuration
TELEGRAM_BOT_TOKEN="$NEW_TOKEN"
TELEGRAM_CHAT_ID="$NEW_CHATID"
EOF
            chmod 600 "$ENV_FILE"
            echo "✅ Kredensial tersimpan di $ENV_FILE"
        fi
    fi

    echo ""
    echo "========================================="
    echo "   tele-sysadmin Setup Complete! 🎉     "
    echo "========================================="
}

# Pure Bash Interactive Fallback / Text Toggle Menu
run_bash_custom_menu() {
    local opt_deps=true
    local opt_cli=true
    local opt_daemon=true
    local opt_boot=true
    local opt_env=true
    local opt_creds=true

    while true; do
        clear 2>/dev/null || true
        echo "========================================="
        echo "   🎛️ CUSTOM COMPONENT SELECTION (HP)   "
        echo "========================================="
        echo "Ketik angka [1-6] untuk toggle centang [X]:"
        echo ""
        [ "$opt_deps" = true ] && echo "  [1] [X] Python Libraries (psutil/matplotlib)" || echo "  [1] [ ] Python Libraries (psutil/matplotlib)"
        [ "$opt_cli" = true ] && echo "  [2] [X] CLI Executable (notify-tele)" || echo "  [2] [ ] CLI Executable (notify-tele)"
        [ "$opt_daemon" = true ] && echo "  [3] [X] Bot Daemon Service (tele-sysadmin-daemon)" || echo "  [3] [ ] Bot Daemon Service (tele-sysadmin-daemon)"
        [ "$opt_boot" = true ] && echo "  [4] [X] Auto-Boot Service (tele-sysadmin-boot)" || echo "  [4] [ ] Auto-Boot Service (tele-sysadmin-boot)"
        [ "$opt_env" = true ] && echo "  [5] [X] File Config (.env)" || echo "  [5] [ ] File Config (.env)"
        [ "$opt_creds" = true ] && echo "  [6] [X] Input Bot Token & Chat ID" || echo "  [6] [ ] Input Bot Token & Chat ID"
        echo ""
        echo "  [7] 🚀 MULAI INSTALASI SEKARANG"
        echo "  [0] ❌ Batal"
        echo "========================================="
        read -p "Pilihan Anda: " choice

        case $choice in
            1) opt_deps=$([ "$opt_deps" = true ] && echo false || echo true) ;;
            2) opt_cli=$([ "$opt_cli" = true ] && echo false || echo true) ;;
            3) opt_daemon=$([ "$opt_daemon" = true ] && echo false || echo true) ;;
            4) opt_boot=$([ "$opt_boot" = true ] && echo false || echo true) ;;
            5) opt_env=$([ "$opt_env" = true ] && echo false || echo true) ;;
            6) opt_creds=$([ "$opt_creds" = true ] && echo false || echo true) ;;
            7) run_install $opt_deps $opt_cli $opt_daemon $opt_boot $opt_env $opt_creds; break ;;
            0) echo "Dibatalkan."; break ;;
            *) echo "Pilihan tidak valid." ;;
        esac
    done
}

# Non-interactive execution
if [ "$NON_INTERACTIVE" = true ]; then
    run_install true true true true true false
    exit 0
fi

calc_dimensions

# TUI Interactive Wizard using Whiptail with Mobile Responsive bounds
if command -v whiptail >/dev/null 2>&1; then
    TMP_MENU=$(mktemp)
    whiptail --title "🤖 tele-sysadmin Setup" --menu \
    "Pilih Template Instalasi:\n(Gunakan PANAH & ENTER)" $BOX_HEIGHT $BOX_WIDTH $MENU_HEIGHT \
    "1" "🚀 FULL SUITE (Install Semua)" \
    "2" "📢 NOTIFIER ONLY (CLI + Boot Alert)" \
    "3" "🐚 DAEMON ONLY (CLI + Bot Daemon)" \
    "4" "🎛️ CUSTOM (Whiptail Checkbox)" \
    "5" "📱 CUSTOM HP (Angka 1-6 Toggle)" 2> "$TMP_MENU" || echo "0" > "$TMP_MENU"

    CHOICE=$(cat "$TMP_MENU")
    rm -f "$TMP_MENU"

    case $CHOICE in
        1)
            run_install true true true true true true
            ;;
        2)
            run_install true true false true true true
            ;;
        3)
            run_install true true true false true true
            ;;
        4)
            # Custom Checkbox selection using whiptail and tempfile
            TMP_CHECK=$(mktemp)
            whiptail --title "🎛️ Custom Selection" --checklist \
            "Gunakan SPASI untuk toggle [X], ENTER untuk OK:" $BOX_HEIGHT $BOX_WIDTH $MENU_HEIGHT \
            "DEPS" "Python Libraries" ON \
            "CLI" "notify-tele CLI Tool" ON \
            "DAEMON" "Master Bot Daemon" ON \
            "BOOT" "Auto-Boot Alert" ON \
            "ENV" "File Config (.env)" ON \
            "CREDS" "Token & Chat ID Setup" ON 2> "$TMP_CHECK" || echo "" > "$TMP_CHECK"

            SELECTIONS=$(cat "$TMP_CHECK")
            rm -f "$TMP_CHECK"

            if [ -z "$SELECTIONS" ]; then
                echo "Tidak ada komponen yang dipilih. Batal."
                exit 0
            fi

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
        5)
            run_bash_custom_menu
            ;;
        *)
            echo "Instalasi dibatalkan."
            exit 0
            ;;
    esac
else
    run_bash_custom_menu
fi
