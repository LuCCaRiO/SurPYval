import pygame
import random
from ConstantsSurvival import *
from math import *


class Tile:
    def __init__(self, image, x, y, img_code):
        self.animation = 0
        self.image = image[self.animation]
        self.rect = image[self.animation].get_rect()
        self.rect.x, self.rect.y = x, y
        self.img_code = img_code


class InvetoryTile:
    def __init__(self, image, x, y, id_, font):
        self.animation = 0
        self.image = image[self.animation]
        self.rect = pygame.Surface(image[self.animation].get_size())
        self.x, self.y = x, y
        self.img_code = id_
        self.font = font


class CraftingTile:
    def __init__(self, image, x, y, id_, font):
        self.animation = 1
        self.image = image[self.animation]
        self.rect = pygame.Surface(image[self.animation].get_size())
        self.x, self.y = x, y
        self.img_code = id_
        self.font = font


class Player:
    def __init__(self, image, x, y, img_code, speed):
        self.animation = 0
        self.image = image[self.animation]
        self.rect = image[self.animation].get_rect()
        self.rect.x, self.rect.y = x, y
        self.img_code = img_code
        self.speed = speed
        self.speed_x = 0
        self.speed_y = 0


class TileMap:
    def __init__(self, tile_map_number, img_code_dict, row, column):
        self.tile_map_number = tile_map_number
        self.img_code_dict = img_code_dict
        self.row, self.column = row, column

    def read_tiles(self):
        map_ = []
        j = 0

        # tilemap

        for column in range(self.column):
            for row in range(self.row):
                map_.append(
                    Tile(self.img_code_dict[TILE_MAP[self.tile_map_number][j]], row * TILE_SIZE, column * TILE_SIZE,
                         TILE_MAP[self.tile_map_number][j]))
                j += 1

        return map_


def hitbox_check(object_, list_):
    objects = []
    for object__ in list_:
        for object___ in object_:
            if object__.img_code == object___:
                objects.append(object__)
    return objects


