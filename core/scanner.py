import asyncio
from datetime import datetime
from bleak import BleakScanner
from core.filter import SignalProcessor
from core.tracker import PersistenceEngine
from database.models import upsert_device, log_measurement

class BLEManager:
    def __init__(self, detection_callback):
        self.detection_callback = detection_callback
        self.processor = SignalProcessor()
        self.tracker = PersistenceEngine()
        self.scanner = BleakScanner()

    async def handle_detection(self, device, advertisement_data):
        mac = device.address
        name = device.name or "Unknown"
        rssi = advertisement_data.rssi
        timestamp = datetime.now().isoformat()
        
        filtered_rssi, distance = self.processor.process(mac, rssi)
        self.tracker.add_observation(mac, distance)
        is_threat = self.tracker.is_suspicious(mac)
        
        await asyncio.to_thread(upsert_device, mac, name, timestamp)
        await asyncio.to_thread(
            log_measurement, 
            mac, 
            timestamp, 
            rssi, 
            filtered_rssi, 
            distance
        )
        
        payload = {
            "mac": mac,
            "name": name,
            "rssi": rssi,
            "filtered_rssi": filtered_rssi,
            "distance": distance,
            "is_threat": is_threat
        }
        
        await self.detection_callback(payload)

    async def start_scan(self):
        await self.scanner.start(detection_callback=self.handle_detection)
        try:
            while True:
                await asyncio.sleep(1.0)
        finally:
            await self.scanner.stop()

    async def stop_scan(self):
        await self.scanner.stop()