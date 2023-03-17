import pygame
from LevelLoader import Level
from Timer import Timer

class Sound:

    @staticmethod
    def init():

        Sound.SND_LASER_GUN_SOUND = pygame.mixer.Sound("laser-gun-sound.wav")

        Sound.SND_MAIN_MUSIC = pygame.mixer.Sound("main-music.mp3")
        Sound.SND_MAIN_MUSIC_2 = pygame.mixer.Sound("main-music-2.mp3")
        Sound.SND_MAIN_MUSIC_3 = pygame.mixer.Sound("main-music-3.mp3")
        Sound.SND_INTRO_TELEPORT = pygame.mixer.Sound("intro-teleport.mp3")
        Sound.SND_INTRO_TELEPORT_2 = pygame.mixer.Sound("intro-teleport-2.mp3")
        Sound.SND_INTRO_TELEPORT_3 = pygame.mixer.Sound("intro-teleport-3.wav")

        Sound.SND_GAME_ENDING = pygame.mixer.Sound("game-ending.wav")

        Sound.SND_DEATH_SOUND = pygame.mixer.Sound("death-sound.mp3")

        Sound.currentMainMusic = 'none'

    @staticmethod
    def playLaserGunSound():
        pygame.mixer.Sound.play(Sound.SND_LASER_GUN_SOUND)
        pygame.mixer.music.stop()

    @staticmethod
    def playIntroTeleport():
        pygame.mixer.Sound.play(Sound.SND_INTRO_TELEPORT)
        pygame.mixer.music.stop()

    @staticmethod
    def playIntroTeleport2():
        pygame.mixer.Sound.play(Sound.SND_INTRO_TELEPORT_2)
        pygame.mixer.music.stop()

    @staticmethod
    def playIntroTeleport3():
        pygame.mixer.Sound.play(Sound.SND_INTRO_TELEPORT_3)
        pygame.mixer.music.stop()

    @staticmethod
    def playBallBounce():
        pygame.mixer.Sound.play(Sound.SND_BALL_BOUNCE)
        pygame.mixer.music.stop()

    @staticmethod
    def playDeathSound():
        pygame.mixer.Sound.play(Sound.SND_DEATH_SOUND)
        pygame.mixer.music.stop()

    @staticmethod
    def increaseEndGameVolume():

        if Sound.endingVolume == 1.0:
            return None

        Sound.endingVolume += 0.005
        Sound.SND_GAME_ENDING.set_volume(Sound.endingVolume)
        Timer.SetTimerEvent(100, Sound.increaseEndGameVolume)

    @staticmethod
    def playGameEnding():
        Sound.endingVolume = 0.0
        Sound.SND_GAME_ENDING.set_volume(Sound.endingVolume)
        pygame.mixer.Sound.play(Sound.SND_GAME_ENDING)
        pygame.mixer.music.stop()

        Timer.SetTimerEvent(100, Sound.increaseEndGameVolume)


    @staticmethod
    def playMainMusic():

        if Sound.currentMainMusic != 1 and Level.currentLevel.main_music == 1:

            Sound.SND_MAIN_MUSIC_3.stop()
            Sound.SND_MAIN_MUSIC_2.stop()

            Sound.currentMainMusic = Level.currentLevel.main_music

            Sound.playIntroTeleport()
            pygame.mixer.Sound.play(Sound.SND_MAIN_MUSIC, -1)

        elif Sound.currentMainMusic != 2 and Level.currentLevel.main_music == 2:

            Sound.SND_MAIN_MUSIC.stop()
            Sound.SND_MAIN_MUSIC_3.stop()

            Sound.currentMainMusic = Level.currentLevel.main_music

            Sound.playIntroTeleport2()
            pygame.mixer.Sound.play(Sound.SND_MAIN_MUSIC_2, -1)

        elif Sound.currentMainMusic != 3 and Level.currentLevel.main_music == 3:

            Sound.SND_MAIN_MUSIC.stop()
            Sound.SND_MAIN_MUSIC_2.stop()

            Sound.currentMainMusic = Level.currentLevel.main_music

            Sound.playIntroTeleport3()

            pygame.mixer.Sound.play(Sound.SND_MAIN_MUSIC_3, -1)
            Sound.SND_MAIN_MUSIC_3.set_volume(0.7)

        pygame.mixer.music.stop()
