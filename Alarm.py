#!/usr/bin/python3
import time
import pygame
from luma.core.render import canvas
from luma.core.legacy import text, show_message

class Alarm:
    def __init__(self, virtual, device):
        # initialize variables and set defaults
        self.alarm_hour = 6
        self.alarm_minutes = 30
        self.alarm_string = "0630"
        self.update_alarm_string()
        self.state = 0
        self.blink_time = 0.5
        self.contrast = 10
        self.virtual = virtual
        self.device = device
        self.filename = "alarm_time"

    def read_alarm_from_file(self):
        '''Reads alarm string from file'''
        fd = open(self.filename, "r")
        self.alarm_string = fd.read()
        self.alarm_hour = int(self.alarm_string[0:2])
        self.alarm_minutes = int(self.alarm_string[2:4])
        print("Read alarm from file: " + str(self.alarm_hour) + ":" + str(self.alarm_minutes))
        fd.close()

    def write_alarm_to_file(self):
        '''Write alarm string to file'''
        fd = open(self.filename, "w")
        print("Writing alarm to file: " + self.alarm_string)
        fd.write(self.alarm_string)
        fd.close()

    def update_alarm_string(self):
        '''Create the alarm string from the integers that indicate the alarm
        time'''
        hour_string = str(self.alarm_hour).zfill(2)
        minute_string = str(self.alarm_minutes).zfill(2)
        self.alarm_string = hour_string + minute_string

    def alarm_loop(self):
        '''Loop for the alarm clock'''
        # initialze hour and time string
        hour = 0
        time_string = 0

        # read alarm from file
        self.read_alarm_from_file()

        # set initial contrast
        self.device.contrast(self.contrast)

        while True:
            # sleep for the blink time
            time.sleep(self.blink_time)

            # set time string
            time_string = time.strftime('%H%M')

            # set contrast based on time
            new_hour = int(time.strftime('%H'))
            if hour != new_hour:
                hour = new_hour
                self.contrast = self.getContrast(hour)
                self.device.contrast(self.contrast)

            if time_string == self.alarm_string:
                self.sounded_alarm = True
                self.state = 3
                print("Sounding Alarm")
                self.display_text(self.alarm_string)
                self.sound_alarm()
                # blink all the numbers during alarm sounding
                # in order to not ring again wait till minute passed
                while time.strftime('%H%M') == self.alarm_string:
                    time.sleep(1)

            # display information depending on the state
            if self.state == 0:
                # display time on display
                self.display_text(time_string)
            elif self.state == 1:
                # blink the alarm_hour on the display
                self.display_text(self.alarm_string)
                time.sleep(self.blink_time)
                tmp_string = "--" + str(self.alarm_minutes).zfill(2)
                self.display_text(tmp_string)
            elif self.state == 2:
                # blink the alarm_minutes on the display
                self.display_text(self.alarm_string)
                time.sleep(self.blink_time)
                tmp_string = str(self.alarm_hour).zfill(2) + "--"
                self.display_text(tmp_string)

    def state_callback(self, channel):
        '''Callback for the button which changes the state, increments the state
        by 1 or loops it around to 0'''
        if self.state == 2 or self.state == 3:
            # update the alarm string
            self.update_alarm_string()
            # write it to the file
            self.write_alarm_to_file()
            self.state = 0
        else:
            self.state = self.state + 1
        print("State: " + str(self.state).zfill(2))

    def inc_callback(self, channel):
        '''Callback for the increase button to increase the alarm hour or
        minutes'''
        if self.state == 1:
            if self.alarm_hour + 1 > 23:
                self.alarm_hour = 0
            else:
                self.alarm_hour = self.alarm_hour + 1
            print("Alarm Hour: " + str(self.alarm_hour).zfill(2))
        elif self.state == 2:
            if self.alarm_minutes + 5 > 59:
                self.alarm_minutes = 0
            else:
                self.alarm_minutes = self.alarm_minutes + 5
            print("Alarm Minutes: " + str(self.alarm_minutes).zfill(2))
        self.update_alarm_string()

    def dec_callback(self, channel):
        '''Callback for the decrease button to decrease the alarm hour or
        minutes'''
        if self.state == 1:
            if self.alarm_hour - 1 < 0:
                self.alarm_hour = 23
            else:
                self.alarm_hour = self.alarm_hour - 1
            print("Alarm Hour: " + str(self.alarm_hour).zfill(2))
        elif self.state == 2:
            if self.alarm_minutes - 5 < 0:
                self.alarm_minutes = 55
            else:
                self.alarm_minutes = self.alarm_minutes - 5
            print("Alarm Minutes: " + str(self.alarm_minutes).zfill(2))
        self.update_alarm_string()

    def sound_alarm(self):
        '''Sounds the alarm using the pygame module, stops when the state
        changes'''
        pygame.mixer.init()
        pygame.mixer.music.load("../alarm_sound.wav")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
            if self.state != 3:
                print("Stopping Alarm")
                pygame.mixer.music.pause()
                break

    def set_contrast(self, new_contrast):
        '''Sets the contrast of the LED matrix'''
        self.device.contrast(new_contrast)

    def getContrast(self, hour):
        '''Returns the contrast for the LED matrix based on hour'''
        if hour >= 20 or hour <= 7:
            contrast = 5
        else:
            contrast = 50
        return contrast

    def display_text(self, text_string):
        '''Display text on the LED matrix'''
        with canvas(self.virtual) as draw:
            text(draw, (1, 0), text_string, fill="white")
