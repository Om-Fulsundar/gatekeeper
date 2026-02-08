import os
import datetime
import subprocess

LOG_PATH = "data/logs/usb_alert.log"

def _write_log(message):
    os.makedirs("data/logs", exist_ok=True)
    with open(LOG_PATH, "a") as f:
        f.write(message + "\n")

def handle_decision(device_info, decision, lockdown=False):
    """
    Enforce policy decisions.
    - Ignore sub-events with unknown fingerprints.
    - Block unauthorized devices by unmounting/disabling.
    - Allow authorized devices silently.
    - Optional lockdown mode disables all USB storage.
    """
    vendor_id = device_info.get("vendor_id", "unknown")
    product_id = device_info.get("product_id", "unknown")
    serial = device_info.get("serial", "unknown")
    device_path = device_info.get("device_path", "unknown")

    # Skip noisy sub-events
    if vendor_id == "unknown" and product_id == "unknown":
        print(f"[Alert] Ignoring sub-event with unknown fingerprint: {device_path}")
        return

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if decision == "BLOCK":
        # Log enforcement
        log_msg = f"{timestamp} | BLOCKED | {vendor_id}:{product_id} | Serial={serial} | Path={device_path}"
        _write_log(log_msg)
        print(f"[Alert] {log_msg}")

        # Enforcement (Linux example)
        try:
            # Attempt to unmount if it's a storage device
            subprocess.run(["udisksctl", "unmount", "-b", device_path], check=False)
            # Disable device authorization (requires root)
            if os.path.exists(f"/sys/bus/usb/devices/{os.path.basename(device_path)}/authorized"):
                subprocess.run(["sudo", "sh", "-c", f"echo 0 > /sys/bus/usb/devices/{os.path.basename(device_path)}/authorized"], check=False)
        except Exception as e:
            print(f"[Alert] Enforcement failed: {e}")

        # Lockdown mode: disable all USB storage
        if lockdown:
            try:
                subprocess.run(["sudo", "sh", "-c", "echo 0 > /sys/bus/usb/devices/*/authorized"], check=False)
                print("[Alert] Lockdown mode activated: all USB storage disabled.")
            except Exception as e:
                print(f"[Alert] Lockdown enforcement failed: {e}")

    elif decision == "ALLOW":
        log_msg = f"{timestamp} | ALLOWED | {vendor_id}:{product_id} | Serial={serial} | Path={device_path}"
        _write_log(log_msg)
        print(f"[Alert] {log_msg}")
