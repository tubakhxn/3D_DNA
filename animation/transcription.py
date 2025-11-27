class TranscriptionAnimation:
    def __init__(self):
        self.running = False
        self.progress = 0.0
        self.speed = 0.6

    def start(self):
        self.running = True
        self.progress = 0.0

    def update(self, dt, model):
        if not self.running:
            return
        self.progress += dt * self.speed
        # For demonstration: gently pulse twist while running
        model.set_twist(1.5 * (0.5 + 0.5 * (self.progress % 1.0)))
        if self.progress > 3.0:
            self.running = False
            model.set_twist(0.0)
