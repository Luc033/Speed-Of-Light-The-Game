import os

# Caminho base do projeto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Pasta de assets
ASSET_DIR = os.path.join(BASE_DIR, "asset")

# Window
WIDTH = 720
HEIGHT = 480
FPS = 60

# Assets
MENU_BG = os.path.join(ASSET_DIR, "image", "menu_bg.png")
GAME_BG = os.path.join(ASSET_DIR, "image", "game_bg.png")
TARGET_IMG = os.path.join(ASSET_DIR, "image", "target.png")
TARGET_SHADOW_IMG = os.path.join(ASSET_DIR, "image", "target_shadow.png")

MENU_MUSIC = os.path.join(ASSET_DIR, "audio", "menu_music.mp3")
GAME_MUSIC = os.path.join(ASSET_DIR, "audio", "game_music.mp3")



# Gameplay
INITIAL_TIME = 30.0            # segundos por partida
TIME_REWARD = 2.0             # segundos adicionados por acerto
INITIAL_TARGET_ACTIVE_MS = 1500  # tempo que alvo fica ativo em ms (será reduzido)
INITIAL_WARNING_MS = 700        # tempo da sombra antes do alvo aparecer
MIN_ACTIVE_MS = 400             # limite mínimo para o tempo ativo (dificuldade)
SCORE_PER_HIT = 10
DB_FILE = os.path.join(BASE_DIR, "scores.db")
