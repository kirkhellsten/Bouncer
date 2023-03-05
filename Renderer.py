import pygame
from GameConstants import *
from GameObjects import *
from Utility import Utils

class Renderer:

    @staticmethod
    def __drawBackground():
        screenBuffer.fill(BACKGROUND_COLOR)

    @staticmethod
    def __drawBouncer():
        bouncer = Bouncer.bouncer
        pygame.draw.circle(screenBuffer, BOUNCER_COLOR, (int(bouncer.position[0]), int(bouncer.position[1])), bouncer.radius)
        pygame.gfxdraw.circle(screenBuffer, int(bouncer.position[0]), int(bouncer.position[1]), bouncer.radius, BOUNCER_BORDER_COLOR)

    @staticmethod
    def __drawLevelTiles():
        cl = Level.currentLevel
        ri = 0
        for tileRow in cl.mapping:
            ci = 0
            for tile in tileRow:
                if tile == 1:
                    tilerect = pygame.Rect((ci * TILE_BLOCK_SIZE, ri * TILE_BLOCK_SIZE),
                                           (TILE_BLOCK_SIZE, TILE_BLOCK_SIZE))
                    pygame.draw.rect(screenBuffer, TILE_COLOR, tilerect)
                    pygame.draw.rect(screenBuffer, TILE_BORDER_COLOR, tilerect, TILE_BORDER_WIDTH, TILE_BORDER_RADIUS)
                    pygame.gfxdraw.rectangle(screenBuffer, tilerect, TILE_BORDER_COLOR)
                elif tile == 2:
                    triangle = [(ci * TILE_BLOCK_SIZE, (ri + 1) * TILE_BLOCK_SIZE),
                                ((ci + 1 / 2) * TILE_BLOCK_SIZE, ri * TILE_BLOCK_SIZE),
                                ((ci + 1 ) * TILE_BLOCK_SIZE, (ri + 1) * TILE_BLOCK_SIZE)]
                    pygame.draw.polygon(screenBuffer, (255, 255, 255), triangle)
                elif tile == 3:
                    tilerect = pygame.Rect((ci * TILE_BLOCK_SIZE, ri * TILE_BLOCK_SIZE),
                                           (TILE_BLOCK_SIZE, TILE_BLOCK_SIZE))
                    pygame.draw.rect(screenBuffer, (0,255,0), tilerect)
                    pygame.draw.rect(screenBuffer, (255,255,255), tilerect, TILE_BORDER_WIDTH, TILE_BORDER_RADIUS)
                    pygame.gfxdraw.rectangle(screenBuffer, tilerect, TILE_BORDER_COLOR)
                ci += 1
            ri += 1

    @staticmethod
    def __drawExitDoor():
        exitDoor = ExitDoor.exitDoor
        exitDoorRect = pygame.Rect((exitDoor.position[0], exitDoor.position[1]), (exitDoor.width, exitDoor.height))
        pygame.draw.rect(screenBuffer, EXIT_DOOR_BG_COLOR, exitDoorRect)


    @staticmethod
    def __drawGlowExitDoor():
        exitDoor = ExitDoor.exitDoor
        image = pygame.Surface((95, 95), pygame.SRCALPHA)
        pygame.draw.rect(image, (255, 255, 255), (10, 10, 60, 30))
        neon_image = Utils.create_neon(image)
        screenBuffer.blit(neon_image,
                          neon_image.get_rect(center=(exitDoor.position[0]+exitDoor.width+10, exitDoor.position[1]+exitDoor.height/2+10)),
                                              special_flags=pygame.BLEND_PREMULTIPLIED)
    @staticmethod
    def __drawExitDoorText():
        exitDoor = ExitDoor.exitDoor
        font = pygame.font.SysFont(None, 24)
        Utils.dropShadowText(screenBuffer, "Exit", 24, exitDoor.position[0]-4, exitDoor.position[1]-16, (255, 0, 0), (100, 0, 0))


    @staticmethod
    def __drawMovingPlatforms():
        platforms = MovingPlatform.platforms
        for platform in platforms:
            exitDoorRect = pygame.Rect((platform.position[0], platform.position[1]), (platform.width, platform.height))
            pygame.draw.rect(screenBuffer, (33, 37, 41), exitDoorRect)
            pygame.draw.rect(screenBuffer, (255, 255, 255), exitDoorRect, 1, 1)

    @staticmethod
    def __drawPixels():
        try:
            pixelsList = Pixels.pixelsList
            for pixels in pixelsList:
                for bit in pixels.bits:
                    pixelRect = pygame.Rect((bit[0], bit[1]), BITS_SIZE)
                    pygame.draw.rect(screenBuffer, BITS_COLOR, pixelRect)
        except Exception as e:
            return None

    @staticmethod
    def __drawLaserVGuns():
        guns = LaserVGun.guns
        for gun in guns:
            gunRect = pygame.Rect((gun.position[0], gun.position[1]), (VGUN_WIDTH, VGUN_HEIGHT))
            pygame.draw.rect(screenBuffer, VGUN_COLOR, gunRect)

    @staticmethod
    def __drawLaserV():
        try:
            lasers = LaserV.lasers
            for laser in lasers:
                laserRect = pygame.Rect((laser.position[0], laser.position[1]), (laser.width, laser.height))
                pygame.draw.rect(screenBuffer, (255, 0, 0), laserRect)
        except Exception as e:
            return None

    @staticmethod
    def draw():

        Renderer.__drawBackground()
        Renderer.__drawPixels()

        Renderer.__drawLaserV()

        Renderer.__drawExitDoor()
        Renderer.__drawBouncer()
        Renderer.__drawGlowExitDoor()
        Renderer.__drawExitDoorText()
        Renderer.__drawLevelTiles()
        Renderer.__drawMovingPlatforms()

        Renderer.__drawLaserVGuns()