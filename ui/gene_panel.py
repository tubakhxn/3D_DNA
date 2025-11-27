import pygame


class GenePanel:
    def __init__(self, x=10, y=300, w=320, h=200):
        pygame.font.init()
        self.font = pygame.font.SysFont('Arial', 14)
        self.rect = pygame.Rect(x, y, w, h)
        self.visible = False
        self.gene_info = None

    def show_gene(self, gene_info):
        self.gene_info = gene_info
        self.visible = True

    def hide(self):
        self.visible = False

    def draw(self, surface):
        if not self.visible or not self.gene_info:
            return
        pygame.draw.rect(surface, (20,20,30), self.rect)
        pygame.draw.rect(surface, (80,80,100), self.rect, 2)
        y = self.rect.y + 8
        for k,v in self.gene_info.items():
            txt = f"{k}: {v}"
            r = self.font.render(txt, True, (220,220,220))
            surface.blit(r, (self.rect.x + 8, y))
            y += 18
