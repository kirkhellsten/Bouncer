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
        if bouncer.visible == False:
            return None

        pygame.draw.circle(screenBuffer, BOUNCER_COLOR, (int(bouncer.centerPosition[0]), int(bouncer.centerPosition[1])), bouncer.radius)
        pygame.gfxdraw.circle(screenBuffer, int(bouncer.centerPosition[0]), int(bouncer.centerPosition[1]), bouncer.radius, BOUNCER_BORDER_COLOR)

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
                    floorSpikes = [(ci * TILE_BLOCK_SIZE, (ri + 1) * TILE_BLOCK_SIZE),
                                ((ci + 1 / 2) * TILE_BLOCK_SIZE, ri * TILE_BLOCK_SIZE),
                                ((ci + 1 ) * TILE_BLOCK_SIZE, (ri + 1) * TILE_BLOCK_SIZE)]
                    pygame.draw.polygon(screenBuffer, SPIKE_COLOR, floorSpikes)
                elif tile == 8:
                    ceilSpikes = [(ci * TILE_BLOCK_SIZE, ri * TILE_BLOCK_SIZE),
                                ((ci + 1/2) * TILE_BLOCK_SIZE, (ri+1) * TILE_BLOCK_SIZE),
                                ((ci + 1) * TILE_BLOCK_SIZE, ri * TILE_BLOCK_SIZE)]
                    pygame.draw.polygon(screenBuffer, SPIKE_COLOR, ceilSpikes)
                elif tile == 5:
                    rightWallSpikes = [(ci * TILE_BLOCK_SIZE, (ri + 1/2) * TILE_BLOCK_SIZE),
                                ((ci + 1) * TILE_BLOCK_SIZE, ri * TILE_BLOCK_SIZE),
                                ((ci + 1) * TILE_BLOCK_SIZE, (ri + 1) * TILE_BLOCK_SIZE)]
                    pygame.draw.polygon(screenBuffer, SPIKE_COLOR, rightWallSpikes)
                elif tile == 6:
                    leftWallSpikes = [(ci * TILE_BLOCK_SIZE, (ri * TILE_BLOCK_SIZE)),
                                ((ci + 1) * TILE_BLOCK_SIZE, (ri+1/2) * TILE_BLOCK_SIZE),
                                (ci * TILE_BLOCK_SIZE, (ri + 1) * TILE_BLOCK_SIZE)]
                    pygame.draw.polygon(screenBuffer, SPIKE_COLOR, leftWallSpikes)
                elif tile == 3:
                    tilerect = pygame.Rect((ci * TILE_BLOCK_SIZE, ri * TILE_BLOCK_SIZE),
                                           (TILE_BLOCK_SIZE, TILE_BLOCK_SIZE))
                    pygame.draw.rect(screenBuffer, (0,255,0), tilerect)
                    pygame.draw.rect(screenBuffer, (255,255,255), tilerect, TILE_BORDER_WIDTH, TILE_BORDER_RADIUS)
                    pygame.gfxdraw.rectangle(screenBuffer, tilerect, TILE_BORDER_COLOR)
                elif tile == 4:
                    tilerect = pygame.Rect((ci * TILE_BLOCK_SIZE, ri * TILE_BLOCK_SIZE),
                                           (TILE_BLOCK_SIZE, TILE_BLOCK_SIZE))
                    pygame.draw.rect(screenBuffer, (255,0,0), tilerect)
                    pygame.draw.rect(screenBuffer, (255,255,255), tilerect, TILE_BORDER_WIDTH, TILE_BORDER_RADIUS)
                    pygame.gfxdraw.rectangle(screenBuffer, tilerect, TILE_BORDER_COLOR)
                elif tile == 7:
                    tilerect = pygame.Rect((ci * TILE_BLOCK_SIZE, ri * TILE_BLOCK_SIZE),
                                           (TILE_BLOCK_SIZE, TILE_BLOCK_SIZE))
                    pygame.draw.rect(screenBuffer, (0,0,0), tilerect)
                    pygame.draw.rect(screenBuffer, (255,255,255), tilerect, TILE_BORDER_WIDTH, TILE_BORDER_RADIUS)
                    pygame.gfxdraw.rectangle(screenBuffer, tilerect, TILE_BORDER_COLOR)
                elif tile == TILE_RAILTRACK_HORIZONTAL:
                    pygame.draw.line(screenBuffer, RAILTRACK_COLOR, (ci * TILE_BLOCK_SIZE, (ri+1/2)*TILE_BLOCK_SIZE),
                                        ((ci + 1) * TILE_BLOCK_SIZE, (ri+1/2)*TILE_BLOCK_SIZE),
                                        2)
                elif tile == TILE_RAILTRACK_VERTICAL:
                    pygame.draw.line(screenBuffer, RAILTRACK_COLOR, ((ci+1/2) * TILE_BLOCK_SIZE, ri*TILE_BLOCK_SIZE),
                                        ((ci+1/2) * TILE_BLOCK_SIZE, (ri+1)*TILE_BLOCK_SIZE),
                                        2)
                elif tile == TILE_RAILTRACK_BOTTOM_LEFT:
                    pygame.draw.line(screenBuffer, RAILTRACK_COLOR, ((ci+1/2) * TILE_BLOCK_SIZE, (ri+1/2)*TILE_BLOCK_SIZE),
                                        ((ci+1) * TILE_BLOCK_SIZE, (ri+1/2)*TILE_BLOCK_SIZE),
                                        2)
                    pygame.draw.line(screenBuffer, RAILTRACK_COLOR, ((ci+1/2) * TILE_BLOCK_SIZE, ri*TILE_BLOCK_SIZE),
                                        ((ci+1/2) * TILE_BLOCK_SIZE, (ri+1/2)*TILE_BLOCK_SIZE),
                                        2)
                elif tile == TILE_RAILTRACK_TOP_LEFT:
                    pygame.draw.line(screenBuffer, RAILTRACK_COLOR, ((ci+1/2) * TILE_BLOCK_SIZE, (ri+1/2)*TILE_BLOCK_SIZE),
                                        ((ci+1) * TILE_BLOCK_SIZE, (ri+1/2)*TILE_BLOCK_SIZE),
                                        2)
                    pygame.draw.line(screenBuffer, RAILTRACK_COLOR, ((ci+1/2) * TILE_BLOCK_SIZE, (ri+1/2)*TILE_BLOCK_SIZE),
                                        ((ci+1/2) * TILE_BLOCK_SIZE, (ri+1)*TILE_BLOCK_SIZE),
                                        2)
                elif tile == TILE_RAILTRACK_TOP_RIGHT:
                    pygame.draw.line(screenBuffer, RAILTRACK_COLOR, (ci * TILE_BLOCK_SIZE, (ri+1/2)*TILE_BLOCK_SIZE),
                                        ((ci+1/2) * TILE_BLOCK_SIZE, (ri+1/2)*TILE_BLOCK_SIZE),
                                        2)
                    pygame.draw.line(screenBuffer, RAILTRACK_COLOR, ((ci+1/2) * TILE_BLOCK_SIZE, (ri+1/2)*TILE_BLOCK_SIZE),
                                        ((ci+1/2) * TILE_BLOCK_SIZE, (ri+1)*TILE_BLOCK_SIZE),
                                        2)
                elif tile == TILE_RAILTRACK_BOTTOM_RIGHT:
                    pygame.draw.line(screenBuffer, RAILTRACK_COLOR, (ci*TILE_BLOCK_SIZE, (ri+1/2)*TILE_BLOCK_SIZE),
                                        ((ci+1/2) * TILE_BLOCK_SIZE, (ri+1/2)*TILE_BLOCK_SIZE),
                                        2)
                    pygame.draw.line(screenBuffer, RAILTRACK_COLOR,
                                     ((ci + 1 / 2) * TILE_BLOCK_SIZE, ri * TILE_BLOCK_SIZE),
                                     ((ci + 1 / 2) * TILE_BLOCK_SIZE, (ri + 1/2) * TILE_BLOCK_SIZE),
                                     2)

                elif tile == TILE_RAILTRACK_LEFT_STOP:
                    pygame.draw.line(screenBuffer, RAILTRACK_COLOR, ((ci+1/2)*TILE_BLOCK_SIZE, (ri+1/2)*TILE_BLOCK_SIZE),
                                        ((ci+1) * TILE_BLOCK_SIZE, (ri+1/2)*TILE_BLOCK_SIZE),
                                        2)
                    stoprect = pygame.Rect(( (ci+1/2) * TILE_BLOCK_SIZE - 3, (ri+1/2) * TILE_BLOCK_SIZE - 3),
                                           (7, 7))
                    pygame.draw.rect(screenBuffer, RAILTRACK_COLOR, stoprect)
                elif tile == TILE_RAILTRACK_RIGHT_STOP:
                    pygame.draw.line(screenBuffer, RAILTRACK_COLOR, (ci*TILE_BLOCK_SIZE, (ri+1/2)*TILE_BLOCK_SIZE),
                                        ((ci+1/2) * TILE_BLOCK_SIZE, (ri+1/2)*TILE_BLOCK_SIZE),
                                        2)
                    stoprect = pygame.Rect(( (ci+1/2) * TILE_BLOCK_SIZE - 3, (ri+1/2) * TILE_BLOCK_SIZE - 3),
                                           (7, 7))
                    pygame.draw.rect(screenBuffer, RAILTRACK_COLOR, stoprect)
                elif tile == TILE_RAILTRACK_TOP_STOP:
                    pygame.draw.line(screenBuffer, RAILTRACK_COLOR, ((ci+1/2)*TILE_BLOCK_SIZE, (ri+1/2)*TILE_BLOCK_SIZE),
                                        ((ci+1/2) * TILE_BLOCK_SIZE, (ri+1)*TILE_BLOCK_SIZE),
                                        2)
                    stoprect = pygame.Rect(( (ci+1/2) * TILE_BLOCK_SIZE - 3, (ri+1/2) * TILE_BLOCK_SIZE - 3),
                                           (7, 7))
                    pygame.draw.rect(screenBuffer, RAILTRACK_COLOR, stoprect)
                elif tile == TILE_RAILTRACK_BOTTOM_STOP:
                    pygame.draw.line(screenBuffer, RAILTRACK_COLOR, ((ci+1/2)*TILE_BLOCK_SIZE, ri*TILE_BLOCK_SIZE),
                                        ((ci+1/2) * TILE_BLOCK_SIZE, (ri+1/2)*TILE_BLOCK_SIZE),
                                        2)
                    stoprect = pygame.Rect(( (ci+1/2) * TILE_BLOCK_SIZE - 3, (ri+1/2) * TILE_BLOCK_SIZE - 3),
                                           (7, 7))
                    pygame.draw.rect(screenBuffer, RAILTRACK_COLOR, stoprect)
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
    def __drawLaserGuns():
        guns = LaserGun.guns
        for gun in guns:
            gunRect = pygame.Rect((gun.position[0], gun.position[1]), (gun.width, gun.height))
            pygame.draw.rect(screenBuffer, VGUN_COLOR, gunRect)

    @staticmethod
    def __drawLaser():
        try:
            lasers = Laser.lasers
            for laser in lasers:
                laserRect = pygame.Rect((laser.position[0], laser.position[1]), (laser.width, laser.height))
                pygame.draw.rect(screenBuffer, (255, 0, 0), laserRect)
        except Exception as e:
            return None

    @staticmethod
    def __drawRailSaws():
        try:
            railSaws = RailSaw.railSaws
            for railSaw in railSaws:
                pygame.draw.circle(screenBuffer, (0,0,0),
                                   (int(railSaw.centerPosition[0]), int(railSaw.centerPosition[1])), railSaw.radius)
                pygame.gfxdraw.circle(screenBuffer, int(railSaw.centerPosition[0]), int(railSaw.centerPosition[1]),
                                      railSaw.radius, (255, 255, 255))
        except Exception as e:
            return None

    @staticmethod
    def __drawEndingCredits():

        bouncer = Bouncer.bouncer

        if not bouncer.wonGame:
            return None

        Utils.dropShadowText(screenBuffer, "The End", 128, 200, 100, (255, 255, 255))


    @staticmethod
    def draw():

        Renderer.__drawBackground()
        Renderer.__drawPixels()

        Renderer.__drawEndingCredits()

        Renderer.__drawLaser()

        Renderer.__drawExitDoor()
        Renderer.__drawGlowExitDoor()
        Renderer.__drawExitDoorText()

        Renderer.__drawMovingPlatforms()

        Renderer.__drawRailSaws()
        Renderer.__drawBouncer()

        Renderer.__drawLevelTiles()

        Renderer.__drawLaserGuns()