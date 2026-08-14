import os
import sys
import json
from datetime import datetime

STATS_FILE = "/tmp/tele_sysadmin_stats.json"

def record_current_stat():
    try:
        import psutil
        mem = psutil.virtual_memory().percent
        cpu = psutil.cpu_percent(interval=0.1)
        now_str = datetime.now().strftime("%H:%M")

        history = []
        if os.path.exists(STATS_FILE):
            try:
                with open(STATS_FILE, "r", encoding="utf-8") as f:
                    history = json.load(f)
            except Exception:
                history = []

        history.append({"time": now_str, "ram": mem, "cpu": cpu})
        # Keep last 10 historical data points
        if len(history) > 10:
            history = history[-10:]

        with open(STATS_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f)
        return history
    except Exception:
        return []

def generate_memory_chart_image():
    chart_path = "/tmp/tele_sysadmin_chart.png"
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import psutil

        history = record_current_stat()
        if len(history) < 2:
            # Generate initial points if first run
            now_str = datetime.now().strftime("%H:%M")
            mem = psutil.virtual_memory().percent
            cpu = psutil.cpu_percent(interval=0.1)
            history = [{"time": now_str, "ram": mem, "cpu": cpu}]

        times = [h["time"] for h in history]
        ram_values = [h["ram"] for h in history]
        cpu_values = [h["cpu"] for h in history]

        fig, ax = plt.subplots(figsize=(6.5, 3.5))
        ax.plot(times, ram_values, color='#3b82f6', linewidth=2.5, marker='o', label='RAM Usage (%)')
        ax.plot(times, cpu_values, color='#10b981', linewidth=2.0, marker='s', linestyle='--', label='CPU Usage (%)')

        ax.set_title("Real-Time Server Performance Trend (%)", fontsize=12, fontweight='bold', pad=10)
        ax.set_ylim(0, 100)
        ax.axhline(85, color='#ef4444', linestyle=':', label='Alert Threshold (85%)')
        ax.legend(loc='upper right', fontsize=8)
        ax.grid(True, linestyle=':', alpha=0.6)
        plt.xticks(rotation=15, fontsize=8)
        plt.tight_layout()
        plt.savefig(chart_path, dpi=120)
        plt.close(fig)
        return True, chart_path
    except Exception as e:
        return False, str(e)
