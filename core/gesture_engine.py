import time
import math
from collections import deque
from .gesture_definitions import *
from .utils import angle_between, normalize


class GestureEngine:
    """Heuristics-based gesture detection using MediaPipe landmarks.

    Uses simple geometric rules and short temporal history to detect gestures.
    """

    def __init__(self):
        self.prev_hands = []
        self.history = deque(maxlen=32)
        self.last_swipe_time = 0
        self.swipe_cooldown = 0.4

    def update(self, hands, dt):
        gestures = {}
        now = time.time()
        self.history.append({'time': now, 'hands': hands})

        if len(hands) >= 1:
            h = hands[0]
            lm = h['landmarks']

            # Two-finger rotate: angle between index & middle finger vectors
            angle = angle_between(
                (lm[INDEX_TIP][0] - lm[INDEX_PIP][0], lm[INDEX_TIP][1] - lm[INDEX_PIP][1]),
                (lm[MIDDLE_TIP][0] - lm[MIDDLE_PIP][0], lm[MIDDLE_TIP][1] - lm[MIDDLE_PIP][1])
            )
            gestures[GEST_ROTATE] = {'angle': angle}

            # Pinch: thumb tip to index tip distance
            pinch_dist = math.hypot(lm[THUMB_TIP][0] - lm[INDEX_TIP][0], lm[THUMB_TIP][1] - lm[INDEX_TIP][1])
            gestures[GEST_PINCH] = {'distance': pinch_dist}

            # Point detection
            index_extended = lm[INDEX_TIP][1] < lm[INDEX_PIP][1]
            others_folded = all(lm[i][1] > lm[i-2][1] for i in (MIDDLE_TIP, RING_TIP, PINKY_TIP))
            if index_extended and others_folded:
                origin = lm[INDEX_TIP]
                direction = normalize((lm[INDEX_TIP][0]-lm[INDEX_PIP][0], lm[INDEX_TIP][1]-lm[INDEX_PIP][1], lm[INDEX_TIP][2]-lm[INDEX_PIP][2]))
                gestures[GEST_POINT] = {'origin': origin, 'direction': direction}

            # Palm up/down simple heuristic via cross product z
            v1 = (lm[PINKY_MCP][0]-lm[INDEX_MCP][0], lm[PINKY_MCP][1]-lm[INDEX_MCP][1], lm[PINKY_MCP][2]-lm[INDEX_MCP][2])
            v2 = (lm[MIDDLE_MCP][0]-lm[WRIST][0], lm[MIDDLE_MCP][1]-lm[WRIST][1], lm[MIDDLE_MCP][2]-lm[WRIST][2])
            normal_z = v1[0]*v2[1] - v1[1]*v2[0]
            if normal_z < -0.01:
                gestures[GEST_PALM_DOWN] = True
            elif normal_z > 0.01:
                gestures[GEST_PALM_UP] = True

        # Two-hand stretch & clap — stabilize by averaging recent frames
        recent = list(self.history)[-6:]
        two_hand_entries = [e for e in recent if len(e['hands']) == 2]
        if len(two_hand_entries) >= 2:
            centers = []
            dists = []
            for entry in two_hand_entries:
                h0, h1 = entry['hands'][0], entry['hands'][1]
                c0 = ((h0['bbox'][0] + h0['bbox'][2]) / 2.0, (h0['bbox'][1] + h0['bbox'][3]) / 2.0)
                c1 = ((h1['bbox'][0] + h1['bbox'][2]) / 2.0, (h1['bbox'][1] + h1['bbox'][3]) / 2.0)
                centers.append((c0, c1))
                dists.append(math.hypot(c0[0]-c1[0], c0[1]-c1[1]))

            mean_dist = sum(dists) / len(dists)
            # average centers for a stable visual
            avg_c0 = (sum(c[0][0] for c in centers) / len(centers), sum(c[0][1] for c in centers) / len(centers))
            avg_c1 = (sum(c[1][0] for c in centers) / len(centers), sum(c[1][1] for c in centers) / len(centers))

            gestures[GEST_STRETCH] = {'distance': mean_dist, 'center0': avg_c0, 'center1': avg_c1}

            # Clap when averaged distance is below threshold
            if mean_dist < 0.12:
                gestures[GEST_CLAP] = True

        # Fist detection: fingertips near their lower joints
        for h in hands:
            lm = h['landmarks']
            avg_tip_dist = sum(math.hypot(lm[i][0]-lm[i-3][0], lm[i][1]-lm[i-3][1]) for i in (INDEX_TIP, MIDDLE_TIP, RING_TIP, PINKY_TIP))/4.0
            if avg_tip_dist < 0.03:
                gestures[GEST_FIST] = True

        # Swipe up/down using history
        if len(self.history) >= 6:
            first = self.history[0]
            last = self.history[-1]
            if first['hands'] and last['hands']:
                fy = first['hands'][0]['landmarks'][INDEX_TIP][1]
                ly = last['hands'][0]['landmarks'][INDEX_TIP][1]
                diff = fy - ly
                dt = last['time'] - first['time']
                if dt > 0:
                    speed = diff / dt
                    if speed > 1.0 and (time.time() - self.last_swipe_time) > self.swipe_cooldown:
                        gestures[GEST_SWIPE_UP] = {'speed': speed}
                        self.last_swipe_time = time.time()
                    elif speed < -1.0 and (time.time() - self.last_swipe_time) > self.swipe_cooldown:
                        gestures[GEST_SWIPE_DOWN] = {'speed': -speed}
                        self.last_swipe_time = time.time()

        # Pinch+rotate detection
        if len(hands) >= 1:
            angles = []
            for entry in self.history:
                hs = entry['hands']
                if hs:
                    lm = hs[0]['landmarks']
                    ang = angle_between((lm[INDEX_TIP][0]-lm[INDEX_PIP][0], lm[INDEX_TIP][1]-lm[INDEX_PIP][1]), (lm[MIDDLE_TIP][0]-lm[MIDDLE_PIP][0], lm[MIDDLE_TIP][1]-lm[MIDDLE_PIP][1]))
                    angles.append(ang)
            if len(angles) >= 3:
                rot_speed = (angles[-1] - angles[0]) / max(1e-6, (len(angles)-1))
                if 'pinch_zoom' in gestures and gestures['pinch_zoom']['distance'] < 0.05 and abs(rot_speed) > 0.5:
                    gestures[GEST_PINCH_ROTATE] = {'rot_speed': rot_speed}

        self.prev_hands = hands
        return gestures
