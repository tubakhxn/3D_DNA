import math
import ctypes
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

from .dna_model import DNAModel
from .camera import Camera


class GLRenderer:
    def __init__(self, size=(1280, 800)):
        self.width, self.height = size
        # DNAModel now uses stack_height, segments, radius
        self.model = DNAModel(stack_height=8.0, segments=200, radius=0.45)
        self.camera = Camera(zoom=6.0, pitch=0.2, yaw=0.8)
        self.animations = []
        self.bg_color = (0.05, 0.05, 0.07, 1.0)
        self._init_gl()

    def _init_gl(self):
        glViewport(0, 0, self.width, self.height)
        glEnable(GL_DEPTH_TEST)
        glClearColor(*self.bg_color)

    def register_animation(self, anim):
        self.animations.append(anim)

    def apply_gestures(self, gestures):
        # map gestures to model params
        if 'two_finger_rotate' in gestures:
            a = gestures['two_finger_rotate']['angle']
            self.model.set_twist(a * 0.05)

        if 'pinch_zoom' in gestures:
            d = gestures['pinch_zoom']['distance']
            # invert distance to zoom: smaller = zoom in
            z = 1.0 + max(0.1, 1.0 - d*10)
            self.model.set_zoom(z)

        if 'two_hand_stretch' in gestures:
            amt = gestures['two_hand_stretch']['distance']
            # normalized stretch amount
            un = min(1.0, amt * 2.0)
            self.model.set_uncoil(un)

        if 'pinch_rotate' in gestures:
            # control playback speed via rotational speed
            rs = gestures['pinch_rotate']['rot_speed']
            for a in self.animations:
                if hasattr(a, 'set_speed'):
                    a.set_speed(1.0 + abs(rs))

        if 'palm_down' in gestures:
            # freeze DNA: stop updates
            for a in self.animations:
                if hasattr(a, 'pause'):
                    a.pause()

        if 'palm_up' in gestures:
            # show mutation panel handled in UI layer
            pass

        if 'clap' in gestures:
            # trigger replication animation
            for a in self.animations:
                if a.__class__.__name__ == 'ReplicationAnimation':
                    a.start()

        if 'fist' in gestures:
            # compress into chromosome
            for a in self.animations:
                if hasattr(a, 'compress'):
                    a.compress()

        if 'swipe_up' in gestures:
            for a in self.animations:
                if a.__class__.__name__ == 'TranscriptionAnimation':
                    a.start()

        if 'swipe_down' in gestures:
            for a in self.animations:
                if a.__class__.__name__ == 'TranslationAnimation':
                    a.start()

    def update(self, dt):
        # update animations then model
        for a in self.animations:
            a.update(dt, self.model)
        self.model.update(dt)

    def render(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # set projection
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45.0, float(self.width)/float(self.height), 0.1, 100.0)

        # view
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        eye, center, up = self.camera.get_view_matrix()
        gluLookAt(eye[0], eye[1], eye[2], center[0], center[1], center[2], up[0], up[1], up[2])

        # draw DNA strands: two colored strands (red and blue) plus base-pair rungs
        # Render two vertical stacks using DNAModel API
        # separation and height can be driven by camera zoom or model params
        separation = 2.0
        height = self.model.stack_height
        # allow camera zoom to influence overall model zoom
        # the DNAModel.render_two_stacks uses its internal zoom factor
        self.model.render_two_stacks(center_x=0.0, separation=separation, height=height)
