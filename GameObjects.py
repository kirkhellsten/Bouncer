from GameConstants import *
from LevelLoader import Level
from Sound import *
from Timer import *
import random
from Utility import Utils

class ExitDoor:
    def __init__(self, pos, width, height):
        self.position = [pos[0],pos[1]]
        self.width = width
        self.height = height

    def setPosition(self, pos):
        self.position = [pos[0], pos[1]]

class Bouncer:
    def __init__(self, pos, radius):
        self.centerPosition = [pos[0],pos[1]]
        self.previousPosition = [pos[0],pos[1]]
        self.speed = [0, 0]
        self.radius = radius
        self.direction = 'none'
        self.boxingRadius = radius - BOXING_DECREMENT
        self.gravityDirection = 'down'
        self.visible = True
        self.wonGame = False

    def update(self):

        """
            Apply Gravity based on direction
        """
        if self.gravityDirection == 'up':
            self.speed[1] += -GRAVITY_SPEED
        elif self.gravityDirection == 'down':
            self.speed[1] += GRAVITY_SPEED

        self.previousPosition[0] = self.centerPosition[0]
        self.previousPosition[1] = self.centerPosition[1]
        self.centerPosition[1] += self.speed[1]


        if self.direction == 'left':
            self.centerPosition[0] -= BOUNCER_H_SPEED
        elif self.direction == 'right':
            self.centerPosition[0] += BOUNCER_H_SPEED


    def changeGravityDirection(self):

        if self.gravityDirection == 'down':
            self.gravityDirection = 'up'
        elif self.gravityDirection == 'up':
            self.gravityDirection = 'down'

        self.speed[1] = 0

    """
        Fall back collision detection. More primitive than isCollidingWithObj
    """
    def isColliding(self, rect):
        if self.centerPosition[0] + self.boxingRadius >= rect.x and \
            self.centerPosition[1] + self.boxingRadius >= rect.y and \
            self.centerPosition[0] - self.boxingRadius <= rect.x + rect.width and \
            self.centerPosition[1] - self.boxingRadius <= rect.y + rect.height:
            return True
        return False

    """
        More advance collision detection. Fall back to isColliding
        if this detection doesn't work
    """
    def isCollidingWithObj(self, objRect):

        if self.centerPosition[0] + self.boxingRadius >= objRect.x and \
            self.centerPosition[0] + self.boxingRadius <= objRect.x + objRect.width:

            if self.centerPosition[1] + self.radius > objRect.y and \
                self.previousPosition[1] + self.radius < objRect.y or \
                self.centerPosition[1] - self.radius < objRect.y + objRect.height and \
                self.previousPosition[1] - self.radius > objRect.y + objRect.height:
                return True

        return self.isColliding(objRect)


    """
        Special Collision getters for Bouncer
        Used to aid in collisions with rect sources
    """
    def getRightPositionForCollision(self, rectSource):
        return rectSource.x + rectSource.width + self.boxingRadius + 1

    def getLeftPositionForCollision(self, rectSource):
        return rectSource.x - self.boxingRadius - 1

    def getBottomPositionForCollision(self, rectSource):
        return rectSource.y + rectSource.height + self.radius + 1

    def getTopPositionForCollision(self, rectSource):
        return rectSource.y - self.radius - 1

    """
        Special method to handle ball Collisions given rect
        Call right after collision is detected
    """
    def handleBallCollision(self, rectSource):
        ballDir = self.getCollisionDirection(rectSource)
        if ballDir == 'right':
            self.centerPosition[0] = self.getRightPositionForCollision(rectSource)
        elif ballDir == 'left':
            self.centerPosition[0] = self.getLeftPositionForCollision(rectSource)
        elif ballDir == 'top':
            self.centerPosition[1] = self.getTopPositionForCollision(rectSource)
        elif ballDir == 'bottom':
            self.centerPosition[1] = self.getBottomPositionForCollision(rectSource)

    """
        Special method to get direction ball collided with rectSource
    """
    def getCollisionDirection(self, tilerect):
        if self.previousPosition[0] + self.boxingRadius < tilerect.x:
            return 'left'
        elif self.previousPosition[0] - self.boxingRadius > tilerect.x + tilerect.width:
            return 'right'
        elif self.previousPosition[1] + self.boxingRadius < tilerect.y:
            return 'top'
        elif self.previousPosition[1] - self.boxingRadius > tilerect.y + tilerect.height:
            return 'bottom'
        else:
            return 'none'

    def setPosition(self, pos):
        self.previousPosition = [self.centerPosition[0],self.centerPosition[1]]
        self.centerPosition = [pos[0], pos[1]]

    def setPreviousPosition(self, pos):
        self.previousPosition = [pos[0],pos[1]]

