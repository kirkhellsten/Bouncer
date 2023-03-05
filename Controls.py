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
        elif keys[pygame.K_UP]:
            bouncer.direction = 'up'
        elif keys[pygame.K_DOWN]:
            bouncer.direction = 'down'
        else:
            bouncer.direction = 'none'