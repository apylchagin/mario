#!/usr/bin/env python3

import pygame, random
from datetime import datetime
from enum import Enum
from LevelMap import LevelMap
import button
from Static import StaticBackground, StaticScaledBackground
from Animation import AnimatedBackground
from Sprites import SpriteFile, SpriteMoves, SpriteDirection, Sprite

pygame.init()
pygame.mixer.init()

W = 800
H = 600
screen = pygame.display.set_mode((W, H))

FPS = 60
clock = pygame.time.Clock()
running = True

font_path = 'fonts/mario_font.ttf'
font_large = pygame.font.SysFont(font_path, 48)
font_small = pygame.font.SysFont(font_path, 36)

class MapProjectionBlockType(Enum):
    GROUND = '='
    PLAYER = 'p'
    TREE = 't'
    MISC = '\0'
    CLOUD_RIGHT = 'C'
    CLOUD_LEFT = 'c'
    IN_SKY_GOOMBA = '+'

class MapProjectionBlock:
    type = None
    rect = None
    def __init__(self, projection, mapBlock):
        self.type = self.__mapType(mapBlock.type)
        self.rect = pygame.Rect(mapBlock.x * projection.block[0],
                                mapBlock.y * projection.block[1],
                                mapBlock.width * projection.block[0],
                                mapBlock.height * projection.block[1])
    def __mapType(self, type):
        if type == '=':
            return MapProjectionBlockType.GROUND
        if type == '+':
            return MapProjectionBlockType.IN_SKY_GOOMBA
        if type == 'p':
            return MapProjectionBlockType.PLAYER
        if type == 't':
            return MapProjectionBlockType.TREE
        if type == 'C':
            return MapProjectionBlockType.CLOUD_RIGHT
        if type == 'c':
            return MapProjectionBlockType.CLOUD_LEFT
        return MapProjectionBlockType.MISC

    def sizes(self):
        return (self.rect.width, self.rect.height)
    def __str__(self):
        return "[%s, %s]" % (self.type, self.rect)

class MapProjection:
    blocks = None
    block = None
    def __init__(self, map : LevelMap, width, height):
        self.block = (width / map.width, height / map.height)
        self.width = width
        self.height = height
        self.blocks = []
        for block in map.blocks:
            self.blocks.append(MapProjectionBlock(self, block))

    def getBlock(self, type : MapProjectionBlockType) -> MapProjectionBlock:
        for block in self.blocks:
            if block.type == type:
                return block
        return None

    # Provides the line which defines the nearest
    # ground location based for the rect. The middlepoint
    # of the bottom of the rectangle shows is used for
    # the ground detection
    def getGround(self, rect : pygame.Rect) -> pygame.Rect:
        (__x, __y) = rect.midbottom
        __yMinDist = self.height + 1
        __result = None
        # Select all blocks which are above
        # the rectangle
        for block in self.blocks:
            if block.type in [MapProjectionBlockType.GROUND]:
                if (__x >= block.rect.left) and (__x <= block.rect.right) and (__y <= block.rect.top):
                    if (__yMinDist > (block.rect.top - __y)):
                        __result = block.rect
                        __yMinDist = block.rect.top - __y
        if __result is None:
            __result = pygame.Rect(0, 0, 0, 0)
        return __result

