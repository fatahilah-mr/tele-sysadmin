#!/usr/bin/env bash

# Telegram Notifier Auto Installer
# Location: /root/telegram-notifier/install.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_BIN="/usr/local/bin/notify-tele"
DAEMON_BIN="/usr/local/bin/tele-bot-daemon"

echo "========================================="
echo "   Installing Telegram Notifier Suite    "
echo "========================================="

if [ ! -f "$SCRIPT_DIR/notify-tele" ]; then
    echo "Error: notify-tele file not found in $SCRIPT_DIR!"
    exit 1
fi

echo "[1/4] Copying notify-tele to $TARGET_BIN..."
cp "$SCRIPT_DIR/notify-tele" "$TARGET_BIN"
chmod +x "$TARGET_BIN"

if [ -f "$SCRIPT_DIR/tele-bot-daemon" ]; then
    echo "[2/4] Copying tele-bot-daemon to $DAEMON_BIN..."
    cp "$SCRIPT_DIR/tele-bot-daemon" "$DAEMON_BIN"
    chmod +x "$DAEMON_BIN"
fi

if [ -f "$SCRIPT_DIR/telegram-boot-notify.service" ]; then
    echo "[3/4] Setting up automatic boot notification service..."
    cp "$SCRIPT_DIR/telegram-boot-notify.service" "/etc/systemd/system/telegram-boot-notify.service"
    systemctl daemon-reload || true
    systemctl enable telegram-boot-notify.service || true
fi

if [ -f "$SCRIPT_DIR/telegram-bot-daemon.service" ]; then
    echo "[4/4] Setting up Telegram bot command daemon service..."
    cp "$SCRIPT_DIR/telegram-bot-daemon.service" "/etc/systemd/system/telegram-bot-daemon.service"
    systemctl daemon-reload || true
    systemctl enable telegram-bot-daemon.service || true
    systemctl restart telegram-bot-daemon.service || true
fi

if [ ! -f "$SCRIPT_DIR/.env" ] && [ -f "$SCRIPT_DIR/.env.example" ]; then
    echo "[Config] Creating .env file from .env.example..."
    cp "$SCRIPT_DIR/.env.example" "$SCRIPT_DIR/.env"
fi

echo ""
echo "Installation complete!"
echo "Next step: Set your credentials in .env file or run:"
echo "  notify-tele --set-config --token \"YOUR_BOT_TOKEN\" --chatid \"YOUR_CHAT_ID\""
echo "========================================="
