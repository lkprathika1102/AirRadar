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