# Base class for the playable characters like player and enemy
class Entity:
    def __init__(self, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.x_speed = 0
        self.y_speed = 0
        self.speed = 5
        self.is_out = False
        self.is_dead = False
        self.look_right = True
        self.jump_speed = -12
        self.gravity = 0.5
        self.is_grounded = False

    def handle_input(self):
        pass

    def kill(self):
        self.is_dead = True
        self.x_speed = -self.x_speed
        self.y_speed = self.jump_speed
        self.look_right = self.x_speed > 0

    # Updates the state of the entity based on the
    # current speed on both axises
    def update(self, map: MapProjection):
        __ground = map.getGround(self.rect)
        self.rect.x += self.x_speed
        self.y_speed += self.gravity
        self.rect.y += self.y_speed

        if not self.is_dead:
            if self.rect.top > __ground.top:
                self.is_out = True
            else:
                self.handle_input()

            if self.rect.bottom > __ground.top:
                self.is_grounded = True
                self.y_speed = 0
                self.rect.bottom = __ground.top
        else:
            if self.rect.top > H:
                self.is_out = True
            else:
                self.handle_input()

    # Draws the current state of the character onto the
    # provided surface instance
    def draw(self, surface):
        if self.is_dead:
            surface.blit(self.image.dead.image, self.rect)
        elif self.is_grounded:
            if (self.x_speed > 0) or (self.x_speed < 0):
                if self.look_right:
                    surface.blit(self.image.walk.right.image, self.rect)
                else:
                    surface.blit(self.image.walk.left.image, self.rect)
            else:
                if self.look_right:
                    surface.blit(self.image.stay.right.image, self.rect)
                else:
                    surface.blit(self.image.stay.left.image, self.rect)
        elif self.look_right:
            surface.blit(self.image.jump.right.image, self.rect)
        else:
            surface.blit(self.image.jump.left.image, self.rect)

# Defines player entity
class Player(Entity):
    def __init__(self, image):
        super().__init__(image)
        self.__jumpSound = pygame.mixer.Sound("sounds/jump.wav")
        self.respawn()

    def handle_input(self):
        self.x_speed = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.x_speed = -self.speed
            self.look_right = False
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.x_speed = self.speed
            self.look_right = True
        if self.is_grounded and keys[pygame.K_SPACE]:
            self.is_grounded = False
            self.jump()

    def respawn(self):
        self.is_out = False
        self.is_dead = False
        self.rect.midbottom = (W // 2, H // 2)

    def jump(self):
        self.y_speed = self.jump_speed
        self.__jumpSound.play()


# Defines enemy entity
class Goomba(Entity):
    def __init__(self):
        super().__init__(enemy_image)
        self.spawn()

    def spawn(self):
        direction = random.randint(0, 1)

        if direction == 0:
            self.x_speed = self.speed
            self.rect.bottomright = (0, 0)
        else:
            self.x_speed = -self.speed
            self.rect.bottomleft = (W, 0)

    # Updates the state of the entity based on the
    # current speed on both axises
    def update(self, map: MapProjection):
        super().update(map)
        if (self.x_speed > 0 and self.rect.left > W) or (self.x_speed < 0 and self.rect.right < 0):
            self.is_out = True

backgroundElements = []


# Defines full set of movement related sprites for the enemy
# character
enemy_image = SpriteMoves(
    SpriteDirection(Sprite('images/ngoomba.png', (60, 60)), Sprite('images/ngoomba.png', (60, 60))),
    SpriteDirection(Sprite('images/ngoomba.png', (60, 60)), Sprite('images/ngoomba.png', (60, 60))),
    SpriteDirection(Sprite('images/ngoomba.png', (60, 60)), Sprite('images/ngoomba.png', (60, 60))),
    Sprite('images/deadngoomba.png', (60, 60))
)


class Score:
    value = 0
    def __init__(self, location):
        self.location = location
    def inc(self):
        self.value += 1
    def reset(self):
        self.value = 0
    def draw(self, surface : pygame.Surface):
        score_text_value = "Your score: " +  str(self.value)
        score_text = font_large.render(score_text_value, True, (255, 255, 255))
        score_text_rect = score_text.get_rect()
        score_text_rect.midtop = self.location
        screen.blit(score_text, score_text_rect)
    def moveTo(self, location):
        self.location = location

score = Score((W // 2, 20))

class Timer:
    def __init__(self, location):
        self.location = location
        self.reset()

    def reset(self):
        self.__init = datetime.now()

    def draw(self, surface : pygame.Surface):
        seconds = (datetime.now() - self.__init).total_seconds()
        timer_text_value = "%1d:%02d" % (seconds // 60, seconds % 60)
        timer_text = font_large.render(timer_text_value, True, (255, 255, 255))
        timer_text_rect = timer_text.get_rect()
        timer_text_rect.topleft = self.location
        screen.blit(timer_text, timer_text_rect)

timer = Timer((W // 5, 20))


INIT_DELAY = 2000
DECREASE_BASE = 1.01

class GameConfig:
    def __init__(self):
        self.player = 'Girl'
        self.level = 1 # Possible values: 1, 2, 3

class Game:
    def __init__(self, config: GameConfig):
        self.last_spawn_time = pygame.time.get_ticks()
        self.spawn_delay = INIT_DELAY
        self.goombas = []
        self.running = True
        self.game_over = False
        self.game_over_text = font_large.render('Game Over', True, (255, 255, 255))
        self.game_over_rect = self.game_over_text.get_rect()
        self.game_over_rect = (W // 2 - self.game_over_rect.width // 2, H // 2 - 100)

        self.retry_text = font_small.render('Press any key to continue', True, (255, 255, 255))
        self.retry_rect = self.retry_text.get_rect()
        self.retry_rect = (W // 2 - self.retry_rect.width // 2, H // 2 + 10)


        self.kickSound = pygame.mixer.Sound("sounds/kick.wav")
        self.themeSong = pygame.mixer.Sound("sounds/theme.mp3")
        self.themeSong.play(1000)

        if config.level == 1:
            levelName = "level1.map"
        elif config.level == 2:
            levelName = "level2.map"
        elif config.level == 3:
            levelName = "level3.map"

        levelMap = LevelMap()
        levelMap.loadFromFile(levelName)
        self.projectMap = MapProjection(levelMap, W, H)
        self.load_blocks()

        self.__createPlayer(config)

    def load_blocks(self):
        # Load blocks content per type
        for bgBlock in self.projectMap.blocks:
            if bgBlock.type == MapProjectionBlockType.TREE:
                backgroundElements.append(
                    StaticScaledBackground(bgBlock.rect,
                                           pygame.image.load('images/tree.png'))
                )
            elif bgBlock.type == MapProjectionBlockType.GROUND:
                backgroundElements.append(
                    StaticScaledBackground(bgBlock.rect,
                                           pygame.image.load('images/ground.png'))
                )
            elif bgBlock.type == MapProjectionBlockType.IN_SKY_GOOMBA:
                inSky = AnimatedBackground(
                    bgBlock.rect,
                    SpriteFile('images/inSkyGoomba.png', 11, 1), 200)
                backgroundElements.append(inSky)
            elif bgBlock.type == MapProjectionBlockType.CLOUD_LEFT:
                cloudsLeft = AnimatedBackground(bgBlock.rect,
                                                [pygame.image.load('images/1Clouds.png'),
                                                 pygame.image.load('images/2Clouds.png'),
                                                 pygame.image.load('images/3Clouds.png')],
                                                200)
                backgroundElements.append(cloudsLeft)
            elif bgBlock.type == MapProjectionBlockType.CLOUD_RIGHT:
                cloudsRight = AnimatedBackground(bgBlock.rect,
                                                 [pygame.image.load('images/2Clouds.png'),
                                                  pygame.image.load('images/3Clouds.png'),
                                                  pygame.image.load('images/1Clouds.png')],
                                                 200)
                backgroundElements.append(cloudsRight)

    def process(self, screen : pygame.Surface):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.running = False
            elif e.type == pygame.KEYDOWN:
                if self.player.is_dead:
                    score.reset()
                    timer.reset()
                    self.spawn_delay = INIT_DELAY
                    self.last_spawn_time = pygame.time.get_ticks()
                    self.player.respawn()
                    self.goombas.clear()

        if self.player.is_dead:
            screen.fill((0, 0, 45))
        elif score.value == 0 or (int(score.value / 3) % 2) == 0:
            screen.fill((92, 148, 252))
        else:
            screen.fill((0, 0, 230))

        for element in backgroundElements:
            element.draw(screen)
        score.draw(screen)
        if not self.player.is_dead:
            timer.draw(screen)

        if self.player.is_out:
            score.moveTo((W // 2, H // 2 - 45))
            screen.blit(self.game_over_text, self.game_over_rect)
            screen.blit(self.retry_text, self.retry_rect)
        else:
            now = pygame.time.get_ticks()
            elapsed = now - self.last_spawn_time

            if elapsed > self.spawn_delay:
                self.last_spawn_time = now
                self.goombas.append(Goomba())

            self.player.update(self.projectMap)
            self.player.draw(screen)

            for goomba in list(self.goombas):
                if goomba.is_out:
                    self.goombas.remove(goomba)
                else:
                    goomba.update(self.projectMap)
                    goomba.draw(screen)

                if not self.player.is_dead and not goomba.is_dead and self.player.rect.colliderect(goomba.rect):
                    if (self.player.rect.bottom - self.player.y_speed) < goomba.rect.top:
                        goomba.kill()
                        self.kickSound.play()
                        self.player.jump()
                        score.inc()
                        self.spawn_delay = INIT_DELAY / (DECREASE_BASE ** score.value)
                    else:
                        self.player.kill()

            score.moveTo((W // 2, 10))
        return self.running

    def __createPlayer(self, config : GameConfig):
        # Defines full set of movement related sprites for the player
        # character
        self.player_block = self.projectMap.getBlock(MapProjectionBlockType.PLAYER)
        self.player_image = SpriteMoves(
            SpriteDirection(
                Sprite('images/' + config.player + '.stay.left.png', self.player_block.sizes()),
                Sprite('images/' + config.player + '.stay.right.png', self.player_block.sizes())
            ),
            SpriteDirection(
                Sprite('images/' + config.player + '.jump.left.png', self.player_block.sizes()),
                Sprite('images/' + config.player + '.jump.right.png', self.player_block.sizes())
            ),
            SpriteDirection(
                Sprite('images/' + config.player + '.left.png', self.player_block.sizes()),
                Sprite('images/' + config.player + '.right.png', self.player_block.sizes())
            ),
            Sprite('images/' + config.player + '.dead.png', self.player_block.sizes())
        )
        self.player = Player(self.player_image)

class Menu:
    LEVEL_PLAY = -1
    LEVEL_ROOT = 0
    LEVEL_OPTIONS = 1
    LEVEL_CHAR = 2
    LEVEL_LEVEL = 3

    def __init__(self):
        self.config = GameConfig()
        self.running = True
        self.level = self.LEVEL_ROOT

        self.play_img = pygame.image.load("images/button_play.png").convert_alpha()
        self.options_img = pygame.image.load("images/button_options.png").convert_alpha()
        self.quit_img = pygame.image.load("images/button_quit.png").convert_alpha()
        self.char_img = pygame.image.load('images/button_character.png').convert_alpha()
        self.level_img = pygame.image.load('images/button_level.png').convert_alpha()
        self.keys_img = pygame.image.load('images/button_keys.png').convert_alpha()
        self.back_img = pygame.image.load('images/button_back.png').convert_alpha()
        self.girl_img = pygame.image.load('images/Girl.png').convert_alpha()
        self.boy_img = pygame.image.load('images/Boy.png').convert_alpha()
        self.game_level_1 = pygame.image.load('images/Level1_button.png').convert_alpha()
        self.game_level_2 = pygame.image.load('images/Level2_button.png').convert_alpha()
        self.game_level_3 = pygame.image.load('images/Level3_button.png').convert_alpha()

        self.play_button = button.Button(336, 125, self.play_img, 1)
        self.options_button = button.Button(297, 250, self.options_img, 1)
        self.quit_button = button.Button(336, 375, self.quit_img, 1)
        self.char_button = button.Button(226, 75, self.char_img, 1)
        self.level_button = button.Button(225, 200, self.level_img, 1)
        self.keys_button = button.Button(246, 325, self.keys_img, 1)
        self.back_button = button.Button(332, 450, self.back_img, 1)
        self.boy_button = button.Button(100, 100, self.boy_img, 5)
        self.girl_button = button.Button(400, 100, self.girl_img, 5)
        self.game_level_button_1 = button.Button(200, 100, self.game_level_1, 1)
        self.game_level_button_2 = button.Button(200, 200, self.game_level_2, 1)
        self.game_level_button_3 = button.Button(200, 300, self.game_level_3, 1)

    def process(self, screen : pygame.Surface):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.running = False

        ##screen.fill((238, 18, 137))
        screen.fill((0, 244, 0))
        if self.level == self.LEVEL_ROOT:
            if self.play_button.draw(screen):
                self.level = self.LEVEL_PLAY
            if self.options_button.draw(screen):
                self.level = self.LEVEL_OPTIONS
            if self.quit_button.draw(screen):
                self.running = False
        elif self.level == self.LEVEL_OPTIONS:
            if self.char_button.draw(screen):
                self.level = self.LEVEL_CHAR
            if self.level_button.draw(screen):
                self.level = self.LEVEL_LEVEL
            if self.back_button.draw(screen):
                self.level = self.LEVEL_ROOT
        elif self.level == self.LEVEL_CHAR:
            if self.boy_button.draw(screen):
                self.config.player = 'Boy'
                print("CHAR -> " + str(self.config.player))
            if self.girl_button.draw(screen):
                self.config.player = 'Girl'
                print("CHAR -> " + str(self.config.player))
            if self.back_button.draw(screen):
                self.level = self.LEVEL_ROOT
        elif self.level == self.LEVEL_LEVEL:
            if self.back_button.draw(screen):
                self.level = self.LEVEL_ROOT
            if self.game_level_button_1.draw(screen):
                self.config.level = 1
                print("Level -> " + str(self.config.level))
            if self.game_level_button_2.draw(screen):
                self.config.level = 2
                print("Level -> " + str(self.config.level))
            if self.game_level_button_3.draw(screen):
                self.config.level = 3
                print("Level -> " + str(self.config.level))

        return self.running

menu = Menu()
game = None

# Main drawing loop. Every iteration means drawing of
# the single frame of the game
while running:
    clock.tick(FPS)
    if game == None:
        running = menu.process(screen)
        if running and menu.level == menu.LEVEL_PLAY:
            game = Game(menu.config)
    else:
        running = game.process(screen)
    pygame.display.update()
    pygame.display.flip()
