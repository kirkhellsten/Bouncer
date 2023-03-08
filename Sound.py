import pygame

class Sound:

    @staticmethod
    def init():
        Sound.SND_GAME_MUSIC = pygame.mixer.Sound("gamemusic.wav")
        Sound.SND_LASER_GUN_SOUND = pygame.mixer.Sound("laser-gun-sound.wav")

        Sound.SND_MAIN_MUSIC = pygame.mixer.Sound("main-music.mp3")
        Sound.SND_INTRO_TELEPORT = pygame.mixer.Sound("intro-teleport.mp3")
        Sound.SND_BALL_BOUNCE = pygame.mixer.Sound("ballbounce.wav")
        Sound.SND_DEATH_SOUND = pygame.mixer.Sound("death-sound.mp3")

    @staticmethod
    def playLaserGunSound():
        pygame.mixer.Sound.play(Sound.SND_LASER_GUN_SOUND)
        pygame.mixer.music.stop()

    @staticmethod
    def playIntroTeleport():
        pygame.mixer.Sound.play(Sound.SND_INTRO_TELEPORT)
        pygame.mixer.music.stop()

    @staticmethod
    def playBallBounce():
        pygame.mixer.Sound.play(Sound.SND_BALL_BOUNCE)
        pygame.mixer.music.stop()

    @staticmethod
    def platDeathSound():
        pygame.mixer.Sound.play(Sound.SND_DEATH_SOUND)
        pygame.mixer.music.stop()

    @staticmethod
    def playMainMusic():
        pygame.mixer.Sound.play(Sound.SND_MAIN_MUSIC, -1)
        pygame.mixer.music.stop()