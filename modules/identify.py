import datetime
import os

LOG_PATH = "data/logs/usb_identify.log"

def _write_log(message):
    os.makedirs("data/logs", exist_ok=True)
    with open(LOG_PATH, "a") as f:
        f.write(message + "\n")

def extract_info(device):
    props = device.properties

    vendor_id = props.get("ID_VENDOR_ID", "unknown")
    product_id = props.get("ID_MODEL_ID", "unknown")
    serial = props.get("ID_SERIAL_SHORT", "unknown")
    vendor_name = props.get("ID_VENDOR_FROM_DATABASE", "unknown")
    model_name = props.get("ID_MODEL_FROM_DATABASE", "unknown")

    device_info = {
        "vendor_id": vendor_id,
        "product_id": product_id,
        "serial": serial,
        "vendor_name": vendor_name,
        "model_name": model_name,
        "device_path": device.device_path
    }

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_msg = f"{timestamp} | {vendor_id}:{product_id} | Serial: {serial} | Path: {device.device_path}"
    _write_log(log_msg)

    print(f"[Identify] {log_msg}")
    return device_info
