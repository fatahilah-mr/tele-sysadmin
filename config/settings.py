import os
import sys

CONFIG_PATHS = [
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"),
    os.path.expanduser("~/tele-sysadmin/.env"),
    os.path.expanduser("~/telegram-notifier/.env"),
    os.path.expanduser("~/.env"),
    os.path.expanduser("~/.telegram_config"),
]

def load_config():
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")

    for path in CONFIG_PATHS:
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#") and "=" in line:
                            k, v = line.split("=", 1)
                            k, v = k.strip(), v.strip().strip('"').strip("'")
                            if k == "TELEGRAM_BOT_TOKEN" and not bot_token:
                                bot_token = v
                            elif k == "TELEGRAM_CHAT_ID" and not chat_id:
                                chat_id = v
            except Exception:
                pass

    return bot_token, chat_id

def get_bot_token():
    token, _ = load_config()
    return token

def get_chat_id():
    _, chat_id = load_config()
    return chat_id

def save_config(bot_token, chat_id, target_env=None):
    save_path = target_env or os.path.expanduser("~/tele-sysadmin/.env")
    parent_dir = os.path.dirname(save_path)
    if parent_dir and not os.path.exists(parent_dir):
        os.makedirs(parent_dir, exist_ok=True)

    with open(save_path, "w", encoding="utf-8") as f:
        f.write(f'TELEGRAM_BOT_TOKEN="{bot_token}"\n')
        f.write(f'TELEGRAM_CHAT_ID="{chat_id}"\n')
    os.chmod(save_path, 0o600)
    print(f"Config saved to {save_path}")

    # Also sync to ~/.telegram_config for fallback
    try:
        fallback = os.path.expanduser("~/.telegram_config")
        with open(fallback, "w", encoding="utf-8") as f:
            f.write(f'TELEGRAM_BOT_TOKEN="{bot_token}"\n')
            f.write(f'TELEGRAM_CHAT_ID="{chat_id}"\n')
        os.chmod(fallback, 0o600)
    except Exception:
        pass
