import sys, pygame
import time, random
import pygame.gfxdraw

import numpy as np
import cv2

BACKGROUND_COLOR = (46, 52, 64)

TILE_BLOCK_SIZE = 25
TILE_COLOR = (3, 79, 132)
TILE_BORDER_COLOR = (0, 0, 0)

MOVING_TILE_COLOR = (255, 25, 25)
TILE_BORDER_WIDTH = 1
TILE_BORDER_RADIUS = 1

EXIT_DOOR_WIDTH = 25
EXIT_DOOR_HEIGHT = 50
EXIT_DOOR_BG_COLOR = 255, 255, 255
EXIT_DOOR_FRAME_BG_COLOR = 25, 25, 25

BLOCK_SIZE = 10
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
NUM_OF_BLOCKS_W = SCREEN_WIDTH / BLOCK_SIZE
NUM_OF_BLOCKS_H = SCREEN_HEIGHT / BLOCK_SIZE
DYING_DYE_INCREMENT = 10
BALL_H_SPEED = 5
BALL_RADIUS = 6
BOXING_DECREMENT = 3.5

DEATH_LINE_HEIGHT = SCREEN_HEIGHT * 1.25
BOUNCER_V_SPEED = 10.2

BITS_SPEED_RANGE = (-5, 5)
BITS_GRAVITY_DOWN = 0.15
BITS_COLOR = (3, 79, 132)
BITS_SIZE = (3,3)

BOUNCER_COLOR = (3, 79, 132)
BOUNCER_BORDER_COLOR = (25, 25, 25)

MOVING_PLATFORM_H_SPEED = 1.5

NUM_OF_TILES_PER_ROW = SCREEN_WIDTH / TILE_BLOCK_SIZE
NUM_OF_TILE_ROWS =  SCREEN_HEIGHT / TILE_BLOCK_SIZE

FPS = 30
fpsClock = pygame.time.Clock()

screenBuffer = pygame.surface.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

class Colors:
    WHITE_ISH = (246, 246, 246)
    YELLOW_ISH = (214, 198, 136)
    RED_ISH = (156, 60, 60)

class Utils:

    @staticmethod
    def getMiddlePosition():
        return [int((SCREEN_WIDTH / 2)), int((SCREEN_HEIGHT / 2))]

    @staticmethod
    def getRandomDirection():
        directions = ['right', 'left', 'down', 'up']
        initialDirection = directions[random.randint(0, 3)]
        return initialDirection

    @staticmethod
    def getBallDirection(sourceRect, previousCenterPosition, radius):
        if previousCenterPosition[0] + radius < sourceRect.x:
            return 'left'
        elif previousCenterPosition[0] - radius > sourceRect.x + sourceRect.width:
            return 'right'
        elif previousCenterPosition[1] + radius < sourceRect.y:
            return 'top'
        elif previousCenterPosition[1] - radius > sourceRect.y + sourceRect.height:
            return 'bottom'

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

class Sound:


    @staticmethod
    def init():
        Sound.SND_GAME_MUSIC = pygame.mixer.Sound("gamemusic.wav")

        Sound.SND_MAIN_MUSIC = pygame.mixer.Sound("main-music.mp3")
        Sound.SND_INTRO_TELEPORT = pygame.mixer.Sound("intro-teleport.mp3")
        Sound.SND_DEATH_SOUND = pygame.mixer.Sound("death-sound.mp3")

    @staticmethod
    def playIntroTeleport():
        pygame.mixer.Sound.play(Sound.SND_INTRO_TELEPORT)
        pygame.mixer.music.stop()

    @staticmethod
    def platDeathSound():
        pygame.mixer.Sound.play(Sound.SND_DEATH_SOUND)
        pygame.mixer.music.stop()


    @staticmethod
    def playMainMusic():
        pygame.mixer.Sound.play(Sound.SND_MAIN_MUSIC)
        pygame.mixer.music.stop()

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

