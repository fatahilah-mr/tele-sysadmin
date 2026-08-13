#!/usr/bin/env bash

# tele-sysadmin Production Auto Installer
# Location: /root/tele-sysadmin/install.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NOTIFY_BIN="/usr/local/bin/notify-tele"
DAEMON_BIN="/usr/local/bin/tele-sysadmin-daemon"

echo "========================================="
echo "   Installing tele-sysadmin Master Suite "
echo "========================================="

if [ ! -f "$SCRIPT_DIR/bin/notify-tele" ]; then
    echo "Error: bin/notify-tele file not found in $SCRIPT_DIR!"
    exit 1
fi

echo "[1/5] Installing Python dependencies..."
if command -v pip3 >/dev/null 2>&1; then
    pip3 install --index-url https://pypi.org/simple --break-system-packages -r "$SCRIPT_DIR/requirements.txt" || true
fi

echo "[2/5] Installing CLI executables to /usr/local/bin..."
cp "$SCRIPT_DIR/bin/notify-tele" "$NOTIFY_BIN"
cp "$SCRIPT_DIR/bin/tele-sysadmin-daemon" "$DAEMON_BIN"
chmod +x "$NOTIFY_BIN" "$DAEMON_BIN"

if [ -f "$SCRIPT_DIR/services/tele-sysadmin-boot.service" ]; then
    echo "[3/5] Setting up boot notification service..."
    cp "$SCRIPT_DIR/services/tele-sysadmin-boot.service" "/etc/systemd/system/tele-sysadmin-boot.service"
    systemctl daemon-reload || true
    systemctl enable tele-sysadmin-boot.service || true
fi

if [ -f "$SCRIPT_DIR/services/tele-sysadmin-daemon.service" ]; then
    echo "[4/5] Setting up master bot daemon service..."
    cp "$SCRIPT_DIR/services/tele-sysadmin-daemon.service" "/etc/systemd/system/tele-sysadmin-daemon.service"
    systemctl daemon-reload || true
    systemctl enable tele-sysadmin-daemon.service || true
    systemctl restart tele-sysadmin-daemon.service || true
fi

if [ ! -f "$SCRIPT_DIR/.env" ] && [ -f "$SCRIPT_DIR/.env.example" ]; then
    echo "[5/5] Creating .env file from .env.example..."
    cp "$SCRIPT_DIR/.env.example" "$SCRIPT_DIR/.env"
fi

echo ""
echo "========================================="
echo "   tele-sysadmin installation complete!  "
echo "========================================="
echo "Configure credentials in .env or run:"
echo "  notify-tele --set-config --token \"YOUR_BOT_TOKEN\" --chatid \"YOUR_CHAT_ID\""
echo "========================================="
