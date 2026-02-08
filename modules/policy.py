import json
import os
import datetime

POLICY_FILE = "data/policy.json"
LOG_PATH = "data/logs/usb_policy.log"

def _write_log(message):
    os.makedirs("data/logs", exist_ok=True)
    with open(LOG_PATH, "a") as f:
        f.write(message + "\n")

def load_policy():
    """Load allowlist/blocklist from JSON file."""
    if not os.path.exists(POLICY_FILE):
        # Create default policy file if missing
        default_policy = {
            "allowlist": ["1234:abcd"],   # Example VendorID:ProductID
            "blocklist": ["9999:ffff"],   # Example blocked device
            "serial_allowlist": [],
            "serial_blocklist": []
        }
        os.makedirs("data", exist_ok=True)
        with open(POLICY_FILE, "w") as f:
            json.dump(default_policy, f, indent=4)
        return default_policy

    with open(POLICY_FILE, "r") as f:
        return json.load(f)

def enforce(device_info):
    """Check device against allowlist/blocklist and return decision."""
    policy = load_policy()
    device_id = f"{device_info['vendor_id']}:{device_info['product_id']}"
    serial = device_info.get("serial", "unknown")

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if device_id in policy["allowlist"] or serial in policy["serial_allowlist"]:
        decision = "ALLOW"
        log_msg = f"{timestamp} | ALLOW | {device_id} | Serial={serial}"
    elif device_id in policy["blocklist"] or serial in policy["serial_blocklist"]:
        decision = "BLOCK"
        log_msg = f"{timestamp} | BLOCK | {device_id} | Serial={serial}"
    else:
        decision = "BLOCK"  # Default deny
        log_msg = f"{timestamp} | BLOCK (unauthorized) | {device_id} | Serial={serial}"

    _write_log(log_msg)
    print(f"[Policy] {log_msg}")
    return decision
