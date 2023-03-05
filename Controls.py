import pygame
from GameObjects import *

class Controls:

    @staticmethod
    def key_pressed(keys):
        bouncer = Bouncer.bouncer
        if keys[pygame.K_LEFT]:
            bouncer.direction = 'left'
        elif keys[pygame.K_RIGHT]:
            bouncer.direction = 'right'
        else:
            bouncer.direction = 'none'