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
    FLOWERS = 'f'
    NEW_GROUND = 'n'
    BLACK_GROUND = 'b'
    HOUSE = 'h'
    RED_GROUND = 'r'
    SUN = 's'
    GREEN_GROUND = 'g'
    RED_HOUSE = 'R'
    GROUND_2 = '2'
    GROUND_3 = '3'
    GROUND_4 = '4'
    GROUND_5 = '5'
    GROUND_6 = '6'
    GROUND_7 = '7'
    GROUND_8 = '8'
    GROUND_9 = '9'
    GROUND_10 = '%'
    GROUND_11 = '!'
    GROUND_12 = '/'
    GROUND_13 = '?'
    GROUND_14 = '>'
    GROUND_15 = ':'
    GROUND_16 = ';'
    GROUND_17 = '<'
    GROUND_18 = ')'
    #
    GROUND_19 = 'j'
    GROUND_20 = 'O'
    GROUND_21 = 'o'
    GROUND_22 = 'A'
    GROUND_23 = 'a'
    GROUND_24 = 'J'
    GROUND_25 = 'P'
    GROUND_26 = 'F'
    GROUND_27 = 'N'
    GROUND_28 = 'B'
    GROUND_29 = 'H'
    GROUND_30 = 'T'
    #
    PALM1 = 'z'
    PALM2 = 'Z'
    NLO = 'm'
    PLANET1 = 'v'
    PLANET2 = 'V'
    ROSE = '^'
    #
    OFLOWER = 'L'
    MAC = 'd'
    WFLOWER = 'D'
    YFLOWER = 'x'
    BFLOWER = 'X'
    
    

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
        if type == 'm':
            return MapProjectionBlockType.NLO
        if type == 'p':
            return MapProjectionBlockType.PLAYER
        if type == 't':
            return MapProjectionBlockType.TREE
        if type == 'C':
            return MapProjectionBlockType.CLOUD_RIGHT
        if type == 'f':
            return MapProjectionBlockType.FLOWERS
        if type == 'n':
            return MapProjectionBlockType.NEW_GROUND
        if type == 'b':
            return MapProjectionBlockType.BLACK_GROUND
        if type == 'h':
            return MapProjectionBlockType.HOUSE
        if type == 'c':
            return MapProjectionBlockType.CLOUD_LEFT
        if type == 'g':
            return MapProjectionBlockType.GREEN_GROUND
        if type == 'r':
            return MapProjectionBlockType.RED_GROUND
        if type == 'R':
            return MapProjectionBlockType.RED_HOUSE
        if type == 's':
            return MapProjectionBlockType.SUN
        if type == '2':
            return MapProjectionBlockType.GROUND_2
        if type == '3':
            return MapProjectionBlockType.GROUND_3
        if type == '4':
            return MapProjectionBlockType.GROUND_4
        if type == '5':
            return MapProjectionBlockType.GROUND_5
        if type == '6':
            return MapProjectionBlockType.GROUND_6
        if type == '7':
            return MapProjectionBlockType.GROUND_7
        if type == '8':
            return MapProjectionBlockType.GROUND_8
        if type == '9':
            return MapProjectionBlockType.GROUND_9
        if type == '%':
            return MapProjectionBlockType.GROUND_10
        if type == '!':
            return MapProjectionBlockType.GROUND_11
        if type == '/':
            return MapProjectionBlockType.GROUND_12
        if type == '?':
            return MapProjectionBlockType.GROUND_13
        if type == '>':
            return MapProjectionBlockType.GROUND_14
        if type == ':':
            return MapProjectionBlockType.GROUND_15
        if type == ';':
            return MapProjectionBlockType.GROUND_16
        if type == '<':
            return MapProjectionBlockType.GROUND_17
        if type == ')':
            return MapProjectionBlockType.GROUND_18
        if type == 'j':
            return MapProjectionBlockType.GROUND_19
        if type == 'O':
            return MapProjectionBlockType.GROUND_20
        if type == 'o':
            return MapProjectionBlockType.GROUND_21
        if type == 'A':
            return MapProjectionBlockType.GROUND_22
        if type == 'a':
            return MapProjectionBlockType.GROUND_23
        if type == 'J':
            return MapProjectionBlockType.GROUND_24
        if type == 'P':
            return MapProjectionBlockType.GROUND_25
        if type == 'F':
            return MapProjectionBlockType.GROUND_26
        if type == 'N':
            return MapProjectionBlockType.GROUND_27
        if type == 'B':
            return MapProjectionBlockType.GROUND_28
        if type == 'H':
            return MapProjectionBlockType.GROUND_29
        if type == 'T':
            return MapProjectionBlockType.GROUND_30
        #
        if type == 'L':
            return MapProjectionBlockType.OFLOWER
        if type == 'd':
            return MapProjectionBlockType.MAC
        if type == 'D':
            return MapProjectionBlockType.WFLOWER
        if type == 'x':
            return MapProjectionBlockType.YFLOWER
        if type == 'X':
            return MapProjectionBlockType.BFLOWER
        if type == 'z':
            return MapProjectionBlockType.PALM1
        if type == 'Z':
            return MapProjectionBlockType.PALM2
        if type == 'v':
            return MapProjectionBlockType.PLANET1
        if type == 'V':
            return MapProjectionBlockType.PLANET2
        if type == '^':
            return MapProjectionBlockType.ROSE

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
            if block.type in [MapProjectionBlockType.GROUND, MapProjectionBlockType.GROUND_2, MapProjectionBlockType.GROUND_19, MapProjectionBlockType.GROUND_20, MapProjectionBlockType.GROUND_21, MapProjectionBlockType.GROUND_22, MapProjectionBlockType.GROUND_23, MapProjectionBlockType.GROUND_24, MapProjectionBlockType.GROUND_25, MapProjectionBlockType.GROUND_26, MapProjectionBlockType.GROUND_27, MapProjectionBlockType.GROUND_28, MapProjectionBlockType.GROUND_29, MapProjectionBlockType.GROUND_30, MapProjectionBlockType.GROUND_3, MapProjectionBlockType.GROUND_4, MapProjectionBlockType.GROUND_5, MapProjectionBlockType.GROUND_6, MapProjectionBlockType.GROUND_7, MapProjectionBlockType.GROUND_8, MapProjectionBlockType.GROUND_9, MapProjectionBlockType.GROUND_10, MapProjectionBlockType.GROUND_11, MapProjectionBlockType.GROUND_12, MapProjectionBlockType.GROUND_13, MapProjectionBlockType.GROUND_14, MapProjectionBlockType.GROUND_15, MapProjectionBlockType.GROUND_16, MapProjectionBlockType.GROUND_17, MapProjectionBlockType.GROUND_18, MapProjectionBlockType.BLACK_GROUND, MapProjectionBlockType.NEW_GROUND, MapProjectionBlockType.GREEN_GROUND, MapProjectionBlockType.RED_GROUND]:
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

    # Handles the input processing
    def handle_input(self):
        pass

    # This method does post processing of the
    # entity position
    def restrict_motion(self):
        pass
    
    # Performs the character 'kill'
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
        self.restrict_motion()
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

    def restrict_motion(self):
        if self.rect.right > W:
            self.rect.right = W
        elif self.rect.left <= 0:
            self.rect.left = 0

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
        #print("jump_speed -> " + str(self.y_speed))
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
        self.level = 1 # Possible values: 1, 2, 3, 4, 5, etc.

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
            levelName = "maps/level1.map.txt"
        elif config.level == 2:
            levelName = "maps/level2.map.txt"
        elif config.level == 3:
            levelName = "maps/level3.map.txt"
        elif config.level == 4:
            levelName = "maps/level4.map.txt"
        elif config.level == 5:
            levelName = "maps/level5.map.txt"
        elif config.level == 6:
            levelName = "maps/level6.map.txt"
        elif config.level == 7:
            levelName = "maps/level7.map.txt"
        elif config.level == 8:
            levelName = "maps/level8.map.txt"
        elif config.level == 9:
            levelName = "maps/level9.map.txt"
        elif config.level == 10:
            levelName = "maps/level10.map.txt"
        elif config.level == 11:
            levelName = "maps/level11.map.txt"
        elif config.level == 12:
            levelName = "maps/level12.map.txt"
        elif config.level == 13:
            levelName = "maps/level13.map.txt"
        elif config.level == 14:
            levelName = "maps/level14.map.txt"
        elif config.level == 15:
            levelName = "maps/level15.map.txt"
        elif config.level == 16:
            levelName = "maps/level16.map.txt"
        elif config.level == 17:
            levelName = "maps/level17.map.txt"
        elif config.level == 18:
            levelName = "maps/level18.map.txt"
        elif config.level == 19:
            levelName = "maps/level19.map.txt"
        elif config.level == 20:
            levelName = "maps/level20.map.txt"
        elif config.level == 21:
            levelName = "maps/level21.map.txt"
        elif config.level == 22:
            levelName = "maps/level22.map.txt"
        elif config.level == 23:
            levelName = "maps/level23.map.txt"
        elif config.level == 24:
            levelName = "maps/level24.map.txt"
        elif config.level == 25:
            levelName = "maps/level25.map.txt"
        elif config.level == 26:
            levelName = "maps/level26.map.txt"
        elif config.level == 27:
            levelName = "maps/level27.map.txt"
        elif config.level == 28:
            levelName = "maps/level28.map.txt"
        elif config.level == 29:
            levelName = "maps/level29.map.txt"
        elif config.level == 30:
            levelName = "maps/level30.map.txt"

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
            elif bgBlock.type == MapProjectionBlockType.FLOWERS:
                backgroundElements.append(
                    StaticScaledBackground(bgBlock.rect,
                                           pygame.image.load('images/flowers.png'))
                )
            elif bgBlock.type == MapProjectionBlockType.HOUSE:
                backgroundElements.append(
                    StaticScaledBackground(bgBlock.rect,
                                           pygame.image.load('images/house.png'))
                )
            elif bgBlock.type == MapProjectionBlockType.BLACK_GROUND:
                backgroundElements.append(
                    StaticScaledBackground(bgBlock.rect,
                                           pygame.image.load('images/bground.png'))
                )

            elif bgBlock.type == MapProjectionBlockType.NEW_GROUND:
                backgroundElements.append(
                    StaticScaledBackground(bgBlock.rect,
                                           pygame.image.load('images/newground.png'))
                )
            elif bgBlock.type == MapProjectionBlockType.GREEN_GROUND:
                backgroundElements.append(
                    StaticScaledBackground(bgBlock.rect,
                                           pygame.image.load('images/greenground.png'))
                )
            elif bgBlock.type == MapProjectionBlockType.RED_GROUND:
                backgroundElements.append(
                    StaticScaledBackground(bgBlock.rect,
                                           pygame.image.load('images/redground.png'))
                )
            elif bgBlock.type == MapProjectionBlockType.GROUND_2:
                backgroundElements.append(
                    StaticScaledBackground(bgBlock.rect,
                                           pygame.image.load('images/2ground.png'))
                )
            elif bgBlock.type == MapProjectionBlockType.GROUND_3:
                backgroundElements.append(
                    StaticScaledBackground(bgBlock.rect,
                                           pygame.image.load('images/3ground.png'))
                )
            elif bgBlock.type == MapProjectionBlockType.GROUND_4:
                backgroundElements.append(
                    StaticScaledBackground(bgBlock.rect,
                                           pygame.image.load('images/4ground.png'))
                )
            elif bgBlock.type == MapProjectionBlockType.GROUND_5:
                backgroundElements.append(
                    StaticScaledBackground(bgBlock.rect,
                                           pygame.image.load('images/5ground.png'))
                )
            elif bgBlock.type == MapProjectionBlockType.GROUND_6:
                backgroundElements.append(
                    StaticScaledBackground(bgBlock.rect,
                                           pygame.image.load('images/6ground.png'))
                )
            elif bgBlock.type == MapProjectionBlockType.GROUND_7:
                backgroundElements.append(
                    StaticScaledBackground(bgBlock.rect,
                                           pygame.image.load('images/7ground.png'))
                )
            elif bgBlock.type == MapProjectionBlockType.GROUND_8:
                backgroundElements.append(
                    StaticScaledBackground(bgBlock.rect,
                                           pygame.image.load('images/8ground.png'))
                )
            elif bgBlock.type == MapProjectionBlockType.GROUND_9:
                backgroundElements.append(
                    StaticScaledBackground(bgBlock.rect,
                                           pygame.image.load('images/9ground.png'))
                )
            elif bgBlock.type == MapProjectionBlockType.GROUND_10:
                backgroundElements.append(
                    StaticScaledBackground(bgBlock.rect,
                                           pygame.image.load('images/10ground.png'))
                )
            elif bgBlock.type == MapProjectionBlockType.GROUND_11:
                backgroundElements.append(
                    StaticScaledBackground(bgBlock.rect,
                                           pygame.image.load('images/11ground.png'))
                )
            elif bgBlock.type == MapProjectionBlockType.GROUND_12:
                backgroundElements.append(
                    StaticScaledBackground(bgBlock.rect,
                                           pygame.image.load('images/12ground.png'))
                )
            elif bgBlock.type == MapProjectionBlockType.GROUND_13:
                backgroundElements.append(
                    StaticScaledBackground(bgBlock.rect,
                                           pygame.image.load('images/13ground.png'))
                )
            elif bgBlock.type == MapProjectionBlockType.GROUND_14:
                backgroundElements.append(
                    StaticScaledBackground(bgBlock.rect,
                                           pygame.image.load('images/14ground.png'))
                )
            elif bgBlock.type == MapProjectionBlockType.GROUND_15:
                backgroundElements.append(
                    StaticScaledBackground(bgBlock.rect,
                                           pygame.image.load('images/15ground.png'))
                )
            elif bgBlock.type == MapProjectionBlockType.GROUND_16:
                backgroundElements.append(
                    StaticScaledBackground(bgBlock.rect,
                                           pygame.image.load('images/16ground.png'))
                )
            elif bgBlock.type == MapProjectionBlockType.GROUND_17:
                backgroundElements.append(
                    StaticScaledBackground(bgBlock.rect,
                                           pygame.image.load('images/17ground.png'))
                )
            elif bgBlock.type == MapProjectionBlockType.GROUND_18:
                backgroundElements.append(
                    StaticScaledBackground(bgBlock.rect,
                                           pygame.image.load('images/18ground.png'))
                )
            
            elif bgBlock.type == MapProjectionBlockType.RED_HOUSE:
                backgroundElements.append(
                    StaticScaledBackground(bgBlock.rect,
                                           pygame.image.load('images/redhouse.png'))
                )
            elif bgBlock.type == MapProjectionBlockType.SUN:
                backgroundElements.append(
                    StaticScaledBackground(bgBlock.rect,
                                           pygame.image.load('images/sun.png'))
                )
            elif bgBlock.type == MapProjectionBlockType.GROUND:
                backgroundElements.append(
                   StaticScaledBackground(bgBlock.rect,
                                          pygame.image.load('images/ground.png'))
                )
            #
            elif bgBlock.type == MapProjectionBlockType.PALM1:
                backgroundElements.append(
                   StaticScaledBackground(bgBlock.rect,
                                          pygame.image.load('images/palm1.png'))
                )
            elif bgBlock.type == MapProjectionBlockType.PALM2:
                backgroundElements.append(
                   StaticScaledBackground(bgBlock.rect,
                                          pygame.image.load('images/palm2.png'))
                )
            elif bgBlock.type == MapProjectionBlockType.PLANET1:
                backgroundElements.append(
                   StaticScaledBackground(bgBlock.rect,
                                          pygame.image.load('images/planet1.png'))
                )
            elif bgBlock.type == MapProjectionBlockType.PLANET2:
                backgroundElements.append(
                   StaticScaledBackground(bgBlock.rect,
                                          pygame.image.load('images/planet2.png'))
                )
            elif bgBlock.type == MapProjectionBlockType.ROSE:
                backgroundElements.append(
                   StaticScaledBackground(bgBlock.rect,
                                          pygame.image.load('images/rose.png'))
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
                                                350)
                backgroundElements.append(cloudsLeft)
            elif bgBlock.type == MapProjectionBlockType.CLOUD_RIGHT:
                cloudsRight = AnimatedBackground(bgBlock.rect,
                                                 [pygame.image.load('images/2Clouds.png'),
                                                  pygame.image.load('images/3Clouds.png'),
                                                  pygame.image.load('images/1Clouds.png')],
                                                 350)
                backgroundElements.append(cloudsRight)
            elif bgBlock.type == MapProjectionBlockType.NLO:
                NLO = AnimatedBackground(bgBlock.rect,
                                                 [pygame.image.load('images/nlo1.png'),
                                                  pygame.image.load('images/nlo2.png')],
                                                 350)
                backgroundElements.append(NLO)
            elif bgBlock.type == MapProjectionBlockType.GROUND_19:
                backgroundElements.append(
                    StaticScaledBackground(bgBlock.rect,
                                           pygame.image.load('images/19ground.png'))
                    )
            elif bgBlock.type == MapProjectionBlockType.GROUND_20:
                backgroundElements.append(
                    StaticScaledBackground(bgBlock.rect,
                                           pygame.image.load('images/20ground.png'))
                    )
            elif bgBlock.type == MapProjectionBlockType.GROUND_21:
                backgroundElements.append(
                    StaticScaledBackground(bgBlock.rect,
                                           pygame.image.load('images/21ground.png'))
                    )
            elif bgBlock.type == MapProjectionBlockType.GROUND_22:
                backgroundElements.append(
                    StaticScaledBackground(bgBlock.rect,
                                           pygame.image.load('images/22ground.png'))
                    )
            elif bgBlock.type == MapProjectionBlockType.GROUND_23:
                backgroundElements.append(
                    StaticScaledBackground(bgBlock.rect,
                                           pygame.image.load('images/23ground.png'))
                    )
            elif bgBlock.type == MapProjectionBlockType.GROUND_24:
                backgroundElements.append(
                    StaticScaledBackground(bgBlock.rect,
                                           pygame.image.load('images/24ground.png'))
                    )
            elif bgBlock.type == MapProjectionBlockType.GROUND_25:
                backgroundElements.append(
                    StaticScaledBackground(bgBlock.rect,
                                           pygame.image.load('images/25ground.png'))
                    )
            elif bgBlock.type == MapProjectionBlockType.GROUND_26:
                backgroundElements.append(
                    StaticScaledBackground(bgBlock.rect,
                                           pygame.image.load('images/26ground.png'))
                    )
            elif bgBlock.type == MapProjectionBlockType.GROUND_27:
                backgroundElements.append(
                    StaticScaledBackground(bgBlock.rect,
                                           pygame.image.load('images/27ground.png'))
                    )
            elif bgBlock.type == MapProjectionBlockType.GROUND_28:
                backgroundElements.append(
                    StaticScaledBackground(bgBlock.rect,
                                           pygame.image.load('images/28ground.png'))
                    )

            elif bgBlock.type == MapProjectionBlockType.GROUND_29:
                backgroundElements.append(
                    StaticScaledBackground(bgBlock.rect,
                                           pygame.image.load('images/29ground.png'))
                    )
            elif bgBlock.type == MapProjectionBlockType.GROUND_30:
                backgroundElements.append(
                    StaticScaledBackground(bgBlock.rect,
                                           pygame.image.load('images/30ground.png'))
                    )
            #
            elif bgBlock.type == MapProjectionBlockType.OFLOWER:
                OFLOWER = AnimatedBackground(bgBlock.rect,
                                                 [pygame.image.load('images/oflower1.png'),
                                                  pygame.image.load('images/oflower2.png'),
                                                  pygame.image.load('images/oflower3.png')],
                                                 350)
                backgroundElements.append(OFLOWER)
            elif bgBlock.type == MapProjectionBlockType.WFLOWER:
                WFLOWER = AnimatedBackground(bgBlock.rect,
                                                 [pygame.image.load('images/wflower1.png'),
                                                  pygame.image.load('images/wflower2.png'),
                                                  pygame.image.load('images/wflower3.png')],
                                                 350)
                backgroundElements.append(WFLOWER)
            elif bgBlock.type == MapProjectionBlockType.YFLOWER:
                YFLOWER = AnimatedBackground(bgBlock.rect,
                                                 [pygame.image.load('images/yflower1.png'),
                                                  pygame.image.load('images/yflower2.png'),
                                                  pygame.image.load('images/yflower3.png')],
                                                 350)
                backgroundElements.append(YFLOWER)
            elif bgBlock.type == MapProjectionBlockType.BFLOWER:
                BFLOWER = AnimatedBackground(bgBlock.rect,
                                                 [pygame.image.load('images/bflower1.png'),
                                                  pygame.image.load('images/bflower2.png'),
                                                  pygame.image.load('images/bflower3.png')],
                                                 350)
                backgroundElements.append(BFLOWER)
            elif bgBlock.type == MapProjectionBlockType.MAC:
                MAC = AnimatedBackground(bgBlock.rect,
                                                 [pygame.image.load('images/mac1.png'),
                                                  pygame.image.load('images/mac2.png'),
                                                  pygame.image.load('images/mac3.png')],
                                                 350)
                backgroundElements.append(MAC)
            
            
            
            

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
    LEVEL_LEVELS = 4


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
        self.more_img = pygame.image.load('images/button_more.png').convert_alpha()
        self.girl_img = pygame.image.load('images/Girl.png').convert_alpha()
        self.boy_img = pygame.image.load('images/Boy.png').convert_alpha()
        #new characters
        self.minion_img = pygame.image.load('images/minion.png').convert_alpha()
        self.shrek_img = pygame.image.load('images/shrek.png').convert_alpha()
        self.bob_img = pygame.image.load('images/bob.png').convert_alpha()
        self.puh_img = pygame.image.load('images/puh.png').convert_alpha()
        self.spider_img = pygame.image.load('images/spider.png').convert_alpha()
        self.egg_img = pygame.image.load('images/egg.png').convert_alpha()
        self.ninja_img = pygame.image.load('images/ninja.png').convert_alpha()
        self.astro_img = pygame.image.load('images/astro.png').convert_alpha()
        #self.spider_img = pygame.image.load('images/spider.png').convert_alpha()
        #self.spider_img = pygame.image.load('images/spider.png').convert_alpha()
        #self.spider_img = pygame.image.load('images/spider.png').convert_alpha()
        #self.spider_img = pygame.image.load('images/spider.png').convert_alpha()
        #self.spider_img = pygame.image.load('images/spider.png').convert_alpha()

        
        self.game_level_1 = pygame.image.load('images/Level1_button.png').convert_alpha()
        self.game_level_2 = pygame.image.load('images/Level2_button.png').convert_alpha()
        self.game_level_3 = pygame.image.load('images/Level3_button.png').convert_alpha()
        self.game_level_4 = pygame.image.load('images/Level4_button.png').convert_alpha()
        self.game_level_5 = pygame.image.load('images/Level5_button.png').convert_alpha()
        self.game_level_6 = pygame.image.load('images/Level6_button.png').convert_alpha()
        self.game_level_7 = pygame.image.load('images/Level7_button.png').convert_alpha()
        self.game_level_8 = pygame.image.load('images/Level8_button.png').convert_alpha()
        self.game_level_9 = pygame.image.load('images/Level9_button.png').convert_alpha()
        self.game_level_10 = pygame.image.load('images/Level10_button.png').convert_alpha()
        self.game_level_11 = pygame.image.load('images/Level11_button.png').convert_alpha()
        self.game_level_12 = pygame.image.load('images/Level12_button.png').convert_alpha()
        self.game_level_13 = pygame.image.load('images/Level13_button.png').convert_alpha()
        self.game_level_14 = pygame.image.load('images/Level14_button.png').convert_alpha()
        self.game_level_15 = pygame.image.load('images/Level15_button.png').convert_alpha()
        self.game_level_16 = pygame.image.load('images/Level16_button.png').convert_alpha()
        self.game_level_17 = pygame.image.load('images/Level17_button.png').convert_alpha()
        self.game_level_18 = pygame.image.load('images/Level18_button.png').convert_alpha()
        self.game_level_19 = pygame.image.load('images/Level19_button.png').convert_alpha()
        self.game_level_20 = pygame.image.load('images/Level20_button.png').convert_alpha()
        self.game_level_21 = pygame.image.load('images/Level21_button.png').convert_alpha()
        self.game_level_22 = pygame.image.load('images/Level22_button.png').convert_alpha()
        self.game_level_23 = pygame.image.load('images/Level23_button.png').convert_alpha()
        self.game_level_24 = pygame.image.load('images/Level24_button.png').convert_alpha()
        self.game_level_25 = pygame.image.load('images/Level25_button.png').convert_alpha()
        self.game_level_26 = pygame.image.load('images/Level26_button.png').convert_alpha()
        self.game_level_27 = pygame.image.load('images/Level27_button.png').convert_alpha()
        self.game_level_28 = pygame.image.load('images/Level28_button.png').convert_alpha()
        self.game_level_29 = pygame.image.load('images/Level29_button.png').convert_alpha()
        self.game_level_30 = pygame.image.load('images/Level30_button.png').convert_alpha()
       
        #selected level button
        self.selectedgame_level_1 = pygame.image.load('images/Level1selected_button.png').convert_alpha()
        self.selectedgame_level_2 = pygame.image.load('images/Level2selected_button.png').convert_alpha()
        self.selectedgame_level_3 = pygame.image.load('images/Level3selected_button.png').convert_alpha()
        self.selectedgame_level_4 = pygame.image.load('images/Level4selected_button.png').convert_alpha()
        self.selectedgame_level_5 = pygame.image.load('images/Level5selected_button.png').convert_alpha()
        self.selectedgame_level_6 = pygame.image.load('images/Level6selected_button.png').convert_alpha()
        self.selectedgame_level_7 = pygame.image.load('images/Level7selected_button.png').convert_alpha()
        self.selectedgame_level_8 = pygame.image.load('images/Level8selected_button.png').convert_alpha()
        self.selectedgame_level_9 = pygame.image.load('images/Level9selected_button.png').convert_alpha()
        self.selectedgame_level_10 = pygame.image.load('images/Level10selected_button.png').convert_alpha()
        self.selectedgame_level_11 = pygame.image.load('images/Level11selected_button.png').convert_alpha()
        self.selectedgame_level_12 = pygame.image.load('images/Level12selected_button.png').convert_alpha()
        self.selectedgame_level_13 = pygame.image.load('images/Level13selected_button.png').convert_alpha()
        self.selectedgame_level_14 = pygame.image.load('images/Level14selected_button.png').convert_alpha()
        self.selectedgame_level_15 = pygame.image.load('images/Level15selected_button.png').convert_alpha()
        self.selectedgame_level_16 = pygame.image.load('images/Level16selected_button.png').convert_alpha()
        self.selectedgame_level_17 = pygame.image.load('images/Level17selected_button.png').convert_alpha()
        self.selectedgame_level_18 = pygame.image.load('images/Level18selected_button.png').convert_alpha()
        self.selectedgame_level_19 = pygame.image.load('images/Level19selected_button.png').convert_alpha()
        self.selectedgame_level_20 = pygame.image.load('images/Level20selected_button.png').convert_alpha()
        self.selectedgame_level_21 = pygame.image.load('images/Level21selected_button.png').convert_alpha()
        self.selectedgame_level_22 = pygame.image.load('images/Level22selected_button.png').convert_alpha()
        self.selectedgame_level_23 = pygame.image.load('images/Level23selected_button.png').convert_alpha()
        self.selectedgame_level_24 = pygame.image.load('images/Level24selected_button.png').convert_alpha()
        self.selectedgame_level_25 = pygame.image.load('images/Level25selected_button.png').convert_alpha()
        self.selectedgame_level_26 = pygame.image.load('images/Level26selected_button.png').convert_alpha()
        self.selectedgame_level_27 = pygame.image.load('images/Level27selected_button.png').convert_alpha()
        self.selectedgame_level_28 = pygame.image.load('images/Level28selected_button.png').convert_alpha()
        self.selectedgame_level_29 = pygame.image.load('images/Level29selected_button.png').convert_alpha()
        self.selectedgame_level_30 = pygame.image.load('images/Level30selected_button.png').convert_alpha()

        self.boyselected = pygame.image.load('images/boyselected.png').convert_alpha()
        self.girlselected = pygame.image.load('images/girlselected.png').convert_alpha()
        #new characters selected button 
        self.minionselected = pygame.image.load('images/minionselected.png').convert_alpha()

        self.shrekselected = pygame.image.load('images/shrekselected.png').convert_alpha()

        self.bobselected = pygame.image.load('images/bobselected.png').convert_alpha()

        self.puhselected = pygame.image.load('images/puhselected.png').convert_alpha()

        self.spiderselected = pygame.image.load('images/spiderselected.png').convert_alpha()

        self.eggselected = pygame.image.load('images/eggselected.png').convert_alpha()

        self.ninjaselected = pygame.image.load('images/ninjaselected.png').convert_alpha()

        self.astroselected = pygame.image.load('images/astroselected.png').convert_alpha()

         #self.puhselected = pygame.image.load('images/puhselected.png').convert_alpha()

         #self.puhselected = pygame.image.load('images/puhselected.png').convert_alpha()

         #self.puhselected = pygame.image.load('images/puhselected.png').convert_alpha()

         #self.puhselected = pygame.image.load('images/puhselected.png').convert_alpha()

         #self.puhselected = pygame.image.load('images/puhselected.png').convert_alpha()
        

        self.bg_l_1 = Menu.blurImage('images/bg_l_1.png')
        self.bg_l_2 = Menu.blurImage('images/bg_l_2.png')
        self.bg_l_3 = Menu.blurImage('images/bg_l_3.png')
        self.bg_l_4 = Menu.blurImage('images/bg_l_4.png')
        self.bg_l_5 = Menu.blurImage('images/bg_l_5.png')
        #
        self.bg_l_6 = Menu.blurImage('images/bg_l_6.png')
        self.bg_l_7 = Menu.blurImage('images/bg_l_7.png')
        self.bg_l_8 = Menu.blurImage('images/bg_l_8.png')
        self.bg_l_9 = Menu.blurImage('images/bg_l_9.png')
        self.bg_l_10 = Menu.blurImage('images/bg_l_10.png')
        self.bg_l_11 = Menu.blurImage('images/bg_l_11.png')
        self.bg_l_12 = Menu.blurImage('images/bg_l_12.png')
        self.bg_l_13 = Menu.blurImage('images/bg_l_13.png')
        self.bg_l_14 = Menu.blurImage('images/bg_l_14.png')
        self.bg_l_15 = Menu.blurImage('images/bg_l_15.png')
        self.bg_l_16 = Menu.blurImage('images/bg_l_16.png')
        self.bg_l_17 = Menu.blurImage('images/bg_l_17.png')
        self.bg_l_18 = Menu.blurImage('images/bg_l_18.png')
        self.bg_l_19 = Menu.blurImage('images/bg_l_19.png')
        self.bg_l_20 = Menu.blurImage('images/bg_l_20.png')
        self.bg_l_21 = Menu.blurImage('images/bg_l_21.png')
        self.bg_l_22 = Menu.blurImage('images/bg_l_22.png')
        self.bg_l_23 = Menu.blurImage('images/bg_l_23.png')
        self.bg_l_24 = Menu.blurImage('images/bg_l_24.png')
        self.bg_l_25 = Menu.blurImage('images/bg_l_25.png')
        self.bg_l_26 = Menu.blurImage('images/bg_l_26.png')
        self.bg_l_27 = Menu.blurImage('images/bg_l_27.png')
        self.bg_l_28 = Menu.blurImage('images/bg_l_28.png')
        self.bg_l_29 = Menu.blurImage('images/bg_l_29.png')
        self.bg_l_30 = Menu.blurImage('images/bg_l_30.png')
        self.current_bg = self.bg_l_1



        self.play_button = button.Button(336, 125, self.play_img, 1)
        self.options_button = button.Button(297, 250, self.options_img, 1)
        self.quit_button = button.Button(336, 375, self.quit_img, 1)
        self.char_button = button.Button(226, 75, self.char_img, 1)
        self.level_button = button.Button(225, 200, self.level_img, 1)
        self.keys_button = button.Button(246, 325, self.keys_img, 1)
        self.back_button = button.Button(332, 450, self.back_img, 1)
        self.more_button = button.Button(500, 450, self.more_img, 1)
        #characters
        self.boy_button = button.Button(180, 50, self.boy_img, 2)
        self.boyselected_button = button.Button(180, 50, self.boyselected, 2)

        self.girl_button = button.Button(328, 50, self.girl_img, 2)
        self.girlselected_button = button.Button(328, 50, self.girlselected, 2)
        
        #new characters
        self.minion_button = button.Button(32, 50, self.minion_img, 1.5)
        self.minionselected_button = button.Button(32, 50, self.minionselected, 1.5)
        #new
        self.shrek_button = button.Button(476, 50, self.shrek_img, 1.5)
        self.shrekselected_button = button.Button(476, 50, self.shrekselected, 1.5)
        #new
        self.bob_button = button.Button(634, 50, self.bob_img, 1)
        self.bobselected_button = button.Button(634, 50, self.bobselected, 1)
        #new
        self.puh_button = button.Button(32, 200, self.puh_img, 2)
        self.puhselected_button = button.Button(32, 200, self.puhselected, 2)

        #new
        self.spider_button = button.Button(180, 200, self.spider_img, 2)
        self.spiderselected_button = button.Button(180, 200, self.spiderselected, 2)

        #new
        self.egg_button = button.Button(328, 200, self.egg_img, 2)
        self.eggselected_button = button.Button(328, 200, self.eggselected, 2)

        #new
        self.ninja_button = button.Button(476, 200, self.ninja_img, 2)
        self.ninjaselected_button = button.Button(476, 200, self.ninjaselected, 2)

        #new
        self.astro_button = button.Button(634, 200, self.astro_img, 1.5)
        self.astroselected_button = button.Button(634, 200, self.astroselected, 1.5)

        #new
        #self.shrek_button = button.Button(450, 100, self.shrek_img, 2.5)
        #self.shrekselected_button = button.Button(450, 100, self.shrekselected, 2.5)

        #new
        #self.shrek_button = button.Button(450, 100, self.shrek_img, 2.5)
        #self.shrekselected_button = button.Button(450, 100, self.shrekselected, 2.5)

        #new
        #self.shrek_button = button.Button(450, 100, self.shrek_img, 2.5)
        #self.shrekselected_button = button.Button(450, 100, self.shrekselected, 2.5)

        #new
        #self.shrek_button = button.Button(450, 100, self.shrek_img, 2.5)
        #self.shrekselected_button = button.Button(450, 100, self.shrekselected, 2.5)

        #new
        #self.shrek_button = button.Button(450, 100, self.shrek_img, 2.5)
        #self.shrekselected_button = button.Button(450, 100, self.shrekselected, 2.5)

        #new
        #self.shrek_button = button.Button(450, 100, self.shrek_img, 2.5)
        #self.shrekselected_button = button.Button(450, 100, self.shrekselected, 2.5)

        #new
        #self.shrek_button = button.Button(450, 100, self.shrek_img, 2.5)
        #self.shrekselected_button = button.Button(450, 100, self.shrekselected, 2.5)

        #new
        #self.shrek_button = button.Button(450, 100, self.shrek_img, 2.5)
        #self.shrekselected_button = button.Button(450, 100, self.shrekselected, 2.5)

    
        # levels button
        self.game_level_button_1 = button.Button(1, 20, self.game_level_1, 1)
        self.game_level_button_2 = button.Button(1, 100, self.game_level_2, 1)
        self.game_level_button_3 = button.Button(1, 180, self.game_level_3, 1)
        self.game_level_button_4 = button.Button(1, 260, self.game_level_4, 1)
        self.game_level_button_5 = button.Button(1, 340, self.game_level_5, 1)
        self.game_level_button_6 = button.Button(230, 20, self.game_level_6, 1)
        self.game_level_button_7 = button.Button(230, 100, self.game_level_7, 1)
        self.game_level_button_8 = button.Button(230, 180, self.game_level_8, 1)
        self.game_level_button_9 = button.Button(230, 260, self.game_level_9, 1)
        self.game_level_button_10 = button.Button(230, 340, self.game_level_10, 1)
        self.game_level_button_11 = button.Button(500, 20, self.game_level_11, 1)
        self.game_level_button_12 = button.Button(500, 100, self.game_level_12, 1)
        self.game_level_button_13 = button.Button(500, 180, self.game_level_13, 1)
        self.game_level_button_14 = button.Button(500, 260, self.game_level_14, 1)
        self.game_level_button_15 = button.Button(500, 340, self.game_level_15, 1)
        self.game_level_button_16 = button.Button(1, 20, self.game_level_16, 1)
        self.game_level_button_17 = button.Button(1, 100, self.game_level_17, 1)
        self.game_level_button_18 = button.Button(1, 180, self.game_level_18, 1)
        self.game_level_button_19 = button.Button(1, 260, self.game_level_19, 1)
        self.game_level_button_20 = button.Button(1, 340, self.game_level_20, 1)
        self.game_level_button_21 = button.Button(230, 20, self.game_level_21, 1)
        self.game_level_button_22 = button.Button(230, 100, self.game_level_22, 1)
        self.game_level_button_23 = button.Button(230, 180, self.game_level_23, 1)
        self.game_level_button_24 = button.Button(230, 260, self.game_level_24, 1)
        self.game_level_button_25 = button.Button(230, 340, self.game_level_25, 1)
        self.game_level_button_26 = button.Button(500, 20, self.game_level_26, 1)
        self.game_level_button_27 = button.Button(500, 100, self.game_level_27, 1)
        self.game_level_button_28 = button.Button(500, 180, self.game_level_28, 1)
        self.game_level_button_29 = button.Button(500, 260, self.game_level_29, 1)
        self.game_level_button_30 = button.Button(500, 340, self.game_level_30, 1)

        #levels selected
        self.selectedgame_level_1_button = button.Button(1, 20, self.selectedgame_level_1, 1)
        self.selectedgame_level_2_button = button.Button(1, 100, self.selectedgame_level_2, 1)
        self.selectedgame_level_3_button = button.Button(1, 180, self.selectedgame_level_3, 1)
        self.selectedgame_level_4_button = button.Button(1, 260, self.selectedgame_level_4, 1)
        self.selectedgame_level_5_button = button.Button(1, 340, self.selectedgame_level_5, 1)
        self.selectedgame_level_6_button = button.Button(230, 20, self.selectedgame_level_6, 1)
        self.selectedgame_level_7_button = button.Button(230, 100, self.selectedgame_level_7, 1)
        self.selectedgame_level_8_button = button.Button(230, 180, self.selectedgame_level_8, 1)
        self.selectedgame_level_9_button = button.Button(230, 260, self.selectedgame_level_9, 1)
        self.selectedgame_level_10_button = button.Button(230, 340, self.selectedgame_level_10, 1)
        self.selectedgame_level_11_button = button.Button(500, 20, self.selectedgame_level_11, 1)
        self.selectedgame_level_12_button = button.Button(500, 100, self.selectedgame_level_12, 1)
        self.selectedgame_level_13_button = button.Button(500, 180, self.selectedgame_level_13, 1)
        self.selectedgame_level_14_button = button.Button(500, 260, self.selectedgame_level_14, 1)
        self.selectedgame_level_15_button = button.Button(500, 340, self.selectedgame_level_15, 1)
        self.selectedgame_level_16_button = button.Button(1, 20, self.selectedgame_level_16, 1)
        self.selectedgame_level_17_button = button.Button(1, 100, self.selectedgame_level_17, 1)
        self.selectedgame_level_18_button = button.Button(1, 180, self.selectedgame_level_18, 1)
        self.selectedgame_level_19_button = button.Button(1, 260, self.selectedgame_level_19, 1)
        self.selectedgame_level_20_button = button.Button(1, 340, self.selectedgame_level_20, 1)
        self.selectedgame_level_21_button = button.Button(230, 20, self.selectedgame_level_21, 1)
        self.selectedgame_level_22_button = button.Button(230, 100, self.selectedgame_level_22, 1)
        self.selectedgame_level_23_button = button.Button(230, 180, self.selectedgame_level_23, 1)
        self.selectedgame_level_24_button = button.Button(230, 260, self.selectedgame_level_24, 1)
        self.selectedgame_level_25_button = button.Button(230, 340, self.selectedgame_level_25, 1)
        self.selectedgame_level_26_button = button.Button(500, 20, self.selectedgame_level_26, 1)
        self.selectedgame_level_27_button = button.Button(500, 100, self.selectedgame_level_27, 1)
        self.selectedgame_level_28_button = button.Button(500, 180, self.selectedgame_level_28, 1)
        self.selectedgame_level_29_button = button.Button(500, 260, self.selectedgame_level_29, 1)
        self.selectedgame_level_30_button = button.Button(500, 340, self.selectedgame_level_30, 1)
        


    # This method load image and does some image blurring
    def blurImage(path: str) -> pygame.Surface:
        surface: pygame.Surface = pygame.image.load(path).convert_alpha()
        scale:float = 1.0 / float(3)
        surf_size: tuple[int, int] = surface.get_size()
        scale_size: tuple[int, int] = (int(surf_size[0]*scale), int(surf_size[1]*scale))
        surf: pygame.Surface = pygame.transform.smoothscale(surface, scale_size)
        surf = pygame.transform.smoothscale(surf, surf_size)
        return surf

    def process(self, screen : pygame.Surface):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.running = False


        screen.blit(self.current_bg, (0,0))
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
                #BOY_LEVEL
            if self.config.player == 'Boy':
                self.boyselected_button.draw(screen)
            if self.girl_button.draw(screen):
                self.config.player = 'Girl'
                print("CHAR -> " + str(self.config.player))
                #GIRL_LEVEL
            if self.config.player == 'Girl':
                self.girlselected_button.draw(screen)
            if self.back_button.draw(screen):
                self.level = self.LEVEL_ROOT
                #MINION_LEVEL
            if self.minion_button.draw(screen):
                self.config.player = 'Minion'
                print("CHAR -> " + str(self.config.player))
            if self.config.player == 'Minion':
                self.minionselected_button.draw(screen)
            if self.back_button.draw(screen):
                self.level = self.LEVEL_ROOT
                #SHREK LEVEL
            if self.shrek_button.draw(screen):
                self.config.player = 'Shrek'
                print("CHAR -> " + str(self.config.player))
            if self.config.player == 'Shrek':
                self.shrekselected_button.draw(screen)
            if self.back_button.draw(screen):
                self.level = self.LEVEL_ROOT
                #BOB LEVEL
            if self.bob_button.draw(screen):
                self.config.player = 'bob'
                print("CHAR -> " + str(self.config.player))
            if self.config.player == 'bob':
                self.bobselected_button.draw(screen)
            if self.back_button.draw(screen):
                self.level = self.LEVEL_ROOT
                #PUH LEVEL
            if self.puh_button.draw(screen):
                self.config.player = 'puh'
                print("CHAR -> " + str(self.config.player))
            if self.config.player == 'puh':
                self.puhselected_button.draw(screen)
            if self.back_button.draw(screen):
                self.level = self.LEVEL_ROOT
                #SPIDER LEVEL
            if self.spider_button.draw(screen):
                self.config.player = 'Spider'
                print("CHAR -> " + str(self.config.player))
            if self.config.player == 'Spider':
                self.spiderselected_button.draw(screen)
            if self.back_button.draw(screen):
                self.level = self.LEVEL_ROOT
                #EGG LEVEL 
            if self.egg_button.draw(screen):
                self.config.player = 'Egg'
                print("CHAR -> " + str(self.config.player))
            if self.config.player == 'Egg':
                self.eggselected_button.draw(screen)
            if self.back_button.draw(screen):
                self.level = self.LEVEL_ROOT
                #NINJA LEVEL
            if self.ninja_button.draw(screen):
                self.config.player = 'Ninja'
                print("CHAR -> " + str(self.config.player))
            if self.config.player == 'Ninja':
                self.ninjaselected_button.draw(screen)
            if self.back_button.draw(screen):
                self.level = self.LEVEL_ROOT
                #ASTRO LEVEL
            if self.astro_button.draw(screen):
                self.config.player = 'Astro'
                print("CHAR -> " + str(self.config.player))
            if self.config.player == 'Astro':
                self.astroselected_button.draw(screen)
            if self.back_button.draw(screen):
                self.level = self.LEVEL_ROOT
                #N CH LEVEL
            if self.minion_button.draw(screen):
                self.config.player = 'Minion'
                print("CHAR -> " + str(self.config.player))
            if self.config.player == 'Minion':
                self.minionselected_button.draw(screen)
            if self.back_button.draw(screen):
                self.level = self.LEVEL_ROOT
                #N CH LEVEL
            if self.minion_button.draw(screen):
                self.config.player = 'Minion'
                print("CHAR -> " + str(self.config.player))
            if self.config.player == 'Minion':
                self.minionselected_button.draw(screen)
            if self.back_button.draw(screen):
                self.level = self.LEVEL_ROOT
                #N CH LEVEL
            if self.minion_button.draw(screen):
                self.config.player = 'Minion'
                print("CHAR -> " + str(self.config.player))
            if self.config.player == 'Minion':
                self.minionselected_button.draw(screen)
            if self.back_button.draw(screen):
                self.level = self.LEVEL_ROOT
        elif self.level == self.LEVEL_LEVEL:
            if self.back_button.draw(screen):
                self.level = self.LEVEL_ROOT
                #level1
            if self.game_level_button_1.draw(screen):
                self.config.level = 1
                self.current_bg = self.bg_l_1
                #print("Level -> " + str(self.config.level))
            if self.config.level == 1:
                self.selectedgame_level_1_button.draw(screen)
                #level2
            if self.game_level_button_2.draw(screen):
                self.config.level = 2
                self.current_bg = self.bg_l_2
            if self.config.level == 2:
                self.selectedgame_level_2_button.draw(screen)
                #level3
            if self.game_level_button_3.draw(screen):
                self.config.level = 3
                self.current_bg = self.bg_l_3
            if self.config.level == 3:
                self.selectedgame_level_3_button.draw(screen)
                #level4
            if self.game_level_button_4.draw(screen):
                self.config.level = 4
                self.current_bg = self.bg_l_4
            if self.config.level == 4:
                self.selectedgame_level_4_button.draw(screen)
                #level5
            if self.game_level_button_5.draw(screen):
                self.config.level = 5
                self.current_bg = self.bg_l_5
            if self.config.level == 5:
                self.selectedgame_level_5_button.draw(screen)
                #6
            if self.game_level_button_6.draw(screen):
                self.config.level = 6
                self.current_bg = self.bg_l_6
            if self.config.level == 6:
                self.selectedgame_level_6_button.draw(screen)
                #7
            if self.game_level_button_7.draw(screen):
                self.config.level = 7
                self.current_bg = self.bg_l_7
            if self.config.level == 7:
                self.selectedgame_level_7_button.draw(screen)
                #8
            if self.game_level_button_8.draw(screen):
                self.config.level = 8
                self.current_bg = self.bg_l_8
            if self.config.level == 8:
                self.selectedgame_level_8_button.draw(screen)
                #9
            if self.game_level_button_9.draw(screen):
                self.config.level = 9
                self.current_bg = self.bg_l_9
            if self.config.level == 9:
                self.selectedgame_level_9_button.draw(screen)
                #10
            if self.game_level_button_10.draw(screen):
                self.config.level = 10
                self.current_bg = self.bg_l_10
            if self.config.level == 10:
                self.selectedgame_level_10_button.draw(screen)
                #11
            if self.game_level_button_11.draw(screen):
                self.config.level = 11
                self.current_bg = self.bg_l_11
            if self.config.level == 11:
                self.selectedgame_level_11_button.draw(screen)
                #12
            if self.game_level_button_12.draw(screen):
                self.config.level = 12
                self.current_bg = self.bg_l_12
            if self.config.level == 12:
                self.selectedgame_level_12_button.draw(screen)
                #13
            if self.game_level_button_13.draw(screen):
                self.config.level = 13
                self.current_bg = self.bg_l_13
            if self.config.level == 13:
                self.selectedgame_level_13_button.draw(screen)
                #14
            if self.game_level_button_14.draw(screen):
                self.config.level = 14
                self.current_bg = self.bg_l_14
            if self.config.level == 14:
                self.selectedgame_level_14_button.draw(screen)
                #15
            if self.game_level_button_15.draw(screen):
                self.config.level = 15
                self.current_bg = self.bg_l_15
            if self.config.level == 15:
                self.selectedgame_level_15_button.draw(screen)
                #more levels
            if self.more_button.draw(screen):
                self.level = self.LEVEL_LEVELS
        elif self.level == self.LEVEL_LEVELS:
            if self.game_level_button_16.draw(screen):
                self.config.level = 16
                self.current_bg = self.bg_l_16
            if self.config.level == 16:
                self.selectedgame_level_16_button.draw(screen)
                #17
            if self.game_level_button_17.draw(screen):
                self.config.level = 17
                self.current_bg = self.bg_l_17
            if self.config.level == 17:
                self.selectedgame_level_17_button.draw(screen)
                #18
            if self.game_level_button_18.draw(screen):
                self.config.level = 18
                self.current_bg = self.bg_l_18
            if self.config.level == 18:
                self.selectedgame_level_18_button.draw(screen)
                #19
            if self.game_level_button_19.draw(screen):
                self.config.level = 19
                self.current_bg = self.bg_l_19
            if self.config.level == 19:
                self.selectedgame_level_19_button.draw(screen)
                #20
            if self.game_level_button_20.draw(screen):
                self.config.level = 20
                self.current_bg = self.bg_l_20
            if self.config.level == 20:
                self.selectedgame_level_20_button.draw(screen)
                #21
            if self.game_level_button_21.draw(screen):
                self.config.level = 21
                self.current_bg = self.bg_l_21
            if self.config.level == 21:
                self.selectedgame_level_21_button.draw(screen)
                #22
            if self.game_level_button_22.draw(screen):
                self.config.level = 22
                self.current_bg = self.bg_l_22
            if self.config.level == 22:
                self.selectedgame_level_22_button.draw(screen)
                #23
            if self.game_level_button_23.draw(screen):
                self.config.level = 23
                self.current_bg = self.bg_l_23
            if self.config.level == 23:
                self.selectedgame_level_23_button.draw(screen)
                #24
            if self.game_level_button_24.draw(screen):
                self.config.level = 24
                self.current_bg = self.bg_l_24
            if self.config.level == 24:
                self.selectedgame_level_24_button.draw(screen)
                #25
            if self.game_level_button_25.draw(screen):
                self.config.level = 25
                self.current_bg = self.bg_l_25
            if self.config.level == 25:
                self.selectedgame_level_25_button.draw(screen)
                #26
            if self.game_level_button_26.draw(screen):
                self.config.level = 26
                self.current_bg = self.bg_l_26
            if self.config.level == 26:
                self.selectedgame_level_26_button.draw(screen)
                #27
            if self.game_level_button_27.draw(screen):
                self.config.level = 27
                self.current_bg = self.bg_l_27
            if self.config.level == 27:
                self.selectedgame_level_27_button.draw(screen)
                #28
            if self.game_level_button_28.draw(screen):
                self.config.level = 28
                self.current_bg = self.bg_l_28
            if self.config.level == 28:
                self.selectedgame_level_28_button.draw(screen)
                #29
            if self.game_level_button_29.draw(screen):
                self.config.level = 29
                self.current_bg = self.bg_l_29
            if self.config.level == 29:
                self.selectedgame_level_29_button.draw(screen)
                #30
            if self.game_level_button_30.draw(screen):
                self.config.level = 30
                self.current_bg = self.bg_l_30
            if self.config.level == 30:
                self.selectedgame_level_30_button.draw(screen)
            if self.back_button.draw(screen):
                self.level = self.LEVEL_LEVEL
                


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
