import sys
import os
import time
import cv2
import pygame
from pygame.locals import DOUBLEBUF, OPENGL, QUIT, KEYDOWN, K_d

project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from core.hand_tracker import HandTracker
from core.gesture_engine import GestureEngine
from renderer.renderer import GLRenderer
from ui.overlay import Overlay

def main():
    debug = False

    # Video capture (Webcam)
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    has_camera = cap.isOpened()
    if not has_camera:
        print("No webcam detected — running in fallback keyboard-control mode.")


    hand_tracker = HandTracker(max_num_hands=2)
    gesture_engine = GestureEngine()

    # Initialize pygame + OpenGL renderer
    pygame.init()
    display_size = (1280, 800)
    pygame.display.set_mode(display_size, DOUBLEBUF | OPENGL)
    pygame.display.set_caption('DNA Visualizer - Air Gestures')
    renderer = GLRenderer(size=display_size)
    overlay = Overlay(renderer.width, renderer.height)

    # Register animations
    from animation.twist import TwistAnimation
    from animation.uncoil import UncoilAnimation
    from animation.replication import ReplicationAnimation
    from animation.transcription import TranscriptionAnimation
    from animation.translation import TranslationAnimation
    from animation.temperature import TemperatureAnimation

    twist = TwistAnimation()
    uncoil = UncoilAnimation()
    replication = ReplicationAnimation()
    transcription = TranscriptionAnimation()
    translation = TranslationAnimation()
    temperature = TemperatureAnimation()

    for a in (twist, uncoil, replication, transcription, translation, temperature):
        renderer.register_animation(a)

    running = True
    last_time = time.time()

    try:
        while running:
            now = time.time()
            dt = now - last_time
            last_time = now

            # Handle pygame events
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYDOWN:
                    if event.key == K_d:
                        debug = not debug
                    # toggle external OpenCV webcam preview
                    if event.key == pygame.K_w:
                        overlay.show_webcam = not getattr(overlay, 'show_webcam', True)

            # Read camera frame (or run fallback simulation)
            hands = []
            frame = None
            if has_camera:
                ret, frame = cap.read()
                if not ret:
                    print("WARNING: Camera frame not received")
                    frame = None
                else:
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    hands = hand_tracker.process(frame_rgb)
            else:
                # keyboard fallback: gesture_engine will receive empty hands; we populate gestures via keys below
                hands = []

            # Gesture processing updates state & triggers animations
            gestures = gesture_engine.update(hands, dt)

            # Keyboard simulation when no camera: map keys to gestures
            if not has_camera:
                keys = pygame.key.get_pressed()
                # Two-finger rotate: hold R or T to rotate left/right
                if keys[pygame.K_r]:
                    gestures['two_finger_rotate'] = {'angle': 60.0}
                if keys[pygame.K_t]:
                    gestures['two_finger_rotate'] = {'angle': -60.0}
                # Pinch zoom: Z (zoom in), X (zoom out)
                if keys[pygame.K_z]:
                    gestures['pinch_zoom'] = {'distance': 0.02}
                if keys[pygame.K_x]:
                    gestures['pinch_zoom'] = {'distance': 0.4}
                # Two-hand stretch: U (increase), J (decrease)
                if keys[pygame.K_u]:
                    gestures['two_hand_stretch'] = {'distance': 0.5}
                if keys[pygame.K_j]:
                    gestures['two_hand_stretch'] = {'distance': 0.02}
                # Point: P
                if keys[pygame.K_p]:
                    gestures['finger_point'] = {'origin': (0.5, 0.5, 0.0), 'direction': (0.0, -1.0, 0.0)}
                # Palm down/up: DOWN/UP
                if keys[pygame.K_DOWN]:
                    gestures['palm_down'] = True
                if keys[pygame.K_UP]:
                    gestures['palm_up'] = True
                # Clap: space
                if keys[pygame.K_SPACE]:
                    gestures['clap'] = True
                # Fist: F
                if keys[pygame.K_f]:
                    gestures['fist'] = True
                # Swipe up/down: K (up), L (down)
                if keys[pygame.K_k]:
                    gestures['swipe_up'] = {'speed': 2.0}
                if keys[pygame.K_l]:
                    gestures['swipe_down'] = {'speed': 2.0}
                # Circle wrist: C increases temperature, V decreases
                if keys[pygame.K_c]:
                    gestures['circle_wrist'] = {'delta': 5.0}
                if keys[pygame.K_v]:
                    gestures['circle_wrist'] = {'delta': -5.0}

            # Print detected gestures for debugging/visibility
            if gestures:
                print('DETECTED_GESTURES:', gestures)

            # Apply gestures to renderer and animations
            renderer.apply_gestures(gestures)

            # Update animations and model
            renderer.update(dt)

            # Render
            renderer.render()
            overlay.draw_frame(frame, hands, gestures, debug=debug, has_camera=has_camera)
            pygame.display.flip()

    except KeyboardInterrupt:
        running = False
    finally:
        cap.release()
        hand_tracker.close()
        # ensure OpenCV windows are closed when exiting
        try:
            cv2.destroyAllWindows()
        except Exception:
            pass
        pygame.quit()


if __name__ == '__main__':
    main()
