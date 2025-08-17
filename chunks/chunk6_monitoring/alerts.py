
import sys
sys.path.append('.')
from datetime import datetime

def send_alert(message: str, level: str = "INFO"):
    """
    Sends an alert. For now, it just prints to the console.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{level}] {message}")

if __name__ == '__main__':
    send_alert("This is a test alert.")
    send_alert("This is a warning alert.", level="WARNING")
    send_alert("This is a critical alert.", level="CRITICAL")
