class TranslationAnimation:
    def __init__(self):
        self.running = False
        self.progress = 0.0
        self.speed = 0.7

    def start(self):
        self.running = True
        self.progress = 0.0

    def update(self, dt, model):
        if not self.running:
            return
        self.progress += dt * self.speed
        # visual: compression then back to normal
        model.set_zoom(1.0 + 0.2 * (0.5 - abs((self.progress % 1.0) - 0.5)))
        if self.progress > 4.0:
            self.running = False
            model.set_zoom(1.0)
