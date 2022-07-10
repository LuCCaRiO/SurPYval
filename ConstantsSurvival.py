import random

BACKGROUND_COLOR = (0, 0, 0)
TILE_SIZE = 32
INVENTORY_HEIGHT = TILE_SIZE * 2

random_dict = {0: "walls", 1: "walls", 2: "walls", 3: "walls", 4: "walls", 5: "sticks", 6: "stones", 7: "walls",
               8: "walls", 9: "walls", 10: "walls", 11: "walls", 12: "walls", 13: "walls", 14: "walls", 15: "walls"}

TILE_MAP = [[]]

for i in range(256):
    TILE_MAP[0].append(random_dict[random.randint(0, 15)])

#

A_KEY = 0
D_KEY = 1
W_KEY = 2
S_KEY = 3
E_KEY = 4
MOUSE_BUTTON_DOWN = 5
ONE_KEY = 6
TWO_KEY = 7
THREE_KEY = 8

SCREEN_WIDTH = TILE_SIZE * 16
SCREEN_HEIGHT = TILE_SIZE * 16 + INVENTORY_HEIGHT
GAME_NAME = "Survival lol"
FPS = 60
