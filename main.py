import sys, pygame
import time, random
import pygame.gfxdraw

from LevelLoader import Level
from GameObjects import ExitDoor, Bouncer, MovingPlatform
from Utility import Utils
from GameConstants import *
from Sound import *
from Timer import *
from Controls import *
from Renderer import *
from GameWorld import *
from SceneModule import *

if __name__ == '__main__':

    pygame.init()
    Timer.init()

    Scene.CreateScenes()
    SceneManager.CreateSceneManager()

    size = width, height = SCREEN_WIDTH, SCREEN_HEIGHT

    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Bouncer")

    while SceneManager.sceneManager.getCurrentStatus() == "running":

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            for i in range(len(Timer.events)):
                timer_event = Timer.events[i]
                timer_callback = Timer.callbacks[i]
                args = Timer.args[i]
                if event.type == timer_event:
                    if args == None:
                        timer_callback()
                    else:
                        timer_callback(args)

        keys = pygame.key.get_pressed()
        SceneManager.sceneManager.triggerSceneControls(keys)
        SceneManager.sceneManager.triggerSceneUpdate()
        SceneManager.sceneManager.triggerSceneRender()
        currentScene = SceneManager.sceneManager.getCurrentScene()
        sceneBuffer = currentScene.getBuffer()
        pygame.Surface.blit(screenBuffer, sceneBuffer, (0, 0))
        pygame.Surface.blit(screen, screenBuffer, (0,0))
        pygame.display.flip()

        fpsClock.tick(FPS)

    GameWorld.quit()