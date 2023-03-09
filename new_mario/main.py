#!/usr/bin/env python3

import pygame, random
from datetime import datetime
from LevelMap import LevelMap
from Static import StaticBackground, StaticScaledBackground
from Animation import AnimatedBackground
from Sprites import SpriteFile

pygame.init()
pygame.mixer.init()

W = 800
H = 600
screen = pygame.display.set_mode((W, H))

FPS = 60
clock = pygame.time.Clock()
running = True

class MapProjectionBlock:
    type = None
    rect = None
    def __init__(self, projection, mapBlock):
        self.type = mapBlock.type
        self.rect = pygame.Rect(mapBlock.x * projection.block[0],
                                mapBlock.y * projection.block[1],
                                mapBlock.width * projection.block[0],
                                mapBlock.height * projection.block[1])

class MapProjection:
    blocks = None
    block = None
    def __init__(self, map, width, height):
        self.block = (width / map.width, height / map.height)
        self.blocks = []
        for block in map.blocks:
            self.blocks.append(MapProjectionBlock(self, block))

levelMap = LevelMap()
levelMap.loadFromFile("level1.map")
print('Map %s' % str(levelMap))
projectMap = MapProjection(levelMap, W, H)

backgroundElements = []

for bgBlock in projectMap.blocks:
    if bgBlock.type == 't':
        backgroundElements.append(StaticScaledBackground(bgBlock.rect, pygame.image.load('tree.png')))
    elif bgBlock.type == '=':
        backgroundElements.append(StaticScaledBackground(bgBlock.rect, pygame.image.load('ground.png')))
    elif bgBlock.type == '+':
        inSky = AnimatedBackground(
            bgBlock.rect,
            SpriteFile("in_sky.png", 11, 1), 200)
        backgroundElements.append(inSky)
    elif bgBlock.type == 'c':
        cloudsLeft = AnimatedBackground(
            bgBlock.rect,
            [pygame.image.load('1Clouds.png'),
            pygame.image.load('2Clouds.png'),
            pygame.image.load('3Clouds.png')], 200)
        backgroundElements.append(cloudsLeft)
    elif bgBlock.type == 'C':
        cloudsRight = AnimatedBackground(
            bgBlock.rect,
            [pygame.image.load('2Clouds.png'),
            pygame.image.load('3Clouds.png'),
            pygame.image.load('1Clouds.png')], 200)
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
    pygame.display.flip()
