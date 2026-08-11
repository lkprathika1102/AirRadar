class KalmanFilter1D:
    def __init__(self, process_variance=1e-5, measurement_variance=0.1, initial_value=None, initial_error=1.0):
        self.q = process_variance
        self.r = measurement_variance
        self.p = initial_error
        self.x = initial_value

    def update(self, measurement):
        if self.x is None:
            self.x = measurement
            return self.x

        self.p = self.p + self.q
        k = self.p / (self.p + self.r)
        self.x = self.x + k * (measurement - self.x)
        self.p = (1 - k) * self.p
        
        return self.x

class SignalProcessor:
    def __init__(self, measured_power=-60, path_loss_exponent=2.0):
        self.measured_power = measured_power
        self.path_loss_exponent = path_loss_exponent
        self.filters = {}

    def process(self, mac, rssi):
        if mac not in self.filters:
            self.filters[mac] = KalmanFilter1D()
        
        filtered_rssi = self.filters[mac].update(rssi)
        distance = 10 ** ((self.measured_power - filtered_rssi) / (10 * self.path_loss_exponent))
        
        return filtered_rssi, distance