#!/usr/bin/env python3

import pygame, random
from datetime import datetime
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

font_path = 'fonts/mario_font.ttf'
font_large = pygame.font.SysFont(font_path, 48)
font_small = pygame.font.SysFont(font_path, 36)

game_over = False
game_over_text = font_large.render('Game Over', True, (255, 255, 255))
game_over_rect = game_over_text.get_rect()
game_over_rect = (W // 2 - game_over_rect.width // 2, H // 2 - 100)

retry_text = font_small.render('Press any key to continue', True, (255, 255, 255))
retry_rect = retry_text.get_rect()
retry_rect = (W // 2 - retry_rect.width // 2, H // 2 + 10)

kickSound = pygame.mixer.Sound("sounds/kick.wav")
themeSong = pygame.mixer.Sound("sounds/theme.mp3")

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

levelName = "level1.map"
levelMap = LevelMap()
levelMap.loadFromFile(levelName)
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

# Defines full set of movement related sprites for the enemy
# character
enemy_image = SpriteMoves(
    SpriteDirection(Sprite('images/ngoomba.png', (60, 60)), Sprite('images/ngoomba.png', (60, 60))),
    SpriteDirection(Sprite('images/ngoomba.png', (60, 60)), Sprite('images/ngoomba.png', (60, 60))),
    SpriteDirection(Sprite('images/ngoomba.png', (60, 60)), Sprite('images/ngoomba.png', (60, 60))),
    Sprite('images/deadngoomba.png', (60, 60))
)

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

class DebugDrawings:
    enabled = False
    def __init__(self, alevelMap : LevelMap, aprojectionMap : MapProjection):
        self.levelMap = alevelMap
        self.projectionMap = aprojectionMap

    def draw(self, surface : pygame.Surface):
        if not self.enabled:
            return
        for block in self.projectionMap.blocks:
            pygame.draw.rect(surface, (255, 0 ,0), block.rect, 2)
    
debug = DebugDrawings(levelMap, projectMap)

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

goombas = []

INIT_DELAY = 2000
spawn_delay = INIT_DELAY
DECREASE_BASE = 1.01
last_spawn_time = pygame.time.get_ticks()
frames=0
themeSong.play(1000)

# Main drawing loop. Every iteration means drawing of
# the single frame of the game
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        elif e.type == pygame.KEYDOWN:
            if player.is_dead:
                score.reset()
                timer.reset()
                spawn_delay = INIT_DELAY
                last_spawn_time = pygame.time.get_ticks()
                player.respawn()
                goombas.clear()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_m]:
        debug.enabled = not debug.enabled

    clock.tick(FPS)

    frames = frames + 1

    if player.is_dead:
        screen.fill((0, 0, 45))
    elif score.value == 0 or (int(score.value / 3) % 2) == 0:
        screen.fill((92, 148, 252))
    else:
        screen.fill((0, 0, 230))

    for element in backgroundElements:
        element.draw(screen)
    score.draw(screen)
    if not player.is_dead:
        timer.draw(screen)

    if player.is_out:
        score.moveTo((W // 2, H // 2 - 45))
        screen.blit(game_over_text, game_over_rect)
        screen.blit(retry_text, retry_rect)
    else:
        now = pygame.time.get_ticks()
        elapsed = now - last_spawn_time

        if elapsed > spawn_delay:
            last_spawn_time = now
            goombas.append(Goomba())

        player.update(projectMap)
        player.draw(screen)

        for goomba in list(goombas):
            if goomba.is_out:
                goombas.remove(goomba)
            else:
                goomba.update(projectMap)
                goomba.draw(screen)

            if not player.is_dead and not goomba.is_dead and player.rect.colliderect(goomba.rect):
                if (player.rect.bottom - player.y_speed) < goomba.rect.top:
                    goomba.kill()
                    kickSound.play()
                    player.jump()
                    score.inc()
                    spawn_delay = INIT_DELAY / (DECREASE_BASE ** score.value)
                else:
                    player.kill()

        score.moveTo((W // 2, 10))

    debug.draw(screen)
    pygame.display.flip()
