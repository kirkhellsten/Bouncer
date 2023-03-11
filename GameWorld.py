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

        Level.currentLevel = Level("level36.txt")

        bouncer = Bouncer(Utils.getMiddlePosition(), BALL_RADIUS)
        Bouncer.bouncer = bouncer

        exitDoor = ExitDoor(Level.currentLevel.exitdoorPosition, EXIT_DOOR_WIDTH, EXIT_DOOR_HEIGHT)
        ExitDoor.exitDoor = exitDoor

        bouncer.setPosition(Level.currentLevel.bouncerPosition)

        MovingPlatform.CreateMovingPlatforms()
        LaserGun.CreateLaserGuns()

        Sound.playMainMusic()

        GameWorld.isEnd = False
        GameWorld.finished = False

    @staticmethod
    def reset():
        bouncer = Bouncer.bouncer
        bouncer.setPosition(Level.currentLevel.bouncerPosition)
        bouncer.setPreviousPosition(Level.currentLevel.bouncerPosition)
        bouncer.speed = [0, 0]
        bouncer.direction = 'none'
        bouncer.gravityDirection = 'down'

    @staticmethod
    def onNextLevel():
        Timer.quit()
        Laser.quit()

        exitDoor = ExitDoor(Level.currentLevel.exitdoorPosition, EXIT_DOOR_WIDTH, EXIT_DOOR_HEIGHT)
        ExitDoor.exitDoor = exitDoor
        MovingPlatform.CreateMovingPlatforms()
        LaserGun.CreateLaserGuns()

        Sound.playMainMusic()

    @staticmethod
    def __finishedCallback():
        GameWorld.finished = True

    @staticmethod
    def endGame():

        if GameWorld.isEnd:
            return None

        bouncer = Bouncer.bouncer
        bouncer.visible = False
        GameWorld.isEnd = True
        bouncer.wonGame = True
        Sound.playGameEnding()

        Timer.SetTimerEvent(55000, GameWorld.__finishedCallback)

    @staticmethod
    def death():
        GameWorld.reset()

    @staticmethod
    def deathExplode():
        bouncer = Bouncer.bouncer
        Pixels.CreatePixels(bouncer.centerPosition)
        GameWorld.death()
        Sound.playDeathSound()

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
                    if tile == TILE_NORMAL or tile == TILE_RED or tile == TILE_GREEN:
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

            if Level.currentLevel.lastlevel and not GameWorld.isEnd:
                GameWorld.endGame()
            elif not GameWorld.isEnd:
                Level.currentLevel.loadLevel(Level.currentLevel.nextLevel)
                GameWorld.onNextLevel()
                GameWorld.reset()

    @staticmethod
    def __update_BouncerBoundariesCheck():
        bouncer = Bouncer.bouncer
        if bouncer.centerPosition[0] - bouncer.boxingRadius <= 0:
            bouncer.centerPosition[0] = bouncer.boxingRadius
        elif bouncer.centerPosition[0] + bouncer.boxingRadius >= SCREEN_WIDTH:
            bouncer.centerPosition[0] = SCREEN_WIDTH - bouncer.boxingRadius
        elif bouncer.centerPosition[1] >= DEATH_LINE_HEIGHT:
            GameWorld.death()

    @staticmethod
    def __GetListOfCollidingTiles():

        """
            Get List of colliding tiles
        """
        bouncer = Bouncer.bouncer
        cl = Level.currentLevel

        collidingTilesList = []

        for ri in range(len(cl.mapping)):
            for ci in range(len(cl.mapping[ri])):

                tile = cl.mapping[ri][ci]

                if tile == 0:
                    continue

                tilerect = pygame.Rect((ci * TILE_BLOCK_SIZE, ri * TILE_BLOCK_SIZE),
                                       (TILE_BLOCK_SIZE, TILE_BLOCK_SIZE))

                if bouncer.isCollidingWithObj(tilerect):
                    collidingTilesList.append((ri,ci,tile,tilerect))

        return collidingTilesList

    @staticmethod
    def __update_BoucerCheckTiles():

        collidingTilesList = GameWorld.__GetListOfCollidingTiles()

        """
            Go through colliding tiles list
        """
        bouncer = Bouncer.bouncer

        for tileData in collidingTilesList:

            tilerect = tileData[3]
            tile = tileData[2]

            ballDir = bouncer.getCollisionDirection(tilerect)

            if tile in TILES_WITH_COLLISIONS:

                bouncer.handleBallCollision(tilerect)

                if ballDir in ['left', 'right']:
                    bouncer.speed[0] = 0

                if ballDir == 'bottom':
                    bouncer.speed[1] = 0

                """
                    Handle Tile Bouncer via top and down based 
                    on tile type and gravity direction
                """
                if ballDir == 'top' and bouncer.gravityDirection == 'down':

                    if tile == TILE_NORMAL:
                        bouncer.speed[1] = -BOUNCER_V_SPEED
                    elif tile == TILE_GREEN:
                        if abs(bouncer.speed[1]) > BOUNCER_V_SPEED * BOUNCER_V_FACTOR_BIG_BOUNCE:
                            bouncer.speed[1] = -abs(bouncer.speed[1])
                        else:
                            bouncer.speed[1] = -BOUNCER_V_SPEED * BOUNCER_V_FACTOR_BIG_BOUNCE
                    elif tile == TILE_RED:
                        bouncer.speed[1] = -BOUNCER_V_SPEED * BOUNCER_V_FACTOR_SMALL_BOUNCE
                    elif tile == TILE_BLACK:
                        bouncer.changeGravityDirection()

                elif ballDir == 'bottom' and bouncer.gravityDirection == 'up':

                    if tile == TILE_NORMAL:
                        bouncer.speed[1] = BOUNCER_V_SPEED
                    elif tile == TILE_GREEN:
                        if abs(bouncer.speed[1]) > BOUNCER_V_SPEED * BOUNCER_V_FACTOR_BIG_BOUNCE:
                            bouncer.speed[1] = abs(bouncer.speed[1])
                        else:
                            bouncer.speed[1] = BOUNCER_V_SPEED * BOUNCER_V_FACTOR_BIG_BOUNCE
                    elif tile == TILE_RED:
                        bouncer.speed[1] = BOUNCER_V_SPEED * BOUNCER_V_FACTOR_SMALL_BOUNCE
                    elif tile == TILE_BLACK:
                        bouncer.changeGravityDirection()

            elif tile in TILES_DEATH_COLLISIONS:
                GameWorld.deathExplode()
                break

    @staticmethod
    def __update_BouncerMovingPlatforms():

        """
            Go through moving platforms and detect collision with bouncer
        """
        bouncer = Bouncer.bouncer
        for platform in MovingPlatform.platforms:

            platformRect = pygame.Rect((platform.position[0],platform.position[1]), (platform.width, platform.height))

            if bouncer.isCollidingWithObj(platformRect):

                """
                    Make Bouncer bounce off moving platforms
                """
                bouncer.handleBallCollision(platformRect)

                ballDir = bouncer.getCollisionDirection(platformRect)

                if bouncer.gravityDirection == 'down' and ballDir == 'top':
                    bouncer.speed[1] = -BOUNCER_V_SPEED
                elif bouncer.gravityDirection == 'up' and ballDir == 'bottom':
                    bouncer.speed[1] = BOUNCER_V_SPEED
                elif bouncer.gravityDirection == 'down' and ballDir == 'bottom' or \
                     bouncer.gravityDirection == 'up' and ballDir == 'top':
                    bouncer.speed[1] = 0



    @staticmethod
    def __update_BouncerLaserGuns():

        """
            Go through laser guns and detect collision with bouncer
        """
        bouncer = Bouncer.bouncer
        for gun in LaserGun.guns:

            gunRect = pygame.Rect((gun.position[0],gun.position[1]), (gun.width, gun.height))

            if bouncer.isCollidingWithObj(gunRect):

                """
                    Make Bouncer bounce off moving platforms
                """
                bouncer.handleBallCollision(gunRect)

                ballDir = bouncer.getCollisionDirection(gunRect)

                if bouncer.gravityDirection == 'down' and ballDir == 'top':
                    bouncer.speed[1] = -BOUNCER_V_SPEED
                elif bouncer.gravityDirection == 'up' and ballDir == 'bottom':
                    bouncer.speed[1] = BOUNCER_V_SPEED

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
            lasersList = Laser.lasers
            laserGun = laser.parent
            lasersList.remove(laser)
            laserGun.triggerShootLaserEvent()
        except Exception as e:
            return None

    @staticmethod
    def __update_Laser():
        try:
            lasersList = Laser.lasers
            bouncer = Bouncer.bouncer
            for laser in lasersList:
                laserRect = pygame.Rect((laser.position[0], laser.position[1]), (laser.width, laser.height))
                if not Utils.collidesWithTile(laserRect):
                    laser.update()
                elif not laser.hitTile:
                    laser.hitTile = True
                    Timer.SetTimerEvent(laser.parent.resetTime, GameWorld.__update_LaserRemove, laser)
                if bouncer.isCollidingWithObj(laserRect):
                    GameWorld.deathExplode()
        except Exception as e:
            return None

    @staticmethod
    def update():

        bouncer = Bouncer.bouncer
        bouncer.update()

        GameWorld.__update_MovingPlatforms()

        GameWorld.__update_BouncerBoundariesCheck()
        GameWorld.__update_BouncerExitDoorCheck()

        GameWorld.__update_BouncerMovingPlatforms()
        GameWorld.__update_BouncerLaserGuns()

        GameWorld.__update_BoucerCheckTiles()


        GameWorld.__update_Laser()
        GameWorld.__update_Pixels()

