# game.py
import pygame
import random
import time
from code.settings import WIDTH, HEIGHT, FPS, INITIAL_TIME, TIME_REWARD, SCORE_PER_HIT, INITIAL_TARGET_ACTIVE_MS, \
    MIN_ACTIVE_MS, GAME_MUSIC, GAME_BG
from code.target import Target
from code.score_manager import ScoreManager

class Game:
    """
    Classe que gerencia uma partida. Uso:
      g = Game(screen, clock)
      g.run(player_name)
    """

    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.screen_rect = self.screen.get_rect()
        self.score_manager = ScoreManager()

        # surfaces de background são carregadas internamente para simplicidade
        try:
            self.bg = pygame.image.load(GAME_BG).convert()
            self.bg = pygame.transform.scale(self.bg, (WIDTH, HEIGHT))
        except Exception:
            self.bg = None  # se não existir, pintamos cor sólida

        self.font = pygame.font.SysFont("arial", 22)
        self.large_font = pygame.font.SysFont("arial", 36)

    def run(self, player_name):
        """
        Loop principal da partida. Retorna dicionário com resultado.
        """
        running = True
        score = 0
        start_time = time.time()
        time_left = INITIAL_TIME
        play_time_elapsed = 0.0

        # spawn control
        spawn_timer = 0.0
        spawn_interval = 900  # ms entre tentativas de spawn
        targets = []

        # dynamic difficulty: reduce active_ms conforme acertos
        target_active_ms = INITIAL_TARGET_ACTIVE_MS

        # tocar música de jogo (se existir)
        try:
            pygame.mixer.music.load(GAME_MUSIC)
            pygame.mixer.music.play(-1)
        except Exception:
            pass

        while running:
            dt = self.clock.tick(FPS)  # ms elapsed since last frame
            # atualiza timer em segundos
            time_left -= dt / 1000.0
            play_time_elapsed = time.time() - start_time

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # salva parcial e fecha (tratamento simples)
                    running = False
                    break
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    pos = event.pos
                    for t in targets[:]:
                        if t.handle_click(pos):
                            # acerto
                            score += SCORE_PER_HIT
                            time_left += TIME_REWARD
                            # reduzir time de exibição do alvo progressivamente
                            target_active_ms = max(MIN_ACTIVE_MS, target_active_ms - 60)
                            # remover alvo clicado
                            try:
                                targets.remove(t)
                            except ValueError:
                                pass

            # spawn logic
            spawn_timer += dt
            if spawn_timer >= spawn_interval:
                spawn_timer = 0
                # chance de spawn
                if random.random() < 0.9:  # 90% chance
                    # cria target com warning_ms e active_ms atual
                    t = Target(self.screen_rect, active_ms=target_active_ms)
                    targets.append(t)
                    # Opcional: reduzir spawn_interval conforme o tempo passa (mais alvos)
                    spawn_interval = max(350, spawn_interval - 4)

            # update targets
            for t in targets[:]:
                t.update(dt)
                if not t.is_alive():
                    targets.remove(t)

            # desenhar cena
            if self.bg:
                self.screen.blit(self.bg, (0, 0))
            else:
                self.screen.fill((40, 120, 200))

            # desenha targets
            for t in targets:
                t.draw(self.screen)

            # UI: score e timer
            score_surf = self.font.render(f"Score: {score}", True, (255, 255, 255))
            self.screen.blit(score_surf, (10, 10))
            # timer format mm:ss
            secs = max(0, int(time_left))
            timer_surf = self.font.render(f"Tempo: {secs}s", True, (255, 255, 255))
            self.screen.blit(timer_surf, (WIDTH - 130, 10))

            pygame.display.flip()

            if time_left <= 0:
                running = False

        # partida acabou: parar música de jogo
        try:
            pygame.mixer.music.stop()
        except Exception:
            pass

        # salvar score no DB
        self.score_manager.add_score(player_name, score, play_time_elapsed)

        # mostrar tela de resultados simples e esperar OK
        return self._show_result_screen(player_name, score, play_time_elapsed)

    def _show_result_screen(self, player_name, score, play_time_seconds):
        """
        Mostra a pontuação final e espera clique em 'OK' para retornar.
        """
        waiting = True
        ok_rect = pygame.Rect((WIDTH//2 - 60, HEIGHT//2 + 40, 120, 40))
        small_font = pygame.font.SysFont("arial", 20)
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    break
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    if ok_rect.collidepoint(event.pos):
                        waiting = False
                        break

            if self.bg:
                self.screen.blit(self.bg, (0, 0))
            else:
                self.screen.fill((30, 30, 30))

            title = self.large_font.render("Fim de Jogo", True, (255, 255, 255))
            title_rect = title.get_rect(center=(WIDTH//2, HEIGHT//2 - 60))
            self.screen.blit(title, title_rect)

            score_txt = small_font.render(f"Jogador: {player_name}  |  Pontos: {score}  |  Tempo: {int(play_time_seconds)}s", True, (230, 230, 230))
            st_rect = score_txt.get_rect(center=(WIDTH//2, HEIGHT//2 - 10))
            self.screen.blit(score_txt, st_rect)

            # botão OK
            pygame.draw.rect(self.screen, (180, 180, 180), ok_rect, border_radius=6)
            ok_txt = small_font.render("OK", True, (10, 10, 10))
            ok_txt_rect = ok_txt.get_rect(center=ok_rect.center)
            self.screen.blit(ok_txt, ok_txt_rect)

            pygame.display.flip()
            self.clock.tick(FPS)

        return {"player": player_name, "points": score, "play_time_seconds": play_time_seconds}
