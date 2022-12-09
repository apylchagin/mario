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

INIT_DELAY = 2000
spawn_delay = INIT_DELAY
DECREASE_BASE = 1.01
last_spawn_time = pygame.time.get_ticks()

game_over = False
retry_text = font_small.render('PRESS ANY KEY', True, (255, 255, 255))
retry_rect = retry_text.get_rect()
retry_rect.midtop = (W // 2, H // 2)

score = 0

ground_image = pygame.image.load('ground.png')
ground_image = pygame.transform.scale(ground_image, (804, 60))
GROUND_H = ground_image.get_height()

enemy_image = pygame.image.load('goomba.png')
enemy_image = pygame.transform.scale(enemy_image, (80, 80))

enemy_dead_image = pygame.image.load('goomba_dead.png')
enemy_dead_image = pygame.transform.scale(enemy_dead_image, (80, 80))

player_image = pygame.image.load('mario.png')
player_image = pygame.transform.scale(player_image, (60, 80))

flower_image = pygame.image.load('flower.png')
flower_image = pygame.transform.scale(flower_image, (60, 80))

class Entity:
    def __init__(self, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.y_speed = 0
        self.x_speed = 0
        self.speed = 5
        self.is_out = False
        self.is_dead = False
        self.jump_speed = -12
        self.gravity = 0.5
        self.is_grounded = False

    def handle_input(self):
        pass

    def kill(self, dead_image):
        self.image = dead_image
        self.is_dead = True
        self.x_speed = -self.x_speed
        self.y_speed = self.jump_speed

    def update(self):
        self.rect.x += self.x_speed
        self.y_speed += self.gravity
        self.rect.y += self.y_speed

        if self.is_dead:
            if self.rect.top > H - GROUND_H:
                self.is_out = True
        else:
            self.handle_input()

            if self.rect.bottom > H - GROUND_H:
                self.is_grounded = True
                self.y_speed = 0
                self.rect.bottom = H - GROUND_H

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Goomba(Entity):
    def __init__(self):
        super().__init__(enemy_image)
        self.spawn()

    def spawn(self):
        direction = random.randint(0, 1)
        if direction == 0:
            self.x_speed = -self.speed
            self.rect.bottomleft = (W, 0)
        else:
            self.x_speed = self.speed
            self.rect.bottomright = (0, 0)

    def update(self):
        super().update()
        if self.x_speed > 0 and self.rect.left > W or self.x_speed < 0 and self.rect.right < 0:
            self.is_out = True


class Player(Entity):
    def __init__(self):
        super().__init__(player_image)
        self.respawn()

    def handle_input(self):
        self.x_speed = 0

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.x_speed = -self.speed
        elif keys[pygame.K_d]:
            self.x_speed = self.speed

        if self.is_grounded and keys[pygame.K_SPACE]:
            self.is_grounded = False
            self.jump()

    def respawn(self):
        self.is_out = False
        self.is_dead = False
        self.rect.midbottom = (W // 2, H)

    def jump(self):
        self.y_speed = self.jump_speed

class Tree(Entity):
    def __init__(self):
        super().__init__(flower_image)
        self.respawn()
    def update(self):
        super().update()
    def respawn(self):
        self.is_out = False
        self.is_dead = False
        self.rect.midbottom = (W // 4, H)
        

player = Player()
tree = Tree()

goombas = []

running = True
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        elif e.type == pygame.KEYDOWN:
            if player.is_out:
                score = 0
                finish_delay = INIT_DELAY
                last_spawn_time = pygame.time.get_ticks()
                player.respawn()
                goombas.clear()

    clock.tick(FPS)

    screen.fill((92, 148, 252))
    screen.blit(ground_image, (0, H - GROUND_H))

    score_surface = font_large.render(str(score), True, (255, 255, 255))
    score_rect = score_surface.get_rect()

    if player.is_out:
        score_rect.midbottom = (W // 2, H // 2)

        screen.blit(retry_text, retry_rect)
    else:
        now = pygame.time.get_ticks()
        elapsed = now - last_spawn_time

        if elapsed > spawn_delay:
            last_spawn_time = pygame.time.get_ticks()
            goombas.append(Goomba())

        tree.update()
        tree.draw(screen)

        player.update()
        player.draw(screen)

        for goomba in list(goombas):
            if goomba.is_out:
                goombas.remove(goomba)
            else:
                goomba.update()
                goomba.draw(screen)

                if not player.is_dead and not goomba.is_dead and player.rect.colliderect(goomba.rect):
                    if player.rect.bottom - player.y_speed < goomba.rect.top:
                        goomba.kill(enemy_dead_image)
                        player.jump()
                        score += 1
                        spawn_delay = INIT_DELAY / (DECREASE_BASE ** score)
                    else:
                        player.kill(player_image)

        
        score_rect.midtop = (W // 2, 5)

    screen.blit(score_surface, score_rect)

    pygame.display.flip()
quit()