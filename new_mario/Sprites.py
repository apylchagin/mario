#!/usr/bin/env python3

import pygame

# Represent the sprite file data.
# The single files contains set of images with the same
# width and height
class SpriteFile:
    __image = None
    __rect = None
    __cols = 0
    __rows = 0

    # Constructor
    def __init__(self, file, cols, rows):
        self.__image = pygame.image.load(file)
        self.__cols = cols
        self.__rows = rows
        self.__rect = pygame.Rect(0, 0, self.__image.get_rect().width / cols, self.__image.get_rect().height / rows)
        print(self.__rect.width)
    
    # The single image region
    def getRect(self):
        return self.__rect

    # The amount of images within the sprite
    def getCount(self):
        return self.__cols * self.__rows

    # Get image by idex and scaled into the provided rectangle
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
    # Constructor
    def __init__(self, sprites, idx, scale):
        self.image = sprites.getImage(idx, scale)
    # Constructor
    def __init__(self, file, scale):
        self.image = pygame.image.load(file)
        self.image = pygame.transform.scale(self.image, scale)

# Represents sprites for the character movements:
# stay, jump, walk and dead
class SpriteMoves:
    stay = None
    jump = None
    walk = None
    dead = None

    # Constructor
    def __init__(self, astay, ajump, awalk, adead):
        self.stay = astay
        self.jump = ajump
        self.walk = awalk
        self.dead = adead

    def get_rect(self):
        return self.stay.left.image.get_rect()

# Represents two sprites for left and right directions
class SpriteDirection:
    left = None
    right = None
    def __init__(self, aleft, aright):
        self.left = aleft
        self.right = aright