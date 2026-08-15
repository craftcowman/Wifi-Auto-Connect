import ctypes
import subprocess
import time
from pathlib import Path

# Stores the chosen Wi-Fi SSID inside the user's Windows profile.
# The executable itself remains the only file you need to distribute.
SAVE_FILE = Path.home() / "AppData" / "Local" / "WiFiAutoConnect" / "network.txt"


def netsh(*args):
    return subprocess.run(
        ["netsh", *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="ignore",
        creationflags=subprocess.CREATE_NO_WINDOW
    )


def current_ssid():
    result = netsh("wlan", "show", "interfaces")
    for line in result.stdout.splitlines():
        line = line.strip()
        if line.startswith("SSID") and not line.startswith("BSSID"):
            parts = line.split(":", 1)
            if len(parts) == 2 and parts[1].strip():
                return parts[1].strip()
    return None


def saved_ssid():
    try:
        return SAVE_FILE.read_text(encoding="utf-8").strip() or None
    except FileNotFoundError:
        return None


def remember(ssid):
    SAVE_FILE.parent.mkdir(parents=True, exist_ok=True)
    SAVE_FILE.write_text(ssid, encoding="utf-8")


def connect(ssid):
    netsh("wlan", "connect", f"name={ssid}")
    for _ in range(15):
        time.sleep(1)
        if current_ssid() == ssid:
            return True
    return False


def main():
    now = current_ssid()
    wanted = saved_ssid()

    # First run: learn the Wi-Fi the PC is already connected to.
    if not wanted:
        if now:
            remember(now)
        return

    # Already connected to the saved network.
    if now == wanted:
        return

    # Not connected to it: ask Windows to reconnect.
    connect(wanted)


if __name__ == "__main__":
    main()
