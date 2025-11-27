import pygame
import cv2
import numpy as np
from pygame import freetype


class Overlay:
    def __init__(self, width, height):
        pygame.font.init()
        self.width = width
        self.height = height
        self.font = pygame.font.SysFont('Arial', 16)
        self.large = pygame.font.SysFont('Arial', 20)
        # Control whether we show an external OpenCV preview window
        self.show_webcam = True

    def draw_frame(self, frame, hands, gestures, debug=False, has_camera=True):
        # frame is BGR from OpenCV; convert to RGB and create surface
        screen = pygame.display.get_surface()
        if has_camera and frame is not None:
            # Also present a separate OpenCV preview window so users can always see themselves
            # This uses the raw BGR frame from OpenCV for minimal latency.
            if getattr(self, 'show_webcam', True):
                try:
                    cv2.imshow('Webcam Preview', frame)
                    cv2.waitKey(1)
                except Exception:
                    # if OpenCV windowing fails for any reason, silently continue to pygame preview
                    pass
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_rgb = np.rot90(frame_rgb)
            surf = pygame.surfarray.make_surface(frame_rgb)
            # small preview in top-right
            preview = pygame.transform.smoothscale(surf, (240, 180))
            screen.blit(preview, (self.width - 250, 10))
        else:
            # show keyboard fallback instructions
            instr_rect = pygame.Rect(self.width - 260, 10, 250, 220)
            pygame.draw.rect(screen, (18,18,22), instr_rect)
            pygame.draw.rect(screen, (80,80,100), instr_rect, 2)
            header = self.large.render('Keyboard Controls (no webcam)', True, (230,230,230))
            screen.blit(header, (instr_rect.x + 6, instr_rect.y + 6))
            lines = [
                'R / T : Rotate left / right',
                'Z / X : Zoom in / out',
                'U / J : Uncoil / Coil',
                'P     : Point (inspect)',
                'UP/DOWN : Palm up / down',
                'SPACE : Clap (replication)',
                'F     : Fist (compress)',
                'K / L : Swipe up / down',
                'C / V : Temp + / - (circle wrist)'
            ]
            y = instr_rect.y + 36
            for line in lines:
                r = self.font.render(line, True, (220,220,220))
                screen.blit(r, (instr_rect.x + 8, y))
                y += 20

        # Draw basic gesture text
        y = 10
        for k,v in gestures.items():
            txt = f"{k}: {v}"
            r = self.font.render(txt, True, (240,240,240))
            screen.blit(r, (10, y))
            y += 18

        # debug: draw landmarks
        if debug and hands:
            for h in hands:
                for (x,y,z) in h['landmarks']:
                    sx = int(x * self.width)
                    sy = int(y * self.height)
                    pygame.draw.circle(screen, (255, 100, 100), (sx, sy), 3)

        # If two-hand stretch present, draw centers and connecting line for debugging
        if 'two_hand_stretch' in gestures:
            info = gestures['two_hand_stretch']
            if 'center0' in info and 'center1' in info:
                c0 = info['center0']
                c1 = info['center1']
                # normalized coords -> screen
                x0 = int(c0[0] * self.width)
                y0 = int(c0[1] * self.height)
                x1 = int(c1[0] * self.width)
                y1 = int(c1[1] * self.height)
                pygame.draw.circle(screen, (200,200,50), (x0, y0), 8, 2)
                pygame.draw.circle(screen, (200,50,200), (x1, y1), 8, 2)
                pygame.draw.line(screen, (180,180,180), (x0, y0), (x1, y1), 2)
                # show distance
                d = info.get('distance', 0.0)
                txt = self.font.render(f"hands dist: {d:.3f}", True, (240,240,240))
                screen.blit(txt, ((x0+x1)//2 + 6, (y0+y1)//2 + 6))
