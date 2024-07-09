import subprocess
import psutil
import time
from datetime import datetime
import csv
import os

# Categories mapping (you can extend this list)
CATEGORIES = {
    "firefox": "Productivity",
    "chrome": "Productivity",
    "code": "Development",
    "slack": "Communication",
    "spotify": "Entertainment",
    # Add more applications and categories as needed
}

# Function to get active window details
def get_active_window():
    try:
        window_id = subprocess.check_output(["xdotool", "getactivewindow"]).strip().decode("utf-8")
        window_name = subprocess.check_output(["xdotool", "getwindowname", window_id]).strip().decode("utf-8")
        pid = subprocess.check_output(["xdotool", "getwindowpid", window_id]).strip().decode("utf-8")
        process_name = psutil.Process(int(pid)).name()
        category = CATEGORIES.get(process_name, "Uncategorized")
        
        # Handle Firefox specifically to get URL
        if process_name == "firefox":
            browser = subprocess.Popen(["firefox", "-v"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, _ = browser.communicate()
            if stdout:
                active_url = subprocess.check_output(["xdotool", "getwindowfocus", "getwindowname"]).strip().decode("utf-8")
                return active_url, process_name, category
        
        return window_name, process_name, category
    except Exception as e:
        return None, None, None

# Function to check for idle time
def get_idle_time():
    idle_time = subprocess.check_output("xprintidle").strip().decode("utf-8")
    return int(idle_time) / 1000  # Convert milliseconds to seconds

# Function to log usage
def log_usage(log_file, idle_threshold=300):  # 5 minutes
    with open(log_file, 'a', newline='') as file:
        writer = csv.writer(file)
        while True:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            idle_time = get_idle_time()
            if idle_time < idle_threshold:
                window_title, app_name, category = get_active_window()
                writer.writerow([timestamp, window_title, app_name, category, "Active"])
                print(f"Logged: {timestamp} - {window_title} - {app_name} - {category}")
            else:
                writer.writerow([timestamp, "Idle", "Idle", "Idle", "Idle"])
                print(f"Idle: {timestamp}")
            time.sleep(5)  # Log every 5 seconds


if __name__ == "__main__":
    log_file = "usage_log.csv"
    if not os.path.isfile(log_file):
        with open(log_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Timestamp", "Window Title", "Application Name", "Category", "Status"])

    log_usage(log_file)
