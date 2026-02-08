import os
import hashlib
import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

LOG_PATH = "data/logs/usb_audit.log"

def _write_log(message):
    os.makedirs("data/logs", exist_ok=True)
    with open(LOG_PATH, "a") as f:
        f.write(message + "\n")

def hash_file(file_path):
    """Return SHA256 hash of a file."""
    try:
        with open(file_path, "rb") as f:
            sha256 = hashlib.sha256()
            while chunk := f.read(4096):
                sha256.update(chunk)
        return sha256.hexdigest()
    except Exception as e:
        print(f"[Audit] Hashing failed for {file_path}: {e}")
        return "error"

def log_transfer(file_path, device_info):
    """Log file transfer to USB device with hash and serial."""
    serial = device_info.get("serial", "unknown")
    vendor_id = device_info.get("vendor_id", "unknown")
    product_id = device_info.get("product_id", "unknown")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    file_hash = hash_file(file_path)
    log_msg = (f"{timestamp} | TRANSFER | {vendor_id}:{product_id} | Serial={serial} | "
               f"File={file_path} | SHA256={file_hash}")
    _write_log(log_msg)
    print(f"[Audit] {log_msg}")

class USBFileHandler(FileSystemEventHandler):
    """Watchdog handler for USB file events."""
    def __init__(self, device_info):
        self.device_info = device_info

    def on_created(self, event):
        if not event.is_directory:
            log_transfer(event.src_path, self.device_info)

    def on_modified(self, event):
        if not event.is_directory:
            log_transfer(event.src_path, self.device_info)

def start_audit(path, device_info):
    """Start watchdog observer on USB mount path."""
    event_handler = USBFileHandler(device_info)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    print(f"[Audit] Monitoring file transfers on {path} for device {device_info['serial']}")
    return observer
