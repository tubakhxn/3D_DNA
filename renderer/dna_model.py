import numpy as np
from .dna_generator import generate_parametric_stack
from OpenGL.GL import *
import math


class DNAModel:
    """DNAModel implements render_dna_stack and renders two vertical stacks.

    Colors are fixed to the specification and must not be modified here.
    """

    # Colors (normalized RGB)
    COLOR_BLUE = (10/255.0, 77/255.0, 191/255.0)      # #0A4DBF
    COLOR_RED = (214/255.0, 64/255.0, 64/255.0)       # #D64040
    RUNG_BLUE = (95/255.0, 163/255.0, 255/255.0)      # #5FA3FF
    RUNG_RED = (255/255.0, 122/255.0, 122/255.0)      # #FF7A7A

    def __init__(self, stack_height=8.0, segments=200, radius=0.45):
        self.stack_height = stack_height
        self.segments = segments
        self.radius = radius
        # step angle per sample (36 degrees requirement will be enforced)
        self.step_angle_deg = 36.0

        # generate two identical stacks (A and B); they will be rendered at different x offsets
        self.stack_template = generate_parametric_stack(height=self.stack_height,
                                                        segments=self.segments,
                                                        radius=self.radius,
                                                        step_angle_deg=self.step_angle_deg,
                                                        phase=0.0)

        self.twist_amount = 0.0
        self.uncoil_amount = 0.0
        self.zoom = 1.0

    def set_twist(self, amount):
        # amount is radians multiplier that modulates phase; keep vertical orientation
        self.twist_amount = amount

    def set_uncoil(self, amount):
        # 0..1
        self.uncoil_amount = max(0.0, min(1.0, amount))

    def set_zoom(self, z):
        self.zoom = max(0.1, z)

    def update(self, dt):
        # nothing to precompute per-frame for now; rendering uses current params
        pass

    def _apply_twist_uncoil(self, pts, strand_index, position_x):
        """Apply twist and uncoil transforms to a strand points array and return transformed positions.

        pts: Nx3 array with (x,y,z) where y is vertical coordinate.
        strand_index: 0 for left (blue), 1 for right (red) - used for phase offset.
        position_x: base x offset for the entire stack center.
        """
        n = pts.shape[0]
        out = pts.copy()
        # For each sample, modulate radius based on uncoil_amount
        for i in range(n):
            x, y, z = pts[i]
            # radial vector from center
            rx, rz = x, z
            r = math.hypot(rx, rz)
            if self.uncoil_amount > 0.0:
                # move points toward the centerline (x=0,z=0) proportionally
                rx = rx * (1.0 - self.uncoil_amount)
                rz = rz * (1.0 - self.uncoil_amount)

            # twist: rotate around vertical axis by angle proportional to twist_amount and y
            angle = self.twist_amount * y
            ca = math.cos(angle)
            sa = math.sin(angle)
            tx = ca * rx - sa * rz
            tz = sa * rx + ca * rz

            # translate by position_x to place the whole stack
            out[i,0] = tx + position_x
            out[i,1] = y
            out[i,2] = tz

        return out

    def render_dna_stack(self, position_x, height, twist_amount, uncoil_amount):
        """Draw one vertical double helix stack at x=position_x.

        Parameters are exact spec-controlled. This function draws:
         - left (blue) strand
         - right (red) strand
         - horizontal rungs between strands using tint colors
        The stack remains vertical (y = up axis)."""
        # Use the template but allow height override
        template = self.stack_template
        segments = template['segments']

        # sample scaling if height differs
        pts_a = template['strand_a'].copy()
        pts_b = template['strand_b'].copy()
        # scale Y to requested height
        scale = height / template['height']
        pts_a[:,1] *= scale
        pts_b[:,1] *= scale

        # apply twist/uncoil transforms
        self.twist_amount = twist_amount
        self.uncoil_amount = uncoil_amount

        ta = self._apply_twist_uncoil(pts_a, 0, position_x)
        tb = self._apply_twist_uncoil(pts_b, 1, position_x)

        # enable smooth lines
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_LINE_SMOOTH)

        # Draw left strand (blue)
        glLineWidth(3.0)
        glBegin(GL_LINE_STRIP)
        for v in ta:
            glColor3f(*self.COLOR_BLUE)
            glVertex3f(v[0]*self.zoom, v[1]*self.zoom, v[2]*self.zoom)
        glEnd()

        # Draw right strand (red)
        glLineWidth(3.0)
        glBegin(GL_LINE_STRIP)
        for v in tb:
            glColor3f(*self.COLOR_RED)
            glVertex3f(v[0]*self.zoom, v[1]*self.zoom, v[2]*self.zoom)
        glEnd()

        # Draw horizontal rungs between corresponding samples
        glLineWidth(2.0)
        glBegin(GL_LINES)
        for i in range(segments):
            va = ta[i]
            vb = tb[i]
            # choose rung tint by averaging the strand colors; alternate left/right tint depending on height step
            # To follow spec, use lighter tint of the same colors but draw rung as gradient: left half blue tint -> right half red tint
            glColor3f(*self.RUNG_BLUE)
            glVertex3f(va[0]*self.zoom, va[1]*self.zoom, va[2]*self.zoom)
            glColor3f(*self.RUNG_RED)
            glVertex3f(vb[0]*self.zoom, vb[1]*self.zoom, vb[2]*self.zoom)
        glEnd()

        # restore states
        glDisable(GL_LINE_SMOOTH)
        glDisable(GL_BLEND)

    def render_two_stacks(self, center_x=0.0, separation=2.0, height=None):
        """Render two vertical stacks (A left, B right) as required by spec."""
        if height is None:
            height = self.stack_height
        left_x = center_x - separation * 0.5
        right_x = center_x + separation * 0.5
        self.render_dna_stack(left_x, height, self.twist_amount, self.uncoil_amount)
        self.render_dna_stack(right_x, height, self.twist_amount, self.uncoil_amount)

