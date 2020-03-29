import time
import pygame
from luma.core.render import canvas
from luma.core.legacy import text, show_message

class Alarm:
    def __init__(self, virtual, device):
        # initialize variables and set defaults
        self.hours = 6
        self.minutes = 30
        self.state = 0
        self.blink_time = 0.5
        self.contrast = 10
        self.virtual = virtual
        self.device = device

    def alarm_loop(self):
        # initialze hour and time string
        hour = 0
        time_string = 0

        while True:
            # sleep for the blink time
            time.sleep(self.blink_time)

            # set time string
            time_string = time.strftime('%H%M')

            # set alarm string for the right time
            hour_string = str(self.hours).zfill(2)
            minute_string = str(self.minutes).zfill(2)
            alarm_string = hour_string + minute_string

            # set contrast based on time
            new_hour = int(time.strftime('%H'))
            if hour != new_hour:
                hour = new_hour
                self.contrast = self.getContrast(hour)
                self.device.contrast(self.contrast)

            if time_string == alarm_string:
                self.sounded_alarm = True
                self.state = 3
                print("Sounding Alarm")
                self.display_text(alarm_string)
                self.sound_alarm()
                # blink all the numbers during alarm sounding
                # in order to not ring again wait till minute passed
                while time.strftime('%H%M') == alarm_string:
                    time.sleep(1)

            # display information depending on the state
            if self.state == 0:
                # display time on display
                self.display_text(time_string)
            elif self.state == 1:
                # blink the hours on the display
                self.display_text(alarm_string)
                time.sleep(self.blink_time)
                alarm_string = "--" + str(self.minutes).zfill(2)
                self.display_text(alarm_string)
            elif self.state == 2:
                # blink the minutes on the display
                self.display_text(alarm_string)
                time.sleep(self.blink_time)
                alarm_string = str(self.hours).zfill(2) + "--"
                self.display_text(alarm_string)

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

    def set_contrast(self, new_contrast):
        self.device.contrast(new_contrast)

    def getContrast(self, hour):
        b = 4.58e-3
        c = -2.19e-1
        d = 2.63
        f = 5
        contrast = b*pow(self.hours,4) + c*pow(self.hours,3) + d*pow(self.hours,2) + f
        return min(int(contrast), 100)

    def display_text(self, text_string):
        with canvas(self.virtual) as draw:
            text(draw, (1, 0), text_string, fill="white")
