import sys
import time
from core.colors import Colors

def animated_loading(duration: float = 1.5):
    chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    end_time = time.time() + duration
    idx = 0
    while time.time() < end_time:
        sys.stdout.write(f"\r{Colors.CYAN}{chars[idx % len(chars)]} Initializing PenKit Core Engine...")
        sys.stdout.flush()
        time.sleep(0.08)
        idx += 1
    sys.stdout.write("\r" + " " * 45 + "\r")
    sys.stdout.flush()

def draw_progress_bar(iteration: int, total: int, prefix: str = '', suffix: str = '', length: int = 40):
    percent = f"{100 * (iteration / float(total)):.1f}"
    filled_length = int(length * iteration // total)
    bar = "█" * filled_length + '-' * (length - filled_length)
    sys.stdout.write(f'\r{Colors.CYAN}{prefix} |{bar}| {percent}% {suffix}')
    sys.stdout.flush()
    if iteration == total:
        sys.stdout.write('\n')