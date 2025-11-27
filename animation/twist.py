import math


class TwistAnimation:
    def __init__(self):
        self.speed = 1.0
        self.time = 0.0
        self.paused = False

    def set_speed(self, s):
        self.speed = s

    def update(self, dt, model):
        if self.paused:
            return
        self.time += dt * self.speed
        model.set_twist(math.sin(self.time) * 2.0)

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False
