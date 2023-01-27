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
font_small = pygame.font.SysFont(font_path, 24)

game_over = False
retry_text = font_small.render('PRESS ANY KEY', True, (255, 255, 255))
retry_rect = retry_text.get_rect()
retry_rect.midtop = (W // 2, H // 2)

ground_image = pygame.image.load('1ground.png')
ground_image = pygame.transform.scale(ground_image, (804, 60))
GROUND_H = ground_image.get_height()

class SpriteFile:
    __image = None
    __rect = None
    __cols = 0
    __rows = 0
    def __init__(self, file, cols, rows):
        self.__image = pygame.image.load(file)
        self.__cols = cols
        self.__rows = rows
        self.__rect = pygame.rect.Rect(0, 0, self.__image.get_rect().width / cols - 1, self.__image.get_rect().height / rows - 1)
        print(self.__rect)
    def getImage(self, idx, rect):
        surface = pygame.Surface((self.__rect.width, self.__rect.height), pygame.SRCALPHA, depth=32)
        __area = self.__rect
        __area.move((idx % self.__cols) * self.__rect.width, (idx // self.__cols) * self.__rect.height)
        surface.blit(self.__image, self.__rect, __area)
        surface = pygame.transform.scale(surface, rect)
        return surface

mario_moves = SpriteFile("Girl.move.png", 1, 15)

class Sprite:
    image = None
    def __init__(self, sprites, idx, scale):
        self.image = sprites.getImage(idx, scale)
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
enemy_image = SpriteMoves(
    SpriteDirection(Sprite('ngoomba.png', (80, 80)), Sprite('ngoomba.png', (80, 80))),
    SpriteDirection(Sprite('ngoomba.png', (80, 80)), Sprite('ngoomba.png', (80, 80))),
    SpriteDirection(Sprite('ngoomba.png', (80, 80)), Sprite('ngoomba.png', (80, 80))),
    Sprite('deadngoomba.png', (80, 80))
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

class Tree:
    def __init__(self, rect, fr0, fr1, fr2):
        self.__fr0 = fr0
        self.__fr1 = fr1
        self.__fr2 = fr2
        self.__num = 0
        self.__rect = rect
        self.__lastUpdate = datetime.now().strftime("%M:%S")
    def draw(self, surface):
        if (self.__lastUpdate != datetime.now().strftime("%M:%S")):
            self.__num = (self.__num + 1)  % 3
            self.__lastUpdate = datetime.now().strftime("%M:%S")
            print("Time switched: %s" % self.__lastUpdate)
        self.__rect.right = self.__rect.right + 1
        if self.__num == 0:
            surface.blit(self.__fr0, self.__rect)
        elif self.__num == 1:
            surface.blit(self.__fr1, self.__rect)
        else:
            surface.blit(self.__fr2, self.__rect)

class Player(Entity):
    def __init__(self, image):
        super().__init__(image)
        self.__jumpSound = pygame.mixer.Sound("jump.wav")

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
        self.__jumpSound.play()

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
tree = Tree(pygame.Rect(0, H - GROUND_H - 30, 30, H - GROUND_H - 30 + 50), pygame.image.load("Girl.jump.left.png"), pygame.image.load("Girl.jump.right.png"),pygame.image.load("Girl.dead.png"))
score = 0
colorSelect=0
pygame.mixer.init()
kickSound = pygame.mixer.Sound("kick.wav")
#themeSong = pygame.mixer.Sound("theme.mp3")

goombas = []
INIT_DELAY = 2000
spawn_delay = INIT_DELAY
DECREASE_BASE = 1.01
last_spawn_time = pygame.time.get_ticks()
frames=0
running = True
#themeSong.play(1000)

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

    print("%d %s" % (frames, str(datetime.now())))

    if (score / 3) % 2 == 0:
        screen.fill((92, 148, 252))
    else:
        screen.fill((255, 0, 0))

    screen.blit(ground_image, (0, H - GROUND_H))
    
    tree.draw(screen)

    score_text = font_large.render(str(score), True, (255, 255, 255))
    score_rect = score_text.get_rect()

    if player.is_out:
        print("we're here")
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
                    kickSound.play()
                    player.jump()
                    score += 1
                    spawn_delay = INIT_DELAY / (DECREASE_BASE ** score)
                else:
                    player.kill()

        score_rect.midtop = (W // 2, 5)

    screen.blit(score_text, score_rect)
    pygame.display.flip()

quit()
