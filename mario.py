#!/usr/bin/env python3
import pygame
import random
pygame.init()

W = 800
H = 600
screen = pygame.display.set_mode((W, H))

FPS = 60
clock = pygame.time.Clock()

font_path = 'mario_font.ttf'
font_large = pygame.font.SysFont(font_path, 48)
font_small = pygame.font.SysFont(font_path, 24)

game_over = False
retry_text = font_small.render('PRESS ANY KEY', True, (255, 255, 255))
retry_rect = retry_text.get_rect()
retry_rect = (W // 2, H // 2)

ground_image = pygame.image.load('ground.png')
ground_image = pygame.transform.scale(ground_image, (804, 60))
GROUND_H = ground_image.get_height()

class SpriteFile:
    __image = None
    __rect = None
    def __init__(self, file, w, h):
        self.__image = pygame.image.load(file)
        self.__rect = pygame.rect.Rect(0, 0, self.__image.get_rect().width / w - 1, self.__image.get_rect().height / h - 1)

class Sprite:
    image = None
    def __init__(self, file, scale):
        self.image = pygame.image.load(file)
        self.image = pygame.transform.scale(self.image, scale)

class SpriteDirection:
    left = None
    right = None
    def __init__(self, aleft, aright):
        self.left = aleft
        self.right = aright
    
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

player_image = SpriteMoves(
    SpriteDirection(Sprite('mario_stay_l.png', (60,80)), Sprite('mario_stay_r.png', (60,80))),
    SpriteDirection(Sprite('mario_jump_l.png', (60,80)), Sprite('mario_jump_r.png', (60,80))),
    SpriteDirection(Sprite('mario_walk_l.png', (60,80)), Sprite('mario_walk_r.png', (60,80))),
    Sprite('mario_dead.png', (60,80))
)
player_dead_image = Sprite('mario_dead.png', (60,80))
enemy_image = SpriteMoves(
    SpriteDirection(Sprite('goomba.png', (80,80)), Sprite('goomba.png', (80,80))),
    SpriteDirection(Sprite('goomba.png', (80,80)), Sprite('goomba.png', (80,80))),
    SpriteDirection(Sprite('goomba.png', (80,80)), Sprite('goomba.png', (80,80))),
    Sprite('goomba_dead.png', (80,80))
)
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

class Player(Entity):
    def __init__(self, image):
        super().__init__(image)
        self.respawn()
        
    def handle_input(self):
        self.x_speed = 0

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.x_speed = -self.speed
            self.look_right = False
        elif keys[pygame.K_d]:
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


player = Player(player_image)
score = 0

goombas = []
INIT_DELAY = 2000
spawn_delay = INIT_DELAY
DECREASE_BASE = 1.01
last_spawn_time = pygame.time.get_ticks()

running = True
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

    screen.fill((92, 148, 252))

    screen.blit(ground_image, (0, H - GROUND_H))

    score_text = font_large.render(str(score), True, (255, 255, 255))
    score_rect = score_text.get_rect()

    if player.is_out:
        score_rect.midbottom = (W // 2, H // 2)

        screen.blit(retry_text, retry_rect)
    else:    
        player.update()
        player.draw(screen)

        now = pygame.time.get_ticks()
        elapsed = now - last_spawn_time
        if elapsed > spawn_delay:
            last_spawn_time = now
            goombas.append(Goomba())

        for goomba in list(goombas):
            if goomba.is_out:
                goombas.remove(goomba)
            else:
                goomba.update()
                goomba.draw(screen)
 
            if not player.is_dead and not goomba.is_dead and player.rect.colliderect(goomba.rect):
                if (player.rect.bottom - player.y_speed) < goomba.rect.top:
                    goomba.kill()
                    player.jump()
                    score += 1
                    spawn_delay = INIT_DELAY / (DECREASE_BASE ** score)
                else:
                    player.kill()

        score_rect.midtop = (W // 2, 5)

    screen.blit(score_text, score_rect)
    pygame.display.flip()

quit()