class Pixels:
    def __init__(self, initialPos):
        self.initialPos = initialPos
        self.bits = []
        for i in range(16):
            xspeed = random.randint(BITS_SPEED_RANGE[0],BITS_SPEED_RANGE[1])
            yspeed = random.randint(BITS_SPEED_RANGE[0], BITS_SPEED_RANGE[1])
            self.bits.append([initialPos[0],initialPos[1], xspeed, yspeed])

    def update(self):
        for bit in self.bits:
            bit[3] += BITS_GRAVITY_DOWN

    @staticmethod
    def CreatePixels(initialPos):
        pixels = Pixels(initialPos)
        try:
            Pixels.pixelsList.append(pixels)
        except Exception as e:
            Pixels.pixelsList = []
            Pixels.pixelsList.append(pixels)

class Level:
    def __init__(self, filepath):
        self.loadFile(filepath)

    def loadFile(self, filepath):

        self.mapping = []
        f = open(filepath, "r")
        parseSector = ""

        self.movingPlatformsPosition = []

        for line in f:

            line = line.replace("\n", "")
            if line == "":
                continue

            if line == "[tiles]":
                parseSector = "tiles"
            elif line == "[bouncer_position]":
                parseSector = "bouncer_position"
            elif line == "[exitdoor_position]":
                parseSector = "exitdoor_position"
            elif line == "[next_map]":
                parseSector = "next_map"
            elif line == "[moving_platforms]":
                parseSector = "moving_platforms"

            if line.find("[") != -1 and line.find("]") != -1:
                continue

            if parseSector == "tiles":
                dataTokens = line.split(",")
                datastream = []
                for data in dataTokens:
                    datastream.append(int(data))
                self.mapping.append(datastream)

            elif parseSector == "bouncer_position":
                dataTokens = line.split(",")
                self.bouncerPosition = (int(dataTokens[0]), int(dataTokens[1]))

            elif parseSector == "exitdoor_position":
                dataTokens = line.split(",")
                self.exitdoorPosition = (int(dataTokens[0]), int(dataTokens[1]))

            elif parseSector == "next_map":
                self.nextLevel = line

            elif parseSector == "moving_platforms":
                dataTokens = line.split(",")
                self.movingPlatformsPosition.append([int(dataTokens[0]), int(dataTokens[1])])

class MovingPlatform:
    def __init__(self, pos):
        self.position = [pos[0], pos[1]]
        self.width = TILE_BLOCK_SIZE
        self.height = TILE_BLOCK_SIZE / 2
        directions = ["left","right"]
        self.hdirection = directions[random.randint(0,1)]

    @staticmethod
    def CreateMovingPlatforms():
        MovingPlatform.platforms = []
        platforms = MovingPlatform.platforms
        movingPlatformPositions = Level.currentLevel.movingPlatformsPosition
        for m in movingPlatformPositions:
            platforms.append(MovingPlatform(m))

    def isColliding(self, rect):
        if self.position[0] + self.width >= rect.x and \
            self.position[1] + self.height >= rect.y and \
            self.position[0] <= rect.x + rect.width and \
            self.position[1] <= rect.y + rect.height:
            return True
        return False

    def update(self):
        if self.hdirection == 'left':
            self.position[0] -= MOVING_PLATFORM_H_SPEED
        elif self.hdirection == 'right':
            self.position[0] += MOVING_PLATFORM_H_SPEED

class ExitDoor:
    def __init__(self, pos, width, height):
        self.position = [pos[0],pos[1]]
        self.width = width
        self.height = height

    def setPosition(self, pos):
        self.position = [pos[0], pos[1]]

