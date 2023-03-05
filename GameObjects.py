from GameConstants import *
from LevelLoader import Level
from Sound import *
from Timer import *
import random

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


class LaserV:
    def __init__(self, pos, parent):
        self.position = [pos[0],pos[1]]
        self.width = LASERV_WIDTH
        self.height = LASERV_HEIGHT
        self.hitTile = False
        self.parent = parent

    def update(self):
        self.height += VGUN_LASER_SPEED

    @staticmethod
    def quit():
        LaserV.lasers = []

    @staticmethod
    def CreateLaserV(pos, parent):
        try:
            laser = LaserV(pos, parent)
            LaserV.lasers.append(laser)
        except Exception as e:
            LaserV.lasers = []
            LaserV.lasers.append(laser)

class LaserVGun:
    def __init__(self, pos, loopTime, resetTime):
        self.position = [pos[0], pos[1]]
        self.width = VGUN_WIDTH
        self.height = VGUN_HEIGHT
        self.loopTime = loopTime
        self.resetTime = resetTime
        self.triggerShootLaserEvent()

    def triggerShootLaserEvent(self):
        Timer.SetTimerEvent(self.loopTime, self.shootLaser)

    def shootLaser(self):
        pos = [self.position[0],self.position[1]]
        pos[0] += self.width / 2
        pos[1] += self.height / 2
        LaserV.CreateLaserV(pos, self)
        Sound.playLaserGunSound()

    @staticmethod
    def CreateLaserVGuns():
        positions = Level.currentLevel.laserVGunPositions
        timers = Level.currentLevel.laserVGunTimers
        LaserVGun.guns = []
        guns = LaserVGun.guns
        for i in range(len(positions)):
            position = positions[i]
            loopTime = timers[i][0]
            resetTime = timers[i][1]
            laserVGun = LaserVGun(position, loopTime, resetTime)
            guns.append(laserVGun)

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
