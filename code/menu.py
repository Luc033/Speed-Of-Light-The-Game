# menu.py
import pygame

from code.settings import MENU_BG
from code.ui import Button
from code.game import Game
from code.score_manager import ScoreManager
import code.settings as settings

class Menu:
    """
    Menu principal com 3 opções: Iniciar jogo, Score e Sair.
    Também mostra tela de pontuação (Score) com nome e pontos/hora.
    """

    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.screen_rect = screen.get_rect()
        self.score_manager = ScoreManager()
        self.font = pygame.font.SysFont("arial", 22)
        self.large_font = pygame.font.SysFont("arial", 36)

        # carregar background de menu
        try:
            self.bg = pygame.image.load(MENU_BG).convert()
            self.bg = pygame.transform.scale(self.bg, (settings.WIDTH, settings.HEIGHT))
        except Exception:
            self.bg = None

        # criar botões
        self.buttons = []
        midx = settings.WIDTH // 2
        self._create_buttons(midx)

        # música do menu (opcional)
        try:
            pygame.mixer.music.load(settings.MENU_MUSIC)
            pygame.mixer.music.play(-1)
        except Exception:
            pass

    def _create_buttons(self, midx):
        btn_w, btn_h = 200, 50
        spacing = 12
        start_y = 240
        font = pygame.font.SysFont("arial", 24)
        self.buttons = [
            Button((midx - btn_w//2, start_y, btn_w, btn_h), "Iniciar Jogo", font, self._on_start),
            Button((midx - btn_w//2, start_y + (btn_h + spacing), btn_w, btn_h), "Score", font, self._on_score),
            Button((midx - btn_w//2, start_y + 2*(btn_h + spacing), btn_w, btn_h), "Sair", font, self._on_exit),
        ]

    def loop(self):
        """
        Loop do menu principal. Retorna False quando o usuário escolhe 'Sair'.
        """
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                for b in self.buttons:
                    b.handle_event(event)

            if self.bg:
                self.screen.blit(self.bg, (0, 0))
            else:
                self.screen.fill((20, 90, 150))

            title = self.large_font.render("Speed of Light", True, (255, 255, 255))
            title_rect = title.get_rect(center=(settings.WIDTH//2, 120))
            self.screen.blit(title, title_rect)

            for b in self.buttons:
                b.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(settings.FPS)

        return False

    def _on_start(self):
        """
        Callback do botão iniciar: solicita nome e inicia Game.run.
        """
        # pausar música do menu para partida
        try:
            pygame.mixer.music.stop()
        except Exception:
            pass

        player_name = self._ask_player_name()
        if not player_name:
            # se o jogador cancelar, retorna ao menu e retoma música
            try:
                pygame.mixer.music.load(settings.MENU_MUSIC)
                pygame.mixer.music.play(-1)
            except Exception:
                pass
            return

        game = Game(self.screen, self.clock)
        result = game.run(player_name)

        # após partida, retocar música do menu
        try:
            pygame.mixer.music.load(settings.MENU_MUSIC)
            pygame.mixer.music.play(-1)
        except Exception:
            pass

    def _ask_player_name(self):
        """
        Mostra uma caixa simples para o jogador digitar o nome.
        Retorna string (pode ser vazia) ou None se cancelado.
        """
        active = True
        name = ""
        input_rect = pygame.Rect(settings.WIDTH//2 - 200, settings.HEIGHT//2 - 20, 400, 40)
        base_font = pygame.font.SysFont("arial", 24)

        while active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return name.strip() or "Jogador"
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    elif event.key == pygame.K_ESCAPE:
                        return None
                    else:
                        if len(name) < 20:
                            name += event.unicode

            if self.bg:
                self.screen.blit(self.bg, (0, 0))
            else:
                self.screen.fill((15, 15, 15))

            prompt = base_font.render("Digite seu nome e pressione Enter (Esc para cancelar):", True, (230, 230, 230))
            self.screen.blit(prompt, (settings.WIDTH//2 - prompt.get_width()//2, settings.HEIGHT//2 - 80))

            pygame.draw.rect(self.screen, (255, 255, 255), input_rect, 2)
            txt_surface = base_font.render(name, True, (255, 255, 255))
            self.screen.blit(txt_surface, (input_rect.x + 8, input_rect.y + 6))

            pygame.display.flip()
            self.clock.tick(settings.FPS)

    def _on_score(self):
        """
        Exibe a tela de scores (top 10).
        """
        rows = self.score_manager.top_scores(10)
        showing = True
        while showing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    showing = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        showing = False
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    # clique para voltar
                    showing = False

            if self.bg:
                self.screen.blit(self.bg, (0, 0))
            else:
                self.screen.fill((10, 10, 10))

            title = self.large_font.render("Scoreboard (Top 10)", True, (255, 255, 255))
            self.screen.blit(title, (settings.WIDTH//2 - title.get_width()//2, 40))

            y = 120
            small = self.font
            if not rows:
                no_txt = small.render("Nenhuma pontuação registrada.", True, (220, 220, 220))
                self.screen.blit(no_txt, (settings.WIDTH//2 - no_txt.get_width()//2, y))
            else:
                # cabeçalho
                hdr = small.render(f"{'Jogador':<20}{'Pontos':>8}{'Tempo(s)':>12}", True, (220,220,220))
                self.screen.blit(hdr, (80, y))
                y += 30
                for r in rows:
                    player_name, points, play_time_seconds, created_at = r
                    line = small.render(f"{player_name:<20}{points:>8}{int(play_time_seconds):>12}", True, (210,210,210))
                    self.screen.blit(line, (80, y))
                    y += 26

            hint = self.font.render("Pressione Esc ou clique para voltar.", True, (180, 180, 180))
            self.screen.blit(hint, (settings.WIDTH//2 - hint.get_width()//2, settings.HEIGHT - 50))

            pygame.display.flip()
            self.clock.tick(settings.FPS)

    def _on_exit(self):
        """
        Fecha o jogo. Chamamos quit aqui.
        """
        pygame.quit()
        raise SystemExit()
