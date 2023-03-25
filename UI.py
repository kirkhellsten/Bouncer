import pygame
from Sprite import *

class UIMenuItem(Sprite):
    def __init__(self, x, y, text, fontsize=48, textcolor=(50,50,50), padding=15, width=200, selected=False):
        self.textFont = pygame.font.SysFont(None, fontsize)
        self.textColor = textcolor
        self.selectedColor = (255, 179, 0)
        self.selectedTextColor = (225, 225, 225)
        self.text = text
        self.padding = padding
        self.centerText = True
        self.selected = selected
        text_width, text_height = self.textFont.size(text)
        super().__init__(x, y, width + self.padding*2, text_height + self.padding*2)
        self.backgroundColor = (200, 200, 200)

    def setSelected(self, selected):
        self.selected = selected

    def getSelected(self):
        return self.selected

    def render(self):
        #super().render()

        backgroundRect = pygame.Rect((0, 0), (self.width, self.height))

        if self.selected:
            img = self.textFont.render(self.text, True, self.selectedTextColor)
            pygame.draw.rect(self.buffer, self.selectedColor, backgroundRect)
        else:
            img = self.textFont.render(self.text, True, self.textColor)
            pygame.draw.rect(self.buffer, self.backgroundColor, backgroundRect)

        if self.centerText:
            text_width, text_height = self.textFont.size(self.text)
            self.buffer.blit(img, (self.width / 2 - text_width / 2, self.padding))
        else:
            self.buffer.blit(img, (self.padding, self.padding))

class UIMenu(Sprite):
    def __init__(self, x, y, title="Main Menu", fontsize=96, textcolor=(255,255,255)):
        self.titleFont = pygame.font.SysFont(None, fontsize)
        self.textColor = textcolor
        self.title = title
        self.sprites = []
        text_width, text_height = self.titleFont.size(title)
        super().__init__(x, y, text_width, text_height)

    def render(self):
        super().render()
        img = self.titleFont.render(self.title, True, self.textColor)
        self.buffer.blit(img, (0, 0))

