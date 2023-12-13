

class PID:

    def __init__(self):
        self.te = 2e-1
        self.kp = 0.15  # 0.2 for v=50
        self.ki = 0.000  # 0 for v=50
        self.kd = 0.00  # 0 for v=50
        self.i = 0
        self.e0 = 0

    def get_control_inputs(self, error):
        self.i += error * self.te
        d = (error - self.e0) / self.te
        u = self.kp * error + self.kd * d + self.ki * self.i
        self.e0 = error
        v = 50

        return u, v
