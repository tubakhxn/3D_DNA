import math
import numpy as np


def vec(a, b, c=0.0):
    return np.array([a, b, c], dtype=float)


def length(v):
    return float(np.linalg.norm(v))


def normalize(v):
    v = np.array(v, dtype=float)
    n = np.linalg.norm(v)
    if n == 0:
        return v
    return v / n


def clamp(x, a, b):
    return max(a, min(b, x))


def angle_between(a, b):
    a = np.array(a, dtype=float)
    b = np.array(b, dtype=float)
    na = np.linalg.norm(a)
    nb = np.linalg.norm(b)
    if na == 0 or nb == 0:
        return 0.0
    cos = np.dot(a, b) / (na * nb)
    cos = max(-1.0, min(1.0, cos))
    return math.degrees(math.acos(cos))
