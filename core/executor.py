import os
import re
import subprocess

def strip_ansi(text):
    return re.sub(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])', '', text)

def escape_html(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def execute_bash_command(cmd_str, cwd=None, timeout=30):
    cwd = cwd or os.path.expanduser("~")
    cmd_str = cmd_str.strip()

    # Handle 'cd' commands explicitly
    if cmd_str.startswith("cd ") or cmd_str == "cd":
        target = cmd_str[3:].strip() if len(cmd_str) > 2 else os.path.expanduser("~")
        if not target:
            target = os.path.expanduser("~")

        new_dir = os.path.abspath(os.path.join(cwd, target))
        if os.path.exists(new_dir) and os.path.isdir(new_dir):
            return True, f"Directory changed to: {new_dir}", new_dir
        else:
            return False, f"Directory not found: {target}", cwd

    try:
        proc = subprocess.run(
            cmd_str,
            shell=True,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=timeout,
            executable="/bin/bash"
        )
        output = proc.stdout.decode("utf-8", errors="replace")
        if not output.strip():
            output = "(Command executed with no output - exit code 0)"
        return (proc.returncode == 0), output, cwd
    except subprocess.TimeoutExpired:
        return False, f"Command timed out (exceeded {timeout} seconds limit).", cwd
    except Exception as e:
        return False, f"Execution error: {e}", cwd
