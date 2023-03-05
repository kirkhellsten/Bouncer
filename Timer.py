import pygame

class Timer:

    @staticmethod
    def init():
        Timer.timer_index = 1
        Timer.events = []
        Timer.callbacks = []
        Timer.args = []

    @staticmethod
    def quit():
        for event in Timer.events:
            pygame.time.set_timer(event, 0)

    @staticmethod
    def __getNextTimerIndex():
        Timer.timer_index += 1
        return Timer.timer_index

    @staticmethod
    def SetTimerEvent(milliseconds, callback, args=None):
        timer_event = pygame.USEREVENT + Timer.__getNextTimerIndex()
        Timer.events.append(timer_event)
        Timer.callbacks.append(callback)
        Timer.args.append(args)
        pygame.time.set_timer(timer_event, milliseconds, 1)