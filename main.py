# main.py
# script by Om Fulsundar (https://github.com/Om-Fulsundar)

import os
import time
import sys
from modules import monitor, identify, policy, alert, audit, report

def wait_for_usb_mount(timeout=20):
    """
    Poll common mount roots for up to `timeout` seconds until a USB subfolder appears.
    Returns the full mount path (e.g. /media/<username>/64 GB).
    If nothing mounts within timeout, returns None.
    """
    candidates = ["/media", "/run/media", "/mnt", "/media/gr0ot"]  
    
    # Replace "gr0ot" with your actual Linux username if your USB drives mount under /media/<username>/

    for _ in range(timeout):
        for base in candidates:
            if os.path.exists(base):
                # Check if base itself is a mount
                if os.path.ismount(base):
                    return base
                # Otherwise scan subfolders
                for entry in os.listdir(base):
                    full_path = os.path.join(base, entry)
                    if os.path.isdir(full_path) and os.path.ismount(full_path):
                        return full_path
        time.sleep(1)
    return None

def main():
    print("[Gatekeeper] USB Device Control & Monitoring Framework starting...")
    monitor.baseline_devices()
    print("[Gatekeeper] Monitoring USB events in real-time. Plug/unplug a device ...")

    try:
        while True:
            device_event = monitor.detect_event(verbose=True)
            if device_event:
                device_info = identify.extract_info(device_event)
                decision = policy.enforce(device_info)
                alert.handle_decision(device_info, decision, lockdown=False)

                if decision == "ALLOW":
                    print("[Gatekeeper] Waiting for USB mount...")
                    mount_path = wait_for_usb_mount(timeout=20)
                    if mount_path:
                        audit.start_audit(mount_path, device_info)
                        print(f"[Gatekeeper] Audit started on {mount_path}")
                    else:
                        print("[Gatekeeper] Timeout: No USB mount path detected for auditing.")

                print(f"[Gatekeeper] Final Decision: {decision} for "
                      f"{device_info['vendor_id']}:{device_info['product_id']} "
                      f"Serial={device_info['serial']}")

                # Update report after each cycle
                report_path = report.save_report()
                print(f"[Gatekeeper] Report updated: {report_path}")

    except KeyboardInterrupt:
        print("\n[Gatekeeper] Exiting gracefully. Goodbye!")
        sys.exit(0)

if __name__ == "__main__":
    main()