class MovingPlatform:
    def __init__(self, pos, direction):
        self.position = [pos[0], pos[1]]
        self.width = TILE_BLOCK_SIZE
        self.height = TILE_BLOCK_SIZE / 2
        self.direction = direction


    @staticmethod
    def CreateMovingPlatforms():
        MovingPlatform.platforms = []
        platforms = MovingPlatform.platforms
        data = Level.currentLevel.movingPlatformData
        for m in data:
            position = [m[0],m[1]]
            platforms.append(MovingPlatform(position, m[2]))


    def isColliding(self, rect):
        if self.position[0] + self.width - GENERAL_BOXING_DECREMENT >= rect.x and \
            self.position[1] + self.height - GENERAL_BOXING_DECREMENT >= rect.y and \
            self.position[0] + GENERAL_BOXING_DECREMENT <= rect.x + rect.width and \
            self.position[1] + GENERAL_BOXING_DECREMENT <= rect.y + rect.height:
            return True
        return False


    def update(self):
        if self.direction == 'left':
            self.position[0] -= MOVING_PLATFORM_H_SPEED
        elif self.direction == 'right':
            self.position[0] += MOVING_PLATFORM_H_SPEED
        elif self.direction == 'up':
            self.position[1] -= MOVING_PLATFORM_V_SPEED
        elif self.direction == 'down':
            self.position[1] += MOVING_PLATFORM_V_SPEED


class Laser:
    def __init__(self, pos, parent):
        self.position = [pos[0],pos[1]]
        self.hitTile = False
        self.direction = parent.direction
        self.parent = parent

        if parent.direction in ['up','down']:
            self.width = LASERV_WIDTH
            self.height = LASERV_HEIGHT
        elif parent.direction in ['left','right']:
            self.height = LASERV_WIDTH
            self.width = LASERV_HEIGHT

    def update(self):

        if self.direction == 'down':
            self.height += VGUN_LASER_SPEED
        elif self.direction == 'up':
            self.height += VGUN_LASER_SPEED
            self.position[1] -= VGUN_LASER_SPEED
        elif self.direction == 'left':
            self.width += VGUN_LASER_SPEED
            self.position[0] -= VGUN_LASER_SPEED
        elif self.direction == 'right':
            self.width += VGUN_LASER_SPEED


    @staticmethod
    def quit():
        Laser.lasers = []

    @staticmethod
    def CreateLaser(pos, parent):
        try:
            laser = Laser(pos, parent)
            Laser.lasers.append(laser)
        except Exception as e:
            Laser.lasers = []
            Laser.lasers.append(laser)

class LaserGun:
    def __init__(self, pos, loopTime, resetTime, direction):
        self.position = [pos[0], pos[1]]

        if direction == 'up' or direction == 'down':
            self.width = VGUN_WIDTH
            self.height = VGUN_HEIGHT
        elif direction == 'left' or direction == 'right':
            self.height = VGUN_WIDTH
            self.width = VGUN_HEIGHT

        self.loopTime = loopTime
        self.resetTime = resetTime
        self.direction = direction
        self.triggerShootLaserEvent()

    def triggerShootLaserEvent(self):
        Timer.SetTimerEvent(self.loopTime, self.shootLaser)

    def shootLaser(self):
        pos = [self.position[0],self.position[1]]
        pos[0] += self.width / 2
        pos[1] += self.height / 2
        Laser.CreateLaser(pos, self)
        Sound.playLaserGunSound()

    @staticmethod
    def CreateLaserGuns():

        laserGunData = Level.currentLevel.laserGunData

        LaserGun.guns = []
        guns = LaserGun.guns

        for i in range(len(laserGunData)):
            position = [laserGunData[i][0], laserGunData[i][1]]
            loopTime = laserGunData[i][2]
            resetTime = laserGunData[i][3]
            direction = laserGunData[i][4]
            laserGun = LaserGun(position, loopTime, resetTime, direction)
            guns.append(laserGun)

class Pixels:
    def __init__(self, initialPos):
        self.initialPos = initialPos
        self.bits = []
        for i in range(BITS_NUMBER):
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
