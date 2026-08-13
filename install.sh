#!/usr/bin/env bash

# Telegram Notifier Auto Installer
# Location: /root/telegram-notifier/install.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_BIN="/usr/local/bin/notify-tele"

echo "========================================="
echo "   Installing Telegram Notifier CLI      "
echo "========================================="

if [ ! -f "$SCRIPT_DIR/notify-tele" ]; then
    echo "Error: notify-tele file not found in $SCRIPT_DIR!"
    exit 1
fi

echo "[1/2] Copying notify-tele to $TARGET_BIN..."
cp "$SCRIPT_DIR/notify-tele" "$TARGET_BIN"
chmod +x "$TARGET_BIN"

echo "[2/2] Installation complete!"
echo ""
echo "Next step: Configure your Bot Token & Chat ID by running:"
echo "  notify-tele --set-config --token \"YOUR_BOT_TOKEN\" --chatid \"YOUR_CHAT_ID\""
echo ""
echo "Or test help command:"
echo "  notify-tele --help"
echo "========================================="
