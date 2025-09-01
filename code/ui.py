# ui.py
import pygame

class Button:
    """
    Botão simples com retângulo, texto e callback.
    """

    def __init__(self, rect, text, font, callback):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.callback = callback
        self.hover = False

    def draw(self, surface):
        color = (200, 200, 200) if self.hover else (160, 160, 160)
        pygame.draw.rect(surface, color, self.rect, border_radius=6)
        # borda
        pygame.draw.rect(surface, (80, 80, 80), self.rect, 2, border_radius=6)
        # texto
        txt = self.font.render(self.text, True, (10, 10, 10))
        txt_rect = txt.get_rect(center=self.rect.center)
        surface.blit(txt, txt_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hover = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.callback()
