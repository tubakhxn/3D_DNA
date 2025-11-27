class TemperatureAnimation:
    def __init__(self):
        self.temperature = 25.0
        self.target = 25.0
        self.speed = 5.0

    def set_target(self, t):
        self.target = t

    def update(self, dt, model):
        # ease temperature toward target
        diff = self.target - self.temperature
        self.temperature += diff * min(1.0, dt * (self.speed/10.0))
        # map temperature to partial uncoil
        # 25C -> 0 uncoil; 95C -> fully melted (1.0)
        amt = max(0.0, min(1.0, (self.temperature - 25.0) / (95.0 - 25.0)))
        model.set_uncoil(amt)
