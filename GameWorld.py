from LevelLoader import Level
from GameObjects import ExitDoor, Bouncer, MovingPlatform
from Utility import Utils
from GameConstants import *
from Sound import *
from Timer import *
from Controls import *
from Renderer import *

class GameWorld:

    @staticmethod
    def init():

        Sound.init()

        Level.currentLevel = Level("level6.txt")

        bouncer = Bouncer(Utils.getMiddlePosition(), BALL_RADIUS)
        Bouncer.bouncer = bouncer

        exitDoor = ExitDoor(Level.currentLevel.exitdoorPosition, EXIT_DOOR_WIDTH, EXIT_DOOR_HEIGHT)
        ExitDoor.exitDoor = exitDoor

        bouncer.setPosition(Level.currentLevel.bouncerPosition)

        MovingPlatform.CreateMovingPlatforms()
        LaserVGun.CreateLaserVGuns()

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
        Timer.quit()
        LaserV.quit()
        exitDoor = ExitDoor(Level.currentLevel.exitdoorPosition, EXIT_DOOR_WIDTH, EXIT_DOOR_HEIGHT)
        ExitDoor.exitDoor = exitDoor
        MovingPlatform.CreateMovingPlatforms()
        LaserVGun.CreateLaserVGuns()


    @staticmethod
    def death():
        GameWorld.reset()

    @staticmethod
    def deathExplode():
        bouncer = Bouncer.bouncer
        Pixels.CreatePixels(bouncer.position)
        GameWorld.death()
        Sound.platDeathSound()

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
                            if platform.direction == 'left':
                                platform.direction = 'right'
                                platform.position[0] = tilerect.x + tilerect.width + 1
                            elif platform.direction == 'right':
                                platform.direction = 'left'
                                platform.position[0] = tilerect.x - platform.width - 1
                            elif platform.direction == 'up':
                                platform.direction = 'down'
                                platform.position[1] = tilerect.y + tilerect.height + 1
                            elif platform.direction == 'down':
                                platform.direction = 'up'
                                platform.position[1] = tilerect.y - platform.height - 1
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
                    elif tile == 3:
                        bouncer.position[1] = ri * TILE_BLOCK_SIZE - bouncer.radius - 1
                        bouncer.speed[1] = -BOUNCER_V_SPEED*1.6
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
    def __update_LaserRemove(laser):
        try:
            lasersVList = LaserV.lasers
            laserVGun = laser.parent
            lasersVList.remove(laser)
            laserVGun.triggerShootLaserEvent()
        except Exception as e:
            return None

    @staticmethod
    def __update_LaserV():
        try:
            lasersVList = LaserV.lasers
            bouncer = Bouncer.bouncer
            for laser in lasersVList:
                laserRect = pygame.Rect((laser.position[0], laser.position[1]), (laser.width, laser.height))
                if not Utils.collidesWithTile(laserRect):
                    laser.update()
                elif not laser.hitTile:
                    laser.hitTile = True
                    Timer.SetTimerEvent(laser.parent.resetTime, GameWorld.__update_LaserRemove, laser)
                if bouncer.isColliding(laserRect):
                    GameWorld.deathExplode()
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

        GameWorld.__update_LaserV()
        GameWorld.__update_Pixels()