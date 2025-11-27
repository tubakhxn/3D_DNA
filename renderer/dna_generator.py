import numpy as np


def generate_parametric_stack(height=6.0, segments=360, radius=0.4, step_angle_deg=36.0, phase=0.0):
    """
    Generate smooth parametric points for a vertical double helix stack.

    x = A * sin(theta + phase)
    y = linear from 0..height
    We sample `segments` points; each segment advances angle by `step_angle_deg` degrees.

    Returns dict with:
      - strand_a: np.array of shape (segments,3)
      - strand_b: np.array of shape (segments,3)
      - rungs: list of (i,j) indices between corresponding points
    """
    theta_step = np.deg2rad(step_angle_deg)
    # adjust theta per sample so that each adjacent sample advances by theta_step
    thetas = phase + np.arange(segments) * theta_step
    ys = np.linspace(0.0, height, segments)

    strand_a = np.zeros((segments, 3), dtype=np.float32)
    strand_b = np.zeros((segments, 3), dtype=np.float32)
    rungs = []

    for i in range(segments):
        t = thetas[i]
        y = ys[i]
        xa = radius * np.sin(t)
        za = radius * np.cos(t)
        xb = radius * np.sin(t + np.pi)
        zb = radius * np.cos(t + np.pi)
        # Keep vertical axis as Y
        strand_a[i] = (xa, y, za)
        strand_b[i] = (xb, y, zb)
        rungs.append((i, i))

    return {
        'strand_a': strand_a,
        'strand_b': strand_b,
        'rungs': rungs,
        'segments': segments,
        'height': height,
        'radius': radius,
        'step_angle_deg': step_angle_deg,
    }

