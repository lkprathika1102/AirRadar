import sqlite3

def init_db():
    conn = sqlite3.connect("air_radar.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS devices (
            mac TEXT PRIMARY KEY,
            name TEXT,
            first_seen DATETIME,
            last_seen DATETIME,
            count INTEGER,
            threat_flag INTEGER DEFAULT 0
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS rssi_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mac TEXT,
            timestamp DATETIME,
            raw_rssi REAL,
            filtered_rssi REAL,
            distance REAL,
            FOREIGN KEY (mac) REFERENCES devices (mac)
        )
    """)
    
    conn.commit()
    conn.close()

def upsert_device(mac, name, timestamp):
    conn = sqlite3.connect("air_radar.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT count FROM devices WHERE mac = ?", (mac,))
    row = cursor.fetchone()
    
    if row:
        new_count = row[0] + 1
        cursor.execute("""
            UPDATE devices 
            SET name = ?, last_seen = ?, count = ? 
            WHERE mac = ?
        """, (name, timestamp, new_count, mac))
    else:
        cursor.execute("""
            INSERT INTO devices (mac, name, first_seen, last_seen, count) 
            VALUES (?, ?, ?, ?, 1)
        """, (mac, name, timestamp, timestamp))
    
    conn.commit()
    conn.close()