import pygame
from luma.core.render import canvas
from luma.core.legacy import text, show_message

class Alarm:
    def __init__(self, virtual, device):
        self.hours = 6
        self.minutes = 30
        self.state = 0
        self.virtual = virtual
        self.device = device

    def state_callback(self, channel):
        if self.state == 2 or self.state == 3:
            self.state = 0
        else:
            self.state = self.state + 1
        print("state: " + str(self.state).zfill(2))

    def inc_callback(self, channel):
        if self.state == 1:
            if self.hours + 1 > 23:
                self.hours = 0
            else:
                self.hours = self.hours + 1
            print("hours: " + str(self.hours).zfill(2))
        elif self.state == 2:
            if self.minutes + 5 > 59:
                self.minutes = 0
            else:
                self.minutes = self.minutes + 5
            print("minutes: " + str(self.minutes).zfill(2))

    def dec_callback(self, channel):
        if self.state == 1:
            if self.hours - 1 < 0:
                self.hours = 23
            else:
                self.hours = self.hours - 1
            print("hours: " + str(self.hours).zfill(2))
        elif self.state == 2:
            if self.minutes - 5 < 0:
                self.minutes = 59
            else:
                self.minutes = self.minutes - 5
            print("minutes: " + str(self.minutes).zfill(2))


    def sound_alarm(self):
        pygame.mixer.init()
        pygame.mixer.music.load("../alarm_sound.wav")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
            if self.state != 3:
                print("Stopping alarm")
                pygame.mixer.music.pause()
                break

    def alarm_loop(self):
        while True:
            time.sleep(blinkTime)

    def set_contrast(self, new_contrast):
        self.device.contrast(new_contrast)

    def getContrast(self):
        b = 4.58e-3
        c = -2.19e-1
        d = 2.63
        f = 5
        contrast = b*pow(self.hours,4) + c*pow(self.hours,3) + d*pow(self.hours,2) + f
        return min(int(contrast), 100)

    def displayText(self, displayText):
        with canvas(self.virtual) as draw:
            text(draw, (1, 0), displayText, fill="white")

