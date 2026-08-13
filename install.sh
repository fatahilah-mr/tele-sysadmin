#!/usr/bin/env bash

# tele-sysadmin Installer Wrapper
# Location: /root/tele-sysadmin/install.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec "$SCRIPT_DIR/setup.sh" "$@"
