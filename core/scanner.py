import asyncio
from bleak import BleakScanner

class BLEManager:
    def __init__(self, detection_callback):
        self.detection_callback = detection_callback
        self.scanner = BleakScanner()

    async def start_scan(self):
        await self.scanner.start()
        try:
            while True:
                devices = await self.scanner.get_discovered_devices()
                for device in devices:
                    await self.detection_callback(device)
                await asyncio.sleep(1.0)
        finally:
            await self.scanner.stop()

    async def stop_scan(self):
        await self.scanner.stop()