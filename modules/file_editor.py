import os
import sys
import json
import urllib.request
from core.executor import escape_html

def send_message(bot_token, chat_id, text, reply_markup=None):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }
    if reply_markup:
        payload["reply_markup"] = reply_markup

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            return json.loads(response.read().decode("utf-8"))
    except Exception as e:
        print(f"Error sending message: {e}", file=sys.stderr)
        return None

def send_document(bot_token, chat_id, file_path, caption=""):
    url = f"https://api.telegram.org/bot{bot_token}/sendDocument"
    if not os.path.exists(file_path):
        send_message(bot_token, chat_id, f"❌ File tidak ditemukan: <code>{file_path}</code>")
        return False

    boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
    filename = os.path.basename(file_path)

    try:
        with open(file_path, "rb") as f:
            file_content = f.read()

        body = []
        body.append(f"--{boundary}".encode("utf-8"))
        body.append(f'Content-Disposition: form-data; name="chat_id"'.encode("utf-8"))
        body.append(b"")
        body.append(str(chat_id).encode("utf-8"))

        if caption:
            body.append(f"--{boundary}".encode("utf-8"))
            body.append(f'Content-Disposition: form-data; name="caption"'.encode("utf-8"))
            body.append(b"")
            body.append(caption.encode("utf-8"))

        body.append(f"--{boundary}".encode("utf-8"))
        body.append(f'Content-Disposition: form-data; name="document"; filename="{filename}"'.encode("utf-8"))
        body.append(b"Content-Type: application/octet-stream")
        body.append(b"")
        body.append(file_content)

        body.append(f"--{boundary}--".encode("utf-8"))
        body.append(b"")

        payload = b"\r\n".join(body)

        req = urllib.request.Request(
            url,
            data=payload,
            headers={"Content-Type": f"multipart/form-data; boundary={boundary}"}
        )

        with urllib.request.urlopen(req, timeout=30) as response:
            res = json.loads(response.read().decode("utf-8"))
            return res.get("ok", False)
    except Exception as e:
        send_message(bot_token, chat_id, f"❌ Gagal mengirim dokumen: {e}")
        return False

def download_telegram_file(bot_token, file_id, save_destination):
    try:
        get_file_url = f"https://api.telegram.org/bot{bot_token}/getFile?file_id={file_id}"
        req = urllib.request.Request(get_file_url)
        with urllib.request.urlopen(req, timeout=10) as response:
            res = json.loads(response.read().decode("utf-8"))
            if not res.get("ok"):
                return False, f"Telegram API error: {res}"
            tele_file_path = res["result"]["file_path"]

        download_url = f"https://api.telegram.org/file/bot{bot_token}/{tele_file_path}"
        req_dl = urllib.request.Request(download_url)
        with urllib.request.urlopen(req_dl, timeout=30) as dl_resp:
            content = dl_resp.read()

        parent_dir = os.path.dirname(save_destination)
        if parent_dir and not os.path.exists(parent_dir):
            os.makedirs(parent_dir, exist_ok=True)

        with open(save_destination, "wb") as f:
            f.write(content)

        return True, f"File berhasil disimpan ke <code>{save_destination}</code> ({len(content)} bytes)."
    except Exception as e:
        return False, f"Gagal mengunduh file: {e}"

def handle_file_editor_command(text, bot_token, chat_id, session_cwd):
    text = text.strip()
    parts = text.split()
    cmd = parts[0].lower()

    if cmd in ["/read", "/cat"]:
        if len(parts) < 2:
            send_message(bot_token, chat_id, "Gunakan: <code>/read &lt;filepath&gt;</code>\nContoh: <code>/read /root/tele-sysadmin/README.md</code>")
            return
        
        filepath = text[len(parts[0]):].strip()
        abs_path = os.path.abspath(os.path.join(session_cwd, filepath))

        if not os.path.exists(abs_path):
            send_message(bot_token, chat_id, f"❌ File tidak ditemukan: <code>{abs_path}</code>")
            return

        if os.path.isdir(abs_path):
            send_message(bot_token, chat_id, f"❌ Path ini adalah direktori/folder, gunakan <code>cd {filepath}</code> atau <code>/tab {filepath}</code>.")
            return

        size = os.path.getsize(abs_path)
        if size > 100000:
            send_message(bot_token, chat_id, f"📄 File cukup besar ({size/1024:.1f} KB), mengunduh sebagai dokumen...")
            send_document(bot_token, chat_id, abs_path, caption=f"📄 {os.path.basename(abs_path)}")
            return

        try:
            with open(abs_path, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
            escaped = escape_html(content)
            header = f"<b>📄 Reading File:</b> <code>{escape_html(abs_path)}</code> ({size} bytes)"
            
            if len(escaped) <= 3800:
                send_message(bot_token, chat_id, f"{header}\n<pre><code>{escaped}</code></pre>")
            else:
                send_document(bot_token, chat_id, abs_path, caption=f"📄 {os.path.basename(abs_path)}")
        except Exception as e:
            send_message(bot_token, chat_id, f"❌ Gagal membaca file: {e}")

    elif cmd in ["/get", "/download"]:
        if len(parts) < 2:
            send_message(bot_token, chat_id, "Gunakan: <code>/get &lt;filepath&gt;</code>\nContoh: <code>/get /root/tele-sysadmin/README.md</code>")
            return

        filepath = text[len(parts[0]):].strip()
        abs_path = os.path.abspath(os.path.join(session_cwd, filepath))
        send_document(bot_token, chat_id, abs_path, caption=f"📄 {os.path.basename(abs_path)} | Path: {abs_path}")

    elif cmd == "/write":
        lines = text.split("\n", 1)
        first_line = lines[0].strip().split()
        if len(first_line) < 2:
            send_message(bot_token, chat_id, "<b>Format Write File:</b>\n<code>/write &lt;filepath&gt;\n[isi file baru...]</code>\n\nAtau kirim/upload file dokumen ke bot ini dengan caption <code>/upload &lt;filepath&gt;</code>.")
            return

        filepath = first_line[1].strip()
        content = lines[1] if len(lines) > 1 else ""
        abs_path = os.path.abspath(os.path.join(session_cwd, filepath))

        try:
            parent_dir = os.path.dirname(abs_path)
            if parent_dir and not os.path.exists(parent_dir):
                os.makedirs(parent_dir, exist_ok=True)
                
            with open(abs_path, "w", encoding="utf-8") as f:
                f.write(content)
            send_message(bot_token, chat_id, f"✅ Berhasil menulis file ke <code>{abs_path}</code> ({len(content)} bytes).")
        except Exception as e:
            send_message(bot_token, chat_id, f"❌ Gagal menulis file: {e}")

    elif cmd == "/append":
        lines = text.split("\n", 1)
        first_line = lines[0].strip().split()
        if len(first_line) < 2:
            send_message(bot_token, chat_id, "<b>Format Append File:</b>\n<code>/append &lt;filepath&gt;\n[baris teks tambahan...]</code>")
            return

        filepath = first_line[1].strip()
        content = (lines[1] if len(lines) > 1 else "") + "\n"
        abs_path = os.path.abspath(os.path.join(session_cwd, filepath))

        try:
            with open(abs_path, "a", encoding="utf-8") as f:
                f.write(content)
            send_message(bot_token, chat_id, f"✅ Berhasil menambahkan baris ke <code>{abs_path}</code>.")
        except Exception as e:
            send_message(bot_token, chat_id, f"❌ Gagal append ke file: {e}")
