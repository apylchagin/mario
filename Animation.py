#!/usr/bin/env python3

from datetime import datetime
from Sprites import SpriteFile

# Defines animated background elements
class AnimatedBackground:
    def __init__(self, rect, sprites, frameDelay):
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
        self.__delay = frameDelay
        self.__lastUpdate = self.__getTime()

    def draw(self, surface):
        if (self.__getTime() - self.__lastUpdate) >= self.__delay:
            self.__num = (self.__num + 1) % len(self.__frames)
            self.__lastUpdate = self.__getTime()
        surface.blit(self.__frames[self.__num], self.__rect)

    def __getTime(self):
        date = datetime.utcnow() - datetime(1970, 1, 1)
        seconds = (date.total_seconds())
        return int(round(seconds * 1000))