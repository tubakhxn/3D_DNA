import pygame


class MutationMenu:
    def __init__(self, x=350, y=300, w=280, h=220):
        pygame.font.init()
        self.font = pygame.font.SysFont('Arial', 14)
        self.rect = pygame.Rect(x, y, w, h)
        self.visible = False
        self.options = ['substitution', 'deletion', 'insertion', 'frameshift']

    def toggle(self):
        self.visible = not self.visible

    def draw(self, surface):
        if not self.visible:
            return
        pygame.draw.rect(surface, (30, 20, 30), self.rect)
        pygame.draw.rect(surface, (100, 80, 90), self.rect, 2)
        y = self.rect.y + 8
        for opt in self.options:
            r = self.font.render(opt, True, (230,230,230))
            surface.blit(r, (self.rect.x + 8, y))
            y += 24
