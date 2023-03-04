import sys, pygame
import time, random
import pygame.gfxdraw

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

BOUNCER_COLOR = (3, 79, 132)
BOUNCER_BORDER_COLOR = (25, 25, 25)


NUM_OF_TILES_PER_ROW = SCREEN_WIDTH / TILE_BLOCK_SIZE
NUM_OF_TILE_ROWS =  SCREEN_HEIGHT / TILE_BLOCK_SIZE

FPS = 30
fpsClock = pygame.time.Clock()

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


class Sound:


    @staticmethod
    def init():
        Sound.SND_GAME_MUSIC = pygame.mixer.Sound("gamemusic.wav")

        Sound.SND_MAIN_MUSIC = pygame.mixer.Sound("main-music.mp3")
        Sound.SND_INTRO_TELEPORT = pygame.mixer.Sound("intro-teleport.mp3")

    @staticmethod
    def playIntroTeleport():
        pygame.mixer.Sound.play(Sound.SND_INTRO_TELEPORT)
        pygame.mixer.music.stop()

    @staticmethod
    def playMainMusic():
        pygame.mixer.Sound.play(Sound.SND_MAIN_MUSIC)
        pygame.mixer.music.stop()

class Level:
    def __init__(self, filepath):
        self.loadFile(filepath)

    def loadFile(self, filepath):
        self.mapping = []
        f = open(filepath, "r")
        parseSector = ""
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
        screen.fill(BACKGROUND_COLOR)

    @staticmethod
    def __drawBouncer():
        bouncer = Bouncer.bouncer
        pygame.draw.circle(screen, BOUNCER_COLOR, (int(bouncer.position[0]), int(bouncer.position[1])), bouncer.radius)
        pygame.gfxdraw.circle(screen, int(bouncer.position[0]), int(bouncer.position[1]), bouncer.radius, BOUNCER_BORDER_COLOR)

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
                    pygame.draw.rect(screen, TILE_COLOR, tilerect)
                    pygame.draw.rect(screen, TILE_BORDER_COLOR, tilerect, TILE_BORDER_WIDTH, TILE_BORDER_RADIUS)
                    pygame.gfxdraw.rectangle(screen, tilerect, TILE_BORDER_COLOR)
                ci += 1
            ri += 1

    @staticmethod
    def __drawExitDoor():
        exitDoor = ExitDoor.exitDoor
        exitDoorRect = pygame.Rect((exitDoor.position[0], exitDoor.position[1]), (exitDoor.width, exitDoor.height))
        pygame.draw.rect(screen, EXIT_DOOR_BG_COLOR, exitDoorRect)

        font = pygame.font.SysFont(None, 24)
        img = font.render('Exit', True, (255, 0, 0))
        screen.blit(img, (exitDoor.position[0]-4, exitDoor.position[1]-15))


    @staticmethod
    def draw():

        Renderer.__drawBackground()
        Renderer.__drawExitDoor()
        Renderer.__drawBouncer()
        Renderer.__drawLevelTiles()


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

        Sound.playMainMusic()
        Sound.playIntroTeleport()

    @staticmethod
    def reset():
        bouncer = Bouncer.bouncer
        bouncer.setPosition(Level.currentLevel.bouncerPosition)
        bouncer.speed = [0, 0]
        bouncer.direction = 'none'
        exitDoor = ExitDoor(Level.currentLevel.exitdoorPosition, EXIT_DOOR_WIDTH, EXIT_DOOR_HEIGHT)
        ExitDoor.exitDoor = exitDoor
        Sound.playIntroTeleport()

    @staticmethod
    def quit():
        return None

    @staticmethod
    def __update_BouncerExitDoorCheck():
        exitDoor = ExitDoor.exitDoor
        bouncer = Bouncer.bouncer
        exitDoorRect = pygame.Rect((exitDoor.position[0],exitDoor.position[1]), (exitDoor.width, exitDoor.height))
        if bouncer.isColliding(exitDoorRect):
            Level.currentLevel.loadFile(Level.currentLevel.nextLevel)
            GameWorld.reset()

    @staticmethod
    def __update_BouncerBoundariesCheck():
        bouncer = Bouncer.bouncer
        if bouncer.position[0] - bouncer.boxingRadius <= 0:
            bouncer.position[0] = bouncer.boxingRadius
        elif bouncer.position[0] + bouncer.boxingRadius >= SCREEN_WIDTH:
            bouncer.position[0] = SCREEN_WIDTH - bouncer.boxingRadius
        elif bouncer.position[1] >= DEATH_LINE_HEIGHT:
            GameWorld.reset()

    @staticmethod
    def __update_BoucerCheckTiles():
        bouncer = Bouncer.bouncer
        cl = Level.currentLevel
        ri = 0
        for tileRow in cl.mapping:
            ci = 0
            for tile in tileRow:
                if tile == 1:
                    tilerect = pygame.Rect((ci * TILE_BLOCK_SIZE, ri * TILE_BLOCK_SIZE),
                                           (TILE_BLOCK_SIZE, TILE_BLOCK_SIZE))
                    if bouncer.isColliding(tilerect):
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
                ci += 1
            ri += 1


    @staticmethod
    def update():

        bouncer = Bouncer.bouncer
        bouncer.update()

        GameWorld.__update_BouncerBoundariesCheck()
        GameWorld.__update_BouncerExitDoorCheck()
        GameWorld.__update_BoucerCheckTiles()

if __name__ == '__main__':


    pygame.init()
    GameWorld.init()

    size = width, height = SCREEN_WIDTH, SCREEN_HEIGHT

    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Bouncer")

    bouncer = Bouncer.bouncer

    prev_time = time.time()


    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()


        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            bouncer.direction = 'left'
        elif keys[pygame.K_RIGHT]:
            bouncer.direction = 'right'
        else:
            bouncer.direction = 'none'


        pygame.display.flip()
        GameWorld.update()
        Renderer.draw()

        fpsClock.tick(FPS)

        GameWorld.quit()