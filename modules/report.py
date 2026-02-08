# modules/report.py
import os
import datetime

LOG_DIR = "data/logs"

def read_log(file_name):
    path = os.path.join(LOG_DIR, file_name)
    if os.path.exists(path):
        with open(path, "r") as f:
            return f.readlines()
    return []

def generate_summary():
    """
    Aggregate logs from monitor, alert, and audit.
    Return a formatted text summary.
    """
    monitor_logs = read_log("usb_monitor.log")
    alert_logs   = read_log("usb_alert.log")
    audit_logs   = read_log("usb_audit.log")

    summary = []
    summary.append("=== Gatekeeper Report ===")
    summary.append(f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    summary.append("")

    summary.append(">> Device Events (Monitor)")
    summary.extend(monitor_logs if monitor_logs else ["No monitor events recorded."])
    summary.append("")

    summary.append(">> Policy Decisions (Alert)")
    summary.extend(alert_logs if alert_logs else ["No alerts recorded."])
    summary.append("")

    summary.append(">> File Transfers (Audit)")
    summary.extend(audit_logs if audit_logs else ["No audit events recorded."])
    summary.append("")

    return "\n".join(summary)

def save_report():
    """
    Save the summary to a daily timestamped report file.
    Example: gatekeeper_report_2026-01-24.txt
    """
    report_text = generate_summary()
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    report_filename = f"gatekeeper_report_{date_str}.txt"
    report_path = os.path.join(LOG_DIR, report_filename)

    # Ensure log directory exists
    os.makedirs(LOG_DIR, exist_ok=True)

    with open(report_path, "w") as f:
        f.write(report_text)

    return report_path
