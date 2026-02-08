import pyudev
import datetime
import os

LOG_PATH = "data/logs/usb_events.log"
BASELINE_PATH = "data/logs/usb_baseline.log"

def _write_log(path, message):
    os.makedirs("data/logs", exist_ok=True)
    with open(path, "a") as f:
        f.write(message + "\n")

def log_event(action, device_path, subsystem):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = f"{timestamp} | {action} | {subsystem} | {device_path}"
    _write_log(LOG_PATH, message)
    print(f"[Monitor] {message}")

def baseline_devices():
    """Record all currently connected USB devices at startup."""
    context = pyudev.Context()
    devices = [dev for dev in context.list_devices(subsystem='usb')]
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    _write_log(BASELINE_PATH, f"Baseline snapshot at {timestamp}")
    for dev in devices:
        msg = f"{timestamp} | baseline | {dev.subsystem} | {dev.device_path}"
        _write_log(BASELINE_PATH, msg)
        print(f"[Baseline] {msg}")
    return devices

def detect_event(verbose=True):
    """Detect real-time USB connect/disconnect events."""
    context = pyudev.Context()
    monitor = pyudev.Monitor.from_netlink(context)
    monitor.filter_by(subsystem='usb')

    for device in iter(monitor.poll, None):
        action = device.action
        subsystem = device.subsystem
        device_path = device.device_path

        log_event(action, device_path, subsystem)

        if verbose or action in ["add", "remove"]:
            return device
