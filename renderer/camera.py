import math


class Camera:
    def __init__(self, zoom=3.0, pitch=0.4, yaw=0.0):
        self.zoom = zoom
        self.pitch = pitch
        self.yaw = yaw

    def get_view_matrix(self):
        # simple orbit camera: compute eye from yaw/pitch/zoom
        ex = self.zoom * math.cos(self.pitch) * math.sin(self.yaw)
        ey = self.zoom * math.sin(self.pitch)
        ez = self.zoom * math.cos(self.pitch) * math.cos(self.yaw)
        # return tuple (eye, center, up)
        return (ex, ey, ez), (0.0, 0.0, 0.0), (0.0, 1.0, 0.0)
