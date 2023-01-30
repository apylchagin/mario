#!/usr/bin/env python3

import pygame
import random
from datetime import datetime

pygame.init()

W = 800
H = 600
screen = pygame.display.set_mode((W, H))

FPS = 60
clock = pygame.time.Clock()

font_path = 'mario_font.ttf'
font_large = pygame.font.SysFont(font_path, 48)
font_small = pygame.font.SysFont(font_path, 36)

game_over = False
game_over_text = font_large.render('Game Over', True, (255, 255, 255))
game_over_rect = game_over_text.get_rect()
game_over_rect = (W // 2 - game_over_rect.width // 2, H // 2 - 100)

retry_text = font_small.render('Press any key to continue', True, (255, 255, 255))
retry_rect = retry_text.get_rect()
retry_rect = (W // 2 - retry_rect.width // 2, H // 2 + 10)

ground_image = pygame.image.load('1ground.png')
ground_image = pygame.transform.scale(ground_image, (804, 60))
GROUND_H = ground_image.get_height()

# This is a class for the sprite images where
# the same image file can be separated by several
# rectangles and each of them can be used as a single image
class SpriteFile:
    __image = None
    __rect = None
    __cols = 0
    __rows = 0

    def __init__(self, file, cols, rows):
        self.__image = pygame.image.load(file)
        self.__cols = cols
        self.__rows = rows
        self.__rect = pygame.Rect(0, 0, self.__image.get_rect().width / cols, self.__image.get_rect().height / rows)
        print(self.__rect.width)
    def getRect(self):
        return self.__rect

    def getCount(self):
        return self.__cols * self.__rows

    def getImage(self, idx, rect):
        surface = pygame.Surface((self.__rect.width, self.__rect.height), pygame.SRCALPHA, depth=32)
        __area = pygame.Rect(self.__rect)
        __area.top = (idx // self.__cols) * self.__rect.height
        __area.left = (idx % self.__cols) * self.__rect.width
        surface.blit(self.__image, self.__rect, __area)
        surface = pygame.transform.scale(surface, rect)
        return surface

# Represents single sprite of the game, i.e. single
# image.
class Sprite:
    image = None
    def __init__(self, sprites, idx, scale):
        self.image = sprites.getImage(idx, scale)
    def __init__(self, file, scale):
        self.image = pygame.image.load(file)
        self.image = pygame.transform.scale(self.image, scale)

# Represents two sprites for left and right directions
class SpriteDirection:
    left = None
    right = None
    def __init__(self, aleft, aright):
        self.left = aleft
        self.right = aright

# Represents sprites for the character movements:
# stay, jump, walk and dead
class SpriteMoves:
    stay = None
    jump = None
    walk = None
    dead = None
    def __init__(self, astay, ajump, awalk, adead):
        self.stay = astay
        self.jump = ajump
        self.walk = awalk
        self.dead = adead

    def get_rect(self):
        return self.stay.left.image.get_rect()

# Defines full set of movement related sprites for the player
# character
player_image = SpriteMoves(
    SpriteDirection(
        Sprite('Girl.stay.left.png', (60, 80)),
        Sprite('Girl.stay.right.png', (60, 80))
    ),
    SpriteDirection(
        Sprite('Girl.jump.left.png', (60, 80)),
        Sprite('Girl.jump.right.png', (60, 80))
    ),
    SpriteDirection(
        Sprite('Girl.left.png', (60, 80)),
        Sprite('Girl.right.png', (60, 80))
    ),
    Sprite('Girl.dead.png', (60, 80))
)
# Defines full set of movement related sprites for the enemy
# character
enemy_image = SpriteMoves(
    SpriteDirection(Sprite('ngoomba.png', (60, 60)), Sprite('ngoomba.png', (60, 60))),
    SpriteDirection(Sprite('ngoomba.png', (60, 60)), Sprite('ngoomba.png', (60, 60))),
    SpriteDirection(Sprite('ngoomba.png', (60, 60)), Sprite('ngoomba.png', (60, 60))),
    Sprite('deadngoomba.png', (60, 60))
)

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
    def update(self):
        self.rect.x += self.x_speed
        self.y_speed += self.gravity
        self.rect.y += self.y_speed

        if not self.is_dead:
            if self.rect.top > H - GROUND_H:
                self.is_out = True
            else:
                self.handle_input()

            if self.rect.bottom > H - GROUND_H:
                self.is_grounded = True
                self.y_speed = 0
                self.rect.bottom = H - GROUND_H
        else:
            if self.rect.top > H - GROUND_H:
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
        self.__jumpSound = pygame.mixer.Sound("jump.wav")
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
        self.rect.midbottom = (W // 2, H - GROUND_H)

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

    def update(self):
        super().update()
        if (self.x_speed > 0 and self.rect.left > W) or (self.x_speed < 0 and self.rect.right < 0):
            self.is_out = True

# Defines static background elements
class StaticBackground:
    def __init__(self, rect, image):
        self._image = image
        self._num = 0
        self._rect = rect
    def draw(self, surface):
        surface.blit(self._image, self._rect)

# Defines animated background elements
class AnimatedBackground:
    def __init__(self, rect, sprites):
        if isinstance(sprites, SpriteFile):
            self.__frames = [] 
            idx = 0
            while idx < sprites.getCount():
                self.__frames.append(sprites.getImage(idx, (rect.width, rect.height)))
                idx = idx + 1
        else:
            self.__frames = sprites
        self.__num = 0
        self.__rect = rect
        self.__lastUpdate = self.__getTime()

    def draw(self, surface):
        if (self.__getTime() - self.__lastUpdate) >= 200:
            self.__num = (self.__num + 1) % len(self.__frames)
            self.__lastUpdate = self.__getTime()
        surface.blit(self.__frames[self.__num], self.__rect)

    def __getTime(self):
        date = datetime.utcnow() - datetime(1970, 1, 1)
        seconds = (date.total_seconds())
        return int(round(seconds * 1000))

# Defines player
player = Player(player_image)

# Defines set of background elements
treeLeft = StaticBackground(
    pygame.Rect(10, H - GROUND_H - 247, 30, H - GROUND_H),
    pygame.image.load('tree.png'))

treeRight = StaticBackground(
    pygame.Rect(550, H - GROUND_H - 247, 330, H - GROUND_H),
    pygame.image.load('tree.png'))

cloudsLeft = AnimatedBackground(
    pygame.Rect(0, H - GROUND_H - 500, 50, H - GROUND_H),
    [pygame.image.load('1Clouds.png'),
     pygame.image.load('2Clouds.png'),
     pygame.image.load('3Clouds.png')])

cloudsRight = AnimatedBackground(
    pygame.Rect(500, H - GROUND_H - 500, 350, H - GROUND_H),
    [pygame.image.load('2Clouds.png'),
     pygame.image.load('3Clouds.png'),
     pygame.image.load('1Clouds.png')])


inSky = AnimatedBackground(
    pygame.Rect(400 - (31 * 2.5) // 2, 50, 31 * 2.5, 37 * 2.5),
    SpriteFile("in_sky.png", 11, 1)
)

score = 0
colorSelect=0
pygame.mixer.init()
kickSound = pygame.mixer.Sound("kick.wav")
themeSong = pygame.mixer.Sound("theme.mp3")

goombas = []

INIT_DELAY = 2000
spawn_delay = INIT_DELAY
DECREASE_BASE = 1.01
last_spawn_time = pygame.time.get_ticks()
frames=0
themeSong.play(1000)

running = not game_over

# Main drawing loop. Every iteration means drawing of
# the single frame of the game
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        elif e.type == pygame.KEYDOWN:
            if player.is_dead:
                score = 0
                spawn_delay = INIT_DELAY
                last_spawn_time = pygame.time.get_ticks()
                player.respawn()
                goombas.clear()

    clock.tick(FPS)

    frames = frames + 1

    if player.is_dead:
        screen.fill((0, 0, 45))
    elif score == 0 or (int(score / 3) % 2) == 0:
        screen.fill((92, 148, 252))
    else:
        screen.fill((0, 0, 230))

    screen.blit(ground_image, (0, H - GROUND_H))

    treeLeft.draw(screen)
    treeRight.draw(screen)
    cloudsLeft.draw(screen)
    cloudsRight.draw(screen)
    inSky.draw(screen)

    score_text_value = "Your score: " +  str(score)
    score_text = font_large.render(score_text_value, True, (255, 255, 255))
    score_rect = score_text.get_rect()

    if player.is_out:
        score_rect.midbottom = (W // 2, H // 2)
        screen.blit(game_over_text, game_over_rect)
        screen.blit(retry_text, retry_rect)
    else:
        now = pygame.time.get_ticks()
        elapsed = now - last_spawn_time

        if elapsed > spawn_delay:
            last_spawn_time = now
            goombas.append(Goomba())

        player.update()
        player.draw(screen)


        for goomba in list(goombas):
            if goomba.is_out:
                goombas.remove(goomba)
            else:
                goomba.update()
                goomba.draw(screen)

            if not player.is_dead and not goomba.is_dead and player.rect.colliderect(goomba.rect):
                if (player.rect.bottom - player.y_speed) < goomba.rect.top:
                    goomba.kill()
                    kickSound.play()
                    player.jump()
                    score += 1
                    spawn_delay = INIT_DELAY / (DECREASE_BASE ** score)
                else:
                    player.kill()

        score_rect.midtop = (W // 2, 10)

    screen.blit(score_text, score_rect)

    pygame.display.flip()
quit()
