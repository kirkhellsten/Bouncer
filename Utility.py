import random
from GameConstants import *
import pygame
from LevelLoader import Level
import numpy as np
import cv2

class Utils:

    @staticmethod
    def writeDictToFile(dict, filename):
        f = open(filename, "w")
        for key in dict:
            f.write(f"{key}={str(dict[key])}\n")
        f.close()

    @staticmethod
    def getMiddlePosition():
        return [int((SCREEN_WIDTH / 2)), int((SCREEN_HEIGHT / 2))]

    @staticmethod
    def getRandomDirection():
        directions = ['right', 'left', 'down', 'up']
        initialDirection = directions[random.randint(0, 3)]
        return initialDirection

    @staticmethod
    def collidesWithTile(rect):
        cl = Level.currentLevel
        ri = 0
        for tileRow in cl.mapping:
            ci = 0
            for tile in tileRow:
                if tile in [TILE_NORMAL, TILE_GREEN, TILE_RED, TILE_BLACK]:
                    tilerect = pygame.Rect((ci * TILE_BLOCK_SIZE, ri * TILE_BLOCK_SIZE),
                                           (TILE_BLOCK_SIZE, TILE_BLOCK_SIZE))
                    if rect.x < tilerect.x + tilerect.width and rect.y < tilerect.y + tilerect.height \
                        and rect.x + rect.width > tilerect.x and rect.y + rect.height > tilerect.y:
                        return True
                ci += 1
            ri += 1
        return False


    @staticmethod
    def getBallDirections(sourceRect, previousCenterPosition, radius):
        dirs = []
        if previousCenterPosition[0] + radius < sourceRect.x:
            dirs.append('left')
        if previousCenterPosition[0] - radius > sourceRect.x + sourceRect.width:
            dirs.append('right')
        if previousCenterPosition[1] + radius < sourceRect.y:
            dirs.append('top')
        if previousCenterPosition[1] - radius > sourceRect.y + sourceRect.height:
            dirs.append('bottom')
        return dirs

    def create_neon(surf):
        surf_alpha = surf.convert_alpha()
        rgb = pygame.surfarray.array3d(surf_alpha)
        alpha = pygame.surfarray.array_alpha(surf_alpha).reshape((*rgb.shape[:2], 1))
        image = np.concatenate((rgb, alpha), 2)
        cv2.GaussianBlur(image, ksize=(9, 9), sigmaX=10, sigmaY=10, dst=image)
        cv2.blur(image, ksize=(5, 5), dst=image)
        bloom_surf = pygame.image.frombuffer(image.flatten(), image.shape[1::-1], 'RGBA')
        return bloom_surf

    def dropShadowText(buffer, text, size, x, y, colour=(255,255,255), drop_colour=(128,128,128), font=None):
        # how much 'shadow distance' is best?
        dropshadow_offset = 1 + (size // 15)
        text_font = pygame.font.Font(font, size)
        # make the drop-shadow
        text_bitmap = text_font.render(text, True, drop_colour)
        buffer.blit(text_bitmap, (x+dropshadow_offset, y+dropshadow_offset) )
        # make the overlay text
        text_bitmap = text_font.render(text, True, colour)
        buffer.blit(text_bitmap, (x, y) )