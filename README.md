# Gatekeeper: USB Device Control & Monitoring Framework

## Overview
Gatekeeper is a modular Python framework designed to monitor, control, and audit USB device activity in real time. It enforces security policies, logs device events, audits file transfers, and generates daily reports for administrators or academic review.  

---

## Features
- **Device Monitoring**: Detects USB plug/unplug events in real time.  
- **Identification**: Extracts vendor ID, product ID, and serial number for fingerprinting.  
- **Policy Enforcement**: Applies ALLOW/DENY rules to connected devices.  
- **Alerts**: Logs and notifies policy decisions.  
- **Audit**: Watches file transfers, computes SHA256 checksums, and records activity.  
- **Reports**: Generates daily timestamped reports aggregating monitor, alert, and audit logs.  
- **Graceful Exit**: Clean shutdown with `Ctrl+C` or exit commands, no stack trace errors.  

---

## Project Structure
```
gatekeeper/
├── main.py                # Entry point, integrates all modules
├── modules/
│   ├── monitor.py          # Detects USB events
│   ├── identify.py         # Extracts device info
│   ├── policy.py           # Enforces ALLOW/DENY rules
│   ├── alert.py            # Logs decisions
│   ├── audit.py            # Audits file transfers
│   └── report.py           # Generates daily reports
└── data/
│    └── logs/              # Stores monitor, alert, audit logs and reports
│    └── policy.json
└── documents/
     └── screenshots/
     └── gatekeepr ppt
     └── gatekeepr doc
     └── gatekeepr flowchart
```

---

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Om-Fulsundar/gatekeeper.git
   cd gatekeeper
   ```
2. make sure you have pyudev ,  watchdog installed already. (if not install it by using 'pip install watchdog' and so on)

3. Ensure you have Python 3.8+ installed.

---

## Usage
Run Gatekeeper:
```bash
python3 main.py
```

Typical workflow:
1. Plug in a USB device.  
2. Gatekeeper detects and applies policy.  
3. If allowed, it waits for the device to mount.  
4. File transfers are audited and logged.  
5. A daily report is generated in `data/logs/`.  

Graceful exit:
- Press `Ctrl+C` → Gatekeeper shuts down cleanly.  

For new device, it blocks automatically. take vendor ID, product ID and add it in policy.json

---

## Reports
Reports are generated daily with filenames like:
```
data/logs/gatekeeper_report_2026-02-02.txt
```

Each report contains:
- Device events (Monitor)  
- Policy decisions (Alert)  
- File transfers (Audit)  

---

## Configuration
- Default mount roots: `/media`, `/run/media`, `/mnt`, `/media/<username>`.  
- Timeout for mount detection: 20 seconds.  
- To change username, edit the candidate path in `main.py` or extend with a config file.  

---

## Future Enhancements
- Config file for paths, timeouts, and policies.  
- Automatic log rotation (keep last N reports).  
- Observer auto-stop when devices are unplugged.  
- CSV/JSON export for structured reporting.  
