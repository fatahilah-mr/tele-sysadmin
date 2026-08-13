import os
import sys
from datetime import datetime

def generate_memory_chart_image():
    chart_path = "/tmp/tele_sysadmin_chart.png"
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import psutil
        
        # Sample memory trend data
        times = [datetime.now().strftime("%H:%M:%S")]
        mem = psutil.virtual_memory()
        used_pct = mem.percent
        
        fig, ax = plt.subplots(figsize=(6, 3))
        ax.plot([0, 1, 2, 3, 4], [used_pct-2, used_pct-1, used_pct+1, used_pct, used_pct], color='#3b82f6', linewidth=2, marker='o')
        ax.set_title("RAM Usage Trend (%)", fontsize=12, fontweight='bold', pad=10)
        ax.set_ylim(0, 100)
        ax.axhline(85, color='red', linestyle='--', label='Alert Threshold (85%)')
        ax.legend(loc='upper right')
        ax.grid(True, linestyle=':', alpha=0.6)
        plt.tight_layout()
        plt.savefig(chart_path, dpi=100)
        plt.close(fig)
        return True, chart_path
    except Exception as e:
        return False, str(e)
