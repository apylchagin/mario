#!/usr/bin/env python3

import pygame, random
from enum import Enum
from LevelMap import LevelMap
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

class MapProjectionBlockType(Enum):
    GROUND = '='
    PLAYER = 'p'
    TREE = 't'
    MISC = '\0'

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
        if type == 'p':
            return MapProjectionBlockType.PLAYER
        if type == 't':
            return MapProjectionBlockType.TREE
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
            if block.type == MapProjectionBlockType.GROUND:
                if (__x >= block.rect.left) and (__x <= block.rect.right) and (__y <= block.rect.top):
                    if (__yMinDist > (block.rect.top - __y)):
                        __result = block.rect
                        __yMinDist = block.rect.top - __y
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
            if self.rect.top > __ground.top:
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




levelMap = LevelMap()
levelMap.loadFromFile("level1.map")
print('Map %s' % str(levelMap))
projectMap = MapProjection(levelMap, W, H)

backgroundElements = []

# Defines full set of movement related sprites for the player
# character
player_block = projectMap.getBlock(MapProjectionBlockType.PLAYER)
player_image = SpriteMoves(
    SpriteDirection(
        Sprite('images/Girl.stay.left.png', player_block.sizes()),
        Sprite('images/Girl.stay.right.png', player_block.sizes())
    ),
    SpriteDirection(
        Sprite('images/Girl.jump.left.png', player_block.sizes()),
        Sprite('images/Girl.jump.right.png', player_block.sizes())
    ),
    SpriteDirection(
        Sprite('images/Girl.left.png', player_block.sizes()),
        Sprite('images/Girl.right.png', player_block.sizes())
    ),
    Sprite('images/Girl.dead.png', player_block.sizes())
)
player = Player(player_image)

# Load blocks content per type
for bgBlock in projectMap.blocks:
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
    elif bgBlock.type == '+':
        inSky = AnimatedBackground(
            bgBlock.rect,
            SpriteFile('images/inSkyGoomba.png', 11, 1), 200)
        backgroundElements.append(inSky)
    elif bgBlock.type == 'c':
        cloudsLeft = AnimatedBackground(bgBlock.rect,
            [pygame.image.load('images/1Clouds.png'),
             pygame.image.load('images/2Clouds.png'),
             pygame.image.load('images/3Clouds.png')],
            200)
        backgroundElements.append(cloudsLeft)
    elif bgBlock.type == 'C':
        cloudsRight = AnimatedBackground(bgBlock.rect,
            [pygame.image.load('images/2Clouds.png'),
             pygame.image.load('images/3Clouds.png'),
             pygame.image.load('images/1Clouds.png')],
            200)
        backgroundElements.append(cloudsRight)

# Main drawing loop. Every iteration means drawing of
# the single frame of the game
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

    clock.tick(FPS)
    screen.fill((92, 148, 252))
    for element in backgroundElements:
        element.draw(screen)
    player.update(projectMap)
    player.draw(screen)
    pygame.display.flip()
