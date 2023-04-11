#!/usr/bin/env python3

import pygame

# Defines static background elements
class StaticBackground:
    def __init__(self, rect, image):
        self._image = image
        self._rect = rect
    def draw(self, surface):
        surface.blit(self._image, self._rect)

class StaticScaledBackground:
    def __init__(self, rect, image):
        self._image = pygame.transform.scale(image, (rect.width, rect.height))
        self._rect = rect
    def draw(self, surface):
        surface.blit(self._image, self._rect)