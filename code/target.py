# target.py
import pygame
import random
from code.settings import *
class Target:
    """
    Representa um alvo com dois estágios:
      1) warning (sombra) - mostra onde alvo aparecerá
      2) active (alvo visível e clicável) - pode ser clicado para pontuação
    """

    def __init__(self, screen_rect: pygame.Rect, active_ms=None, warning_ms=None):
        self.screen_rect = screen_rect
        self.active_ms = active_ms if active_ms is not None else INITIAL_TARGET_ACTIVE_MS
        self.warning_ms = warning_ms if warning_ms is not None else INITIAL_WARNING_MS

        self.shadow_img = pygame.image.load(TARGET_SHADOW_IMG).convert_alpha()

        self.target_img = pygame.image.load(TARGET_IMG).convert_alpha()

        # escala pequena caso seja maior que tela
        max_w = screen_rect.width // 6
        if self.target_img.get_width() > max_w:
            scale = max_w / self.target_img.get_width()
            new_size = (int(self.target_img.get_width()*scale), int(self.target_img.get_height()*scale))
            self.target_img = pygame.transform.smoothscale(self.target_img, new_size)
            self.shadow_img = pygame.transform.smoothscale(self.shadow_img, new_size)

        # posição aleatória dentro de margens
        w, h = self.target_img.get_size()
        x = random.randint(20, screen_rect.width - w - 20)
        y = random.randint(60, screen_rect.height - h - 20)
        self.pos = (x, y)
        self.rect = pygame.Rect(x, y, w, h)

        self.state = "warning"
        self.timer = 0  # ms elapsed since creation

        self._clicked = False

    def update(self, dt):
        """
        dt: milliseconds since last update
        """
        self.timer += dt
        if self.state == "warning" and self.timer >= self.warning_ms:
            self.state = "active"
            # reseta timer para contar o tempo ativo
            self.timer = 0
        elif self.state == "active" and self.timer >= self.active_ms:
            self.state = "expired"

    def draw(self, surface):
        if self.state == "warning":
            surface.blit(self.shadow_img, self.pos)
        elif self.state == "active":
            surface.blit(self.target_img, self.pos)

    def handle_click(self, pos):
        """
        Retorna True se o alvo foi clicado enquanto ativo.
        """
        if self.state == "active" and self.rect.collidepoint(pos):
            self.state = "gone"  # marcado para remoção
            self._clicked = True
            return True
        return False

    def is_alive(self):
        return self.state in ("warning", "active")

    def was_clicked(self):
        return self._clicked
