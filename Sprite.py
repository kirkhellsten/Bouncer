import pygame
from GameConstants import *

class Sprite():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.backgroundColor = BACKGROUND_COLOR
        self.buffer = pygame.surface.Surface((width, height))

    def setWidth(self, width):
        self.width = width
        self.buffer = pygame.surface.Surface((self.width, self.height))

    def setHeight(self, height):
        self.height = height
        self.buffer = pygame.surface.Surface((self.width, self.height))

    def setBackgroundColor(self, color):
        self.background = color

    def render(self):
        backgroundRect = pygame.Rect((0, 0), (self.width, self.height))
        pygame.draw.rect(self.buffer, self.backgroundColor, backgroundRect)
