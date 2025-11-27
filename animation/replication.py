import time


class ReplicationAnimation:
    def __init__(self):
        self.running = False
        self.progress = 0.0
        self.speed = 0.8

    def start(self):
        self.running = True
        self.progress = 0.0

    def update(self, dt, model):
        if not self.running:
            return
        self.progress += dt * self.speed
        # visual effect: small local uncoil during replication
        model.set_uncoil(min(1.0, 0.5 * self.progress))
        if self.progress >= 2.0:
            self.running = False
            model.set_uncoil(0.0)
