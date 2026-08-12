import time

class PersistenceEngine:
    def __init__(self, window_seconds=300):
        self.window_seconds = window_seconds
        self.observations = {}

    def add_observation(self, mac, timestamp=None):
        if timestamp is None:
            timestamp = time.time()
            
        if mac not in self.observations:
            self.observations[mac] = []
            
        self.observations[mac].append(timestamp)
        self._cleanup(mac)

    def get_observations(self, mac):
        self._cleanup(mac)
        return self.observations.get(mac, [])

    def _cleanup(self, mac):
        now = time.time()
        self.observations[mac] = [
            t for t in self.observations[mac] 
            if now - t <= self.window_seconds
        ]