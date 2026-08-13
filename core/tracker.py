import time

class PersistenceEngine:
    def __init__(self, window_seconds=300):
        self.window_seconds = window_seconds
        self.observations = {}

    def add_observation(self, mac, distance, timestamp=None):
        if timestamp is None:
            timestamp = time.time()
            
        if mac not in self.observations:
            self.observations[mac] = []
            
        self.observations[mac].append((timestamp, distance))
        self._cleanup(mac)

    def get_observations(self, mac):
        self._cleanup(mac)
        return self.observations.get(mac, [])

    def is_suspicious(self, mac, dist_threshold=3.0, min_observations=5):
        obs = self.get_observations(mac)
        if len(obs) < min_observations:
            return False
            
        close_sightings = [d for t, d in obs if d <= dist_threshold]
        return len(close_sightings) >= min_observations

    def _cleanup(self, mac):
        now = time.time()
        if mac in self.observations:
            self.observations[mac] = [
                item for item in self.observations[mac] 
                if now - item[0] <= self.window_seconds
            ]