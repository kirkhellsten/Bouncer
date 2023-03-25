import pygame
from GameConstants import *
from Controls import *
from GameWorld import *
from Renderer import *
from Timer import *
from UI import *

class SceneManager:
    def __init__(self):
        SceneManager.scenes = {}
        self.currentScene = None
        self.sceneStatus = "none"
        self.status = "running"


    @staticmethod
    def CreateSceneManager():
        SceneManager.sceneManager = SceneManager()
        SceneManager.sceneManager.addScene(Scene.splashScene)
        SceneManager.sceneManager.addScene(Scene.mainMenuScene)
        SceneManager.sceneManager.addScene(Scene.playScene)
        SceneManager.sceneManager.setCurrentScene(Scene.splashScene.getId())

    def addScene(self, scene):
        SceneManager.scenes[scene.getId()] = scene

    def setCurrentScene(self, id):
        if id not in SceneManager.scenes:
            raise Exception("Sorry, the scene id does not exist")
        elif self.currentScene == None:
            self.currentScene = SceneManager.scenes[id]
            self.sceneStatus = "init"
            SceneManager.sceneManager.triggerSceneInit()
        elif self.currentScene.getId() != id:
            SceneManager.sceneManager.transitionToScene(id)
        elif self.currentScene.getId() == id:
            return None

    def getCurrentScene(self):
        return self.currentScene

    def getCurrentSceneStatus(self):
        return self.sceneStatus

    def getCurrentStatus(self):
        return self.status

    def exit(self):
        self.status = "exit"


    def __triggerSceneTransition(self, id):
        self.sceneStatus = "exit"
        self.alpha = 0
        self.triggerSceneExit()
        self.currentScene = SceneManager.scenes[id]
        self.sceneStatus = "init"
        SceneManager.sceneManager.triggerSceneInit()

    def transitionToScene(self, id):
        self.sceneStatus = "fadeout"
        Timer.SetTimerEvent(1500, self.__triggerSceneTransition, id)

    def triggerSceneControls(self, keys=None, keydown=None):
        self.currentScene.controls(keys, keydown)

    def triggerSceneUpdate(self):

        if self.sceneStatus == "running":
            self.currentScene.update()

    def triggerSceneRender(self):

        if self.sceneStatus == "running":
            self.currentScene.render()
        elif self.sceneStatus == "fadeout":
            self.currentScene.fadeout()


    def triggerSceneInit(self):
        if self.sceneStatus == "init":
            self.currentScene.init()
            self.sceneStatus = "running"

    def triggerSceneExit(self):
        if self.sceneStatus == "exit":
            self.currentScene.exit()
            self.sceneStatus = "finished"

    def triggerCompleteExit(self):
        self.status = "exit"

class Scene:

    def __init__(self, id):
        self.id = id
        self.buffer = pygame.surface.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.alpha = 0
        self.sprites = []

    @staticmethod
    def CreateScenes():
        Scene.splashScene = SplashScene()
        Scene.playScene = PlayScene()
        Scene.mainMenuScene = MainMenuScene()

    def getId(self):
        return self.id

    def getBuffer(self):
        return self.buffer

    def fadeout(self):
        transparentSurface = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT), pygame.SRCALPHA)
        transparentSurface.fill((0,0,0,self.alpha))
        self.buffer.blit(transparentSurface, (0,0))
        self.alpha += FADEOUT_ALPHA_SPEED

    def init(self):
        return None

    def exit(self):
        return None

    def update(self):
        return None

    def render(self):
        backgroundRect = pygame.Rect((0, 0), (SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.draw.rect(self.buffer, BACKGROUND_COLOR, backgroundRect)
        for sprite in self.sprites:
            sprite.render()
            self.buffer.blit(sprite.buffer, (sprite.x, sprite.y))

    def controls(self, keys=None, keydown=None):
        return None

class PlayScene(Scene):
    def __init__(self, id="PLAY_SCENE"):
        super().__init__(id)

    def init(self):
        GameWorld.init()

    def update(self):
        GameWorld.update()

    def render(self):
        Renderer.draw(self.buffer)


    def controls(self, keys=None, keydown=None):
        Controls.key_pressed(keys)

class MainMenuScene(Scene):
    def __init__(self, id="MAIN_MENU_SCENE"):
        super().__init__(id)

    def __setSelectedMenuItem(self):
        self.resumeMenuItem.setSelected(False)
        self.newGameMenuItem.setSelected(False)
        self.exitMenuItem.setSelected(False)
        if self.currentSelectedMenuItemIndex == 1:
            self.resumeMenuItem.setSelected(True)
        elif self.currentSelectedMenuItemIndex == 2:
            self.newGameMenuItem.setSelected(True)
        elif self.currentSelectedMenuItemIndex == 3:
            self.exitMenuItem.setSelected(True)

    def __selectMenuItem(self):
        if self.currentSelectedMenuItemIndex == 1:
            SceneManager.sceneManager.transitionToScene(Scene.playScene.getId())
        elif self.currentSelectedMenuItemIndex == 2:
            d = {}
            d["resumeLevel"] = "level1.txt"
            Utils.writeDictToFile(d, "save.txt")
            SceneManager.sceneManager.transitionToScene(Scene.playScene.getId())
        elif self.currentSelectedMenuItemIndex == 3:
            SceneManager.sceneManager.exit()

    def init(self):
        self.sprites.append(UIMenu(100, 100))

        self.currentSelectedMenuItemIndex = 1
        self.resumeMenuItem = UIMenuItem(150, 200, "Continue", selected=True)
        self.newGameMenuItem = UIMenuItem(150, 300, "New Game")
        self.exitMenuItem = UIMenuItem(150, 400, "Exit")

        self.sprites.append(self.resumeMenuItem)
        self.sprites.append(self.newGameMenuItem)
        self.sprites.append(self.exitMenuItem)

    def update(self):
        return None

    def render(self):
        super().render()

    def controls(self, keys=None, keydown=None):

        if keydown == pygame.K_UP:
            if self.currentSelectedMenuItemIndex == 1:
                self.currentSelectedMenuItemIndex = 3
            else:
                self.currentSelectedMenuItemIndex -= 1
        elif keydown == pygame.K_DOWN:
            if self.currentSelectedMenuItemIndex == 3:
                self.currentSelectedMenuItemIndex = 1
            else:
                self.currentSelectedMenuItemIndex += 1
        elif keydown == pygame.K_RETURN:
            self.__selectMenuItem()

        self.__setSelectedMenuItem()


class SplashScene(Scene):
    def __init__(self, id="SPLASH_SCENE"):
        super().__init__(id)
        self.backgroundImage = pygame.image.load("HellstenGamesLogo.png")

    def __splashDelayCallback(self):
        SceneManager.sceneManager.transitionToScene(Scene.mainMenuScene.getId())

    def init(self):
        Timer.SetTimerEvent(4000, self.__splashDelayCallback)

    def update(self):
        return None

    def render(self):
        backgroundRect = pygame.Rect((0, 0), (SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.draw.rect(self.buffer, (255, 255, 255), backgroundRect)
        self.buffer.blit(self.backgroundImage, (SCREEN_WIDTH / 2 - self.backgroundImage.get_width() / 2,
                                                SCREEN_HEIGHT / 2 - self.backgroundImage.get_height() / 1.75))

    def controls(self, keys=None, keydown=None):
        return None
