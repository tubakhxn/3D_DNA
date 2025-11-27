class UncoilAnimation:
    def __init__(self):
        self.progress = 0.0
        self.speed = 0.5
        self.paused = False

    def set_speed(self, s):
        self.speed = s

    def update(self, dt, model):
        if self.paused:
            return
        # ease towards target uncoil amount if set on model
        target = model.uncoil_amount
        # simple lerp
        self.progress += (target - self.progress) * min(1.0, dt * self.speed)
        model.set_uncoil(self.progress)

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False