class Bouncer:
    def __init__(self, pos, radius):
        self.position = [pos[0],pos[1]]
        self.previousPosition = [0,0]
        self.speed = [0, 0]
        self.radius = radius
        self.direction = 'none'
        self.boxingRadius = radius - BOXING_DECREMENT

    def update(self):
        self.speed[1] += 0.98
        self.previousPosition[0] = self.position[0]
        self.previousPosition[1] = self.position[1]
        self.position[1] += self.speed[1]

        if self.direction == 'left':
            self.position[0] -= BALL_H_SPEED
        elif self.direction == 'right':
            self.position[0] += BALL_H_SPEED

    def isColliding(self, rect):
        if self.position[0] + self.boxingRadius >= rect.x and \
            self.position[1] + self.boxingRadius >= rect.y and \
            self.position[0] - self.boxingRadius <= rect.x + rect.width and \
            self.position[1] - self.boxingRadius <= rect.y + rect.height:
            return True
        return False

    def setPosition(self, pos):
        self.position = [pos[0], pos[1]]

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
    def draw():

        Renderer.__drawBackground()
        Renderer.__drawExitDoor()
        Renderer.__drawBouncer()
        Renderer.__drawGlowExitDoor()
        Renderer.__drawExitDoorText()
        Renderer.__drawLevelTiles()
        Renderer.__drawMovingPlatforms()
        Renderer.__drawPixels()


