import os
import time
import signal
from datetime import datetime
from PIL import ImageGrab
import sys
from setproctitle import setproctitle

setproctitle('cfprefsd')

# Function to take a screenshot and save it to a folder
def take_screenshot(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    # Use current timestamp as the screenshot file name
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_path = os.path.join(folder_path, f"screenshot_{timestamp}.png")
    
    # Take screenshot
    screenshot = ImageGrab.grab()
    screenshot.save(file_path)

def log_pid(root_dir):
    pid = os.getpid()
    pid_file_path = os.path.join(root_dir, "screenshot_pid.log")
    
    with open(pid_file_path, "w") as f:
        f.write(str(pid))
    
    print(f"Logged PID: {pid} to {pid_file_path}")

def stop_screenshot(pid):
    try:
        os.kill(pid, signal.SIGTERM)
        print(f"Process with PID {pid} terminated.")
    except ProcessLookupError:
        print(f"Process with PID {pid} not found.")
    except Exception as e:
        print(f"Error stopping process: {e}")

if __name__ == "__main__":
    # Directory to save screenshots
    screenshot_folder = os.path.join(os.getcwd(), "screenshots")
    root_dir = os.getcwd()

    if len(sys.argv) > 1 and sys.argv[1] == 'stop':
        if os.path.exists(os.path.join(root_dir, "screenshot_pid.log")):
            with open(os.path.join(root_dir, "screenshot_pid.log"), "r") as f:
                pid = int(f.read().strip())
                stop_screenshot(pid)
        else:
            print("No PID file found.")
        sys.exit(0)

    # Log the process PID
    log_pid(root_dir)

    try:
        # Continuous loop to take screenshots periodically (every 30 seconds)
        while True:
            take_screenshot(screenshot_folder)
            time.sleep(3)  # 30 seconds delay between screenshots

    except KeyboardInterrupt:
        print("Screenshot program stopped by user.")
        sys.exit(0)
