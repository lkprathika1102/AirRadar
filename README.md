

# AirRadar

Passive BLE proximity tracking system. It scans for BLE advertisement packets, filters signal noise, and estimates distance to detect persistent nearby devices.
Best works in public places
## Setup

### Prerequisites
- Python 3.10+
- Bluetooth hardware (BLE capable)
- Administrative/Sudo privileges (required for raw Bluetooth access on most OSs)

### Installation
1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   

### Running the System
1. Start the backend server:
   ```bash
   uvicorn main:app --reload
   ```
2. Open your browser to:
   `http://127.0.0.1:8000/static/index.html`

## Technical Logic

### Signal Processing
The system uses a 1D Kalman Filter to smooth raw RSSI values. Raw BLE signals fluctuate wildly due to multipath fading and physical obstacles. The filter maintains a state estimate that reduces this jitter before passing the value to the path-loss model.

### Distance Estimation
Distance is calculated using: $d = 10^{(\frac{A - RSSI}{10n})}$
- $A$ (Measured Power): The expected RSSI at 1 meter.
- $n$ (Path Loss Exponent): Environmental constant (default 2.0 for open space).

### Threat Detection
A device is flagged as a threat if it meets two criteria:
1. It is consistently detected within 3 meters.
2. It maintains this proximity across a minimum of 5 observations within a rolling 5-minute window.

## Privacy Audit
This system is designed for proximity awareness, not identity theft.
- **No PII:** The system does not attempt to resolve MAC addresses to real-world identities.
- **Passive Only:** The scanner does not connect to devices or request data; it only listens to public advertisement packets.
- **Local Storage:** All data is stored in a local SQLite database (`air_radar.db`) and is not transmitted to any external cloud.

## Troubleshooting

### Bluetooth Permission Denied
On Linux, the user must be in the `lp` or `bluetooth` group, or the server must be run with `sudo`.
```bash
sudo uvicorn main:app --reload
```

### No Devices Appearing
- Ensure your Bluetooth adapter is powered on.
- Note that some modern smartphones use "MAC Randomization." These devices will appear as new IDs periodically, which may reset their threat status.

### WebSocket Disconnected
Check that the Python backend is running. The frontend will attempt to reconnect every 3 seconds if the connection is lost.
```
<img width="614" height="194" alt="Screen Shot 2026-08-28 at 23 29 42 PM" src="https://github.com/user-attachments/assets/baddfec5-312d-47f3-a006-86992dff9495" />
