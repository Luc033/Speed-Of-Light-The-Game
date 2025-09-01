# main.py
import pygame
import code.settings as settings
from code.menu import Menu

def main():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
    pygame.display.set_caption("Speed Of Light")
    clock = pygame.time.Clock()

    menu = Menu(screen, clock)
    try:
        menu.loop()
    except SystemExit:
        pass
    finally:
        pygame.quit()

if __name__ == "__main__":
    main()