class GameWorld:

    @staticmethod
    def init():

        Sound.init()

        Level.currentLevel = Level("level1.txt")

        bouncer = Bouncer(Utils.getMiddlePosition(), BALL_RADIUS)
        Bouncer.bouncer = bouncer

        exitDoor = ExitDoor(Level.currentLevel.exitdoorPosition, EXIT_DOOR_WIDTH, EXIT_DOOR_HEIGHT)
        ExitDoor.exitDoor = exitDoor

        bouncer.setPosition(Level.currentLevel.bouncerPosition)

        MovingPlatform.CreateMovingPlatforms()

        Sound.playMainMusic()
        Sound.playIntroTeleport()

    @staticmethod
    def reset():
        bouncer = Bouncer.bouncer
        bouncer.setPosition(Level.currentLevel.bouncerPosition)
        bouncer.speed = [0, 0]
        bouncer.direction = 'none'


    @staticmethod
    def onNextLevel():
        exitDoor = ExitDoor(Level.currentLevel.exitdoorPosition, EXIT_DOOR_WIDTH, EXIT_DOOR_HEIGHT)
        ExitDoor.exitDoor = exitDoor
        MovingPlatform.CreateMovingPlatforms()

    @staticmethod
    def death():
        Sound.platDeathSound()
        GameWorld.reset()

    @staticmethod
    def deathExplode():
        bouncer = Bouncer.bouncer
        Pixels.CreatePixels(bouncer.position)
        GameWorld.death()

    @staticmethod
    def quit():
        return None

    @staticmethod
    def __update_MovingPlatforms():
        for platform in MovingPlatform.platforms:
            platform.update()
            cl = Level.currentLevel
            ri = 0
            for tileRow in cl.mapping:
                ci = 0
                for tile in tileRow:
                    if tile == 1:
                        tilerect = pygame.Rect((ci * TILE_BLOCK_SIZE, ri * TILE_BLOCK_SIZE),
                                               (TILE_BLOCK_SIZE, TILE_BLOCK_SIZE))
                        if platform.isColliding(tilerect):
                            if platform.hdirection == 'left':
                                platform.hdirection = 'right'
                                platform.position[0] = tilerect.x + tilerect.width + 1
                            elif platform.hdirection == 'right':
                                platform.hdirection = 'left'
                                platform.position[0] = tilerect.x - platform.width - 1
                    ci += 1
                ri += 1


    @staticmethod
    def __update_BouncerExitDoorCheck():
        exitDoor = ExitDoor.exitDoor
        bouncer = Bouncer.bouncer
        exitDoorRect = pygame.Rect((exitDoor.position[0],exitDoor.position[1]), (exitDoor.width, exitDoor.height))
        if bouncer.isColliding(exitDoorRect):
            Level.currentLevel.loadFile(Level.currentLevel.nextLevel)
            GameWorld.reset()
            GameWorld.onNextLevel()

    @staticmethod
    def __update_BouncerBoundariesCheck():
        bouncer = Bouncer.bouncer
        if bouncer.position[0] - bouncer.boxingRadius <= 0:
            bouncer.position[0] = bouncer.boxingRadius
        elif bouncer.position[0] + bouncer.boxingRadius >= SCREEN_WIDTH:
            bouncer.position[0] = SCREEN_WIDTH - bouncer.boxingRadius
        elif bouncer.position[1] >= DEATH_LINE_HEIGHT:
            GameWorld.death()

    @staticmethod
    def __update_BoucerCheckTiles():
        bouncer = Bouncer.bouncer
        cl = Level.currentLevel
        ri = 0
        for tileRow in cl.mapping:
            ci = 0
            for tile in tileRow:
                tilerect = pygame.Rect((ci * TILE_BLOCK_SIZE, ri * TILE_BLOCK_SIZE),
                                       (TILE_BLOCK_SIZE, TILE_BLOCK_SIZE))

                if bouncer.isColliding(tilerect):
                    if tile == 1:
                        ballDir = Utils.getBallDirection(tilerect, bouncer.previousPosition, bouncer.boxingRadius)
                        if ballDir == 'top':
                            bouncer.speed[1] = -BOUNCER_V_SPEED
                            bouncer.position[1] = ri * TILE_BLOCK_SIZE - bouncer.radius - 1
                        elif ballDir == 'right':
                            bouncer.position[0] = ci * TILE_BLOCK_SIZE + TILE_BLOCK_SIZE + bouncer.boxingRadius + 1
                        elif ballDir == 'left':
                            bouncer.position[0] = ci * TILE_BLOCK_SIZE - bouncer.radius - 1
                        elif ballDir == 'bottom':
                            bouncer.position[1] = ri * TILE_BLOCK_SIZE + TILE_BLOCK_SIZE + bouncer.boxingRadius + 1
                            bouncer.speed[1] = 0
                    elif tile == 2:
                        GameWorld.deathExplode()
                ci += 1
            ri += 1

    @staticmethod
    def __update_BouncerMovingPlatforms():
        bouncer = Bouncer.bouncer
        for platform in MovingPlatform.platforms:
            platformRect = pygame.Rect((platform.position[0],platform.position[1]), (platform.width, platform.height))
            if bouncer.isColliding(platformRect):
                bouncer.speed[1] = -BOUNCER_V_SPEED
                bouncer.position[1] = platform.position[1] - bouncer.radius - 1


    @staticmethod
    def __update_Pixels():
        try:
            pixelsList = Pixels.pixelsList
            for pixels in pixelsList:
                for bit in pixels.bits:
                    bit[0] += bit[2]
                    bit[1] += bit[3]
                    bit[3] += BITS_GRAVITY_DOWN
                    if bit[1] > SCREEN_HEIGHT:
                        pixels.bits.remove(bit)
                        if len(pixels.bits) == 0:
                            pixelsList.remove(pixels)
        except Exception as e:
            return None

    @staticmethod
    def update():

        bouncer = Bouncer.bouncer
        bouncer.update()

        GameWorld.__update_BouncerBoundariesCheck()
        GameWorld.__update_BouncerExitDoorCheck()
        GameWorld.__update_BoucerCheckTiles()
        GameWorld.__update_MovingPlatforms()
        GameWorld.__update_BouncerMovingPlatforms()
        GameWorld.__update_Pixels()

if __name__ == '__main__':


    pygame.init()
    GameWorld.init()

    size = width, height = SCREEN_WIDTH, SCREEN_HEIGHT

    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Bouncer")

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        keys = pygame.key.get_pressed()
        Controls.key_pressed(keys)

        GameWorld.update()
        Renderer.draw()
        pygame.Surface.blit(screen, screenBuffer, (0,0))
        pygame.display.flip()

        fpsClock.tick(FPS)

    GameWorld.quit()