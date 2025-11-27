import mediapipe as mp


class HandTracker:
    def __init__(self, max_num_hands=2, min_detection_confidence=0.6, min_tracking_confidence=0.5):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(static_image_mode=False,
                                         max_num_hands=max_num_hands,
                                         min_detection_confidence=min_detection_confidence,
                                         min_tracking_confidence=min_tracking_confidence)

    def process(self, image_rgb):
        # image_rgb: HxWx3 (values 0..255)
        results = self.hands.process(image_rgb)
        hands = []
        if not results.multi_hand_landmarks:
            return hands

        for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
            lm = []
            for p in hand_landmarks.landmark:
                lm.append((p.x, p.y, p.z))

            label = handedness.classification[0].label

            # compute bounding box in normalized coords
            xs = [p[0] for p in lm]
            ys = [p[1] for p in lm]
            min_x, max_x = min(xs), max(xs)
            min_y, max_y = min(ys), max(ys)

            hands.append({
                'landmarks': lm,
                'handedness': label,
                'bbox': (min_x, min_y, max_x, max_y)
            })
        return hands

    def close(self):
        try:
            self.hands.close()
        except Exception:
            pass