class Game:
    def __init__(self):
        self.entitys = []
        self.tile_map_number = None
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(GAME_NAME)

        self.img_code_dict = {"rocks": [pygame.image.load("./img/rock.png"), pygame.image.load("./img/rock2.png")],
                              "woods": [pygame.image.load("./img/wood.png"), pygame.image.load("./img/wood2.png")],
                              "sticks": [pygame.image.load("./img/stick.png")],
                              "stones": [pygame.image.load("./img/wall1.png")],
                              "walls": [pygame.image.load("./img/pixil-frame-0.png")],
                              "player": [pygame.image.load("./img/player.png")]}

        self.invetory = {"sticks": 0, "stones": 0, "woods": 0, "rocks": 0}
        self.select_dict = {1: "sticks", 2: "stones", 3: "woods", 4: "rocks"}
        self.selected = 1

        self.receipe = {"woods": 5, "rocks": 10}  # 5 sticks --> 1 wood, 10 stones --> 1 rock

        self.change_map(0)

        self.entitys.append(
            Player(self.img_code_dict["player"], SCREEN_WIDTH / 2 - TILE_SIZE / 2,
                   SCREEN_HEIGHT / 2 - INVENTORY_HEIGHT - TILE_SIZE / 2, "player",
                   3))

        self.quantitas_font = pygame.font.SysFont("impact", 15)
        self.normal_font = pygame.font.SysFont("bahnschrift", 20)

        self.entitys.append(
            InvetoryTile(self.img_code_dict["sticks"], 0, SCREEN_HEIGHT - TILE_SIZE, "sticks", self.quantitas_font))
        self.entitys.append(
            InvetoryTile(self.img_code_dict["stones"], TILE_SIZE, SCREEN_HEIGHT - TILE_SIZE, "stones",
                         self.quantitas_font))
        self.entitys.append(
            InvetoryTile(self.img_code_dict["woods"], TILE_SIZE * 2, SCREEN_HEIGHT - TILE_SIZE, "woods",
                         self.quantitas_font))
        self.entitys.append(
            InvetoryTile(self.img_code_dict["rocks"], TILE_SIZE * 3, SCREEN_HEIGHT - TILE_SIZE, "rocks",
                         self.quantitas_font))
        self.entitys.append(
            CraftingTile(self.img_code_dict["woods"], SCREEN_WIDTH / 2, SCREEN_HEIGHT - TILE_SIZE, "woods",
                         self.quantitas_font))
        self.entitys.append(
            CraftingTile(self.img_code_dict["rocks"], SCREEN_WIDTH / 2 + TILE_SIZE, SCREEN_HEIGHT - TILE_SIZE, "rocks",
                         self.quantitas_font))

        self.game_running = True

    def run(self):
        clock = pygame.time.Clock()
        while self.game_running:
            user_command = self.handle_events()
            self.physics(user_command)
            self.render()
            clock.tick(FPS)

    def handle_events(self):
        user_command = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    user_command.append(E_KEY)
                if event.key == pygame.K_1:
                    user_command.append(ONE_KEY)
                if event.key == pygame.K_2:
                    user_command.append(TWO_KEY)
                if event.key == pygame.K_3:
                    user_command.append(THREE_KEY)
                if event.key == pygame.K_4:
                    user_command.append(FOUR_KEY)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                user_command.append(MOUSE_BUTTON_DOWN)
        key = pygame.key.get_pressed()
        if key[pygame.K_w] and not key[pygame.K_s]:
            user_command.append(W_KEY)
        if key[pygame.K_s] and not key[pygame.K_w]:
            user_command.append(S_KEY)
        if key[pygame.K_d] and not key[pygame.K_a]:
            user_command.append(D_KEY)
        if key[pygame.K_a] and not key[pygame.K_d]:
            user_command.append(A_KEY)
        return user_command

    def render(self):
        self.screen.fill(BACKGROUND_COLOR)

        for entity in self.entitys:
            if isinstance(entity, InvetoryTile):
                if entity.img_code == self.select_dict[self.selected]:
                    quantitas_text = entity.font.render(str(self.invetory[entity.img_code]), True, (0, 0, 0))
                else:
                    quantitas_text = entity.font.render(str(self.invetory[entity.img_code]), True, (255, 255, 255))
                entity.rect.blit(entity.image, (0, 0))
                entity.rect.blit(quantitas_text, (0, 0))
                self.screen.blit(entity.rect, (entity.x, entity.y))
            elif isinstance(entity, CraftingTile):
                entity.rect.blit(entity.image, (0, 0))
                self.screen.blit(entity.rect, (entity.x, entity.y))
            else:
                self.screen.blit(entity.image, (entity.rect.x, entity.rect.y))

        inventory_text = self.normal_font.render("Inventory", True, (255, 255, 255))
        crafting_text = self.normal_font.render("Crafting", True, (255, 255, 255))

        self.screen.blit(inventory_text, (0, SCREEN_HEIGHT - INVENTORY_HEIGHT))
        self.screen.blit(crafting_text, (SCREEN_WIDTH / 2, SCREEN_HEIGHT - INVENTORY_HEIGHT))

        pygame.display.flip()

    def physics(self, user_command):
        mouse = pygame.mouse.get_pos()
        walls = hitbox_check(["woods", "rocks"], self.entitys)
        players = hitbox_check(["player"], self.entitys)

        if ONE_KEY in user_command:
            self.selected = 1
        if TWO_KEY in user_command:
            self.selected = 2
        if THREE_KEY in user_command:
            self.selected = 3
        if FOUR_KEY in user_command:
            self.selected = 4

        for entity in self.entitys:
            if isinstance(entity, Player):
                entity.speed_x = 0
                entity.speed_y = 0
                if W_KEY in user_command and 0 < entity.rect.top:
                    entity.speed_y = -entity.speed
                if S_KEY in user_command and SCREEN_HEIGHT - INVENTORY_HEIGHT > entity.rect.bottom:
                    entity.speed_y = entity.speed
                if D_KEY in user_command and SCREEN_WIDTH > entity.rect.right:
                    entity.speed_x = entity.speed
                if A_KEY in user_command and 0 < entity.rect.left:
                    entity.speed_x = -entity.speed

                for wall in walls:
                    if isinstance(wall, Tile):
                        rect = pygame.Rect(entity.rect.x, entity.rect.y, entity.image.get_width(),
                                           entity.image.get_height())
                        rect.y += entity.speed_y
                        rect.x += entity.speed_x
                        if wall.rect.colliderect(rect):
                            if entity.speed_y != 0:
                                entity.speed_y = 0

                            if entity.speed_x != 0:
                                entity.speed_x = 0

                entity.rect.x += entity.speed_x
                entity.rect.y += entity.speed_y

            if isinstance(entity, CraftingTile):
                if entity.img_code == "woods":
                    self.get_tile(entity, "sticks", user_command)
                if entity.img_code == "rocks":
                    self.get_tile(entity, "stones", user_command)

            if isinstance(entity, Tile):
                for player in players:
                    if entity.img_code == "walls" and pygame.Rect(entity.rect).collidepoint(
                            mouse) and MOUSE_BUTTON_DOWN in user_command and self.invetory[
                        self.select_dict[self.selected]] >= 1 and not \
                            player.rect.colliderect(entity.rect):
                        self.invetory[self.select_dict[self.selected]] -= 1
                        tile_number = self.entitys.index(entity)
                        self.entitys.remove(entity)
                        self.entitys.insert(tile_number,
                                            Tile(self.img_code_dict[self.select_dict[self.selected]], entity.rect.x,
                                                 entity.rect.y,
                                                 self.select_dict[self.selected]))
                    elif entity.img_code != "walls" and pygame.Rect(entity.rect).collidepoint(
                            mouse) and MOUSE_BUTTON_DOWN in user_command:
                        self.invetory[entity.img_code] += 1
                        tile_number = self.entitys.index(entity)
                        self.entitys.remove(entity)
                        self.entitys.insert(tile_number,
                                            Tile(self.img_code_dict["walls"], entity.rect.x, entity.rect.y, "walls"))

    def change_map(self, map_number):
        self.tile_map_number = map_number
        self.entitys = TileMap(0, self.img_code_dict,
                               ceil(SCREEN_WIDTH / TILE_SIZE),
                               ceil((SCREEN_HEIGHT - INVENTORY_HEIGHT) / TILE_SIZE)).read_tiles()

    def get_tile(self, entity, item, user_command):
        mouse = pygame.mouse.get_pos()
        if self.invetory[item] >= self.receipe[entity.img_code]:
            if entity.animation != 0:
                entity.animation = 0
                entity.image = self.img_code_dict[entity.img_code][entity.animation]
                entity.rect = pygame.Surface(
                    self.img_code_dict[entity.img_code][entity.animation].get_size())

            rect = pygame.Rect((entity.x, entity.y, entity.image.get_width(), entity.image.get_height()))
            if rect.collidepoint(mouse) and MOUSE_BUTTON_DOWN in user_command:
                self.invetory[item] -= self.receipe[entity.img_code]
                self.invetory[entity.img_code] += 1
        else:
            entity.animation = 1
            entity.image = self.img_code_dict[entity.img_code][entity.animation]
            entity.rect = pygame.Surface(
                self.img_code_dict[entity.img_code][entity.animation].get_size())


if __name__ == "__main__":
    pygame.init()
    Game().run()
