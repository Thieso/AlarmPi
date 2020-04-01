#!/usr/bin/python3
import time
import pygame
import pyttsx3
from luma.core.render import canvas
from luma.core.legacy import text, show_message
from luma.core.virtual import viewport

class Alarm:
    def __init__(self, virtual, device):
        # initialize variables and set defaults
        self.alarm_hour = 6
        self.alarm_minutes = 30
        self.alarm_string = "0630"
        self.state = 0
        self.blink_time = 0.25
        self.contrast = 10
        self.virtual = virtual
        self.device = device
        self.filename = "/home/pi/Alarm/alarm_time"
        self.date_interval = 10
        self.is_daytime = True
        self.alarm_sound_file = "/home/pi/Alarm/alarm_sound.wav"
        # set initial contrast
        self.getContrast(int(time.strftime('%H')))
        self.device.contrast(self.contrast)
        # read alarm string from file and update alarm string
        self.read_alarm_from_file()
        self.update_alarm_string()
        self.nth = {
            1: "first",
            2: "second",
            3: "third",
            4: "fourth",
            5: "fifth",
            6: "sixth",
            7: "seventh",
            8: "eighth",
            9: "ninth",
            10: "tenth",
            11: "eleventh",
            12: "twelfth",
            13: "thirteenth",
            14: "fourteenth",
            15: "fifteenth",
            16: "sixteenth",
            17: "seventeenth",
            18: "eighteenth",
            19: "nineteenth",
            20: "twentieth",
            21: "twenty-first",
            22: "twenty-second",
            23: "twenty-third",
            24: "twenty-fourth",
            25: "twenty-fifth",
            26: "twenty-sixth",
            27: "twenty-seventh",
            28: "twenty-eighth",
            29: "twenty-ninth",
            30: "thirtyth",
            31: "thirty-first",
        }

    def alarm_loop(self):
        '''Loop for the alarm clock'''
        # initialze hour and time string
        hour = 0
        time_string = ""

        # initialize tts engine
        self.engine = pyttsx3.init()

        while True:
            # sleep for the blink time
            time.sleep(self.blink_time)

            # set time string
            time_string = time.strftime('%H%M')

            # set contrast based on time
            new_hour = int(time.strftime('%H'))
            if hour != new_hour:
                hour = new_hour
                self.getContrast(hour)
                self.device.contrast(self.contrast)

            if time_string == self.alarm_string:
                self.sounded_alarm = True
                self.state = 3
                print("Sounding Alarm")
                self.display_text(self.alarm_string)
                self.sound_alarm()
                time.sleep(2)
                # say a nice good morning message
                weekday = time.strftime('%A')
                number = self.nth[int(time.strftime('%e'))]
                months = time.strftime('%B')
                hours = time.strftime('%H')
                minutes = time.strftime('%M')
                tts_string = "Good Morning, today is " + weekday + " the " + number + " of " + months + ". It is " + hours + " " + minutes
                self.text_to_speech(tts_string)
                # in order to not ring again wait till minute passed
                while time.strftime('%H%M') == self.alarm_string:
                    time.sleep(1)

            # display information depending on the state
            if self.state == 0:
                # display time on display and every date_interval seconds display the date
                seconds = int(time.localtime().tm_sec % 60)
                if  seconds % self.date_interval == 0 and self.is_daytime is True:
                    months = time.strftime('%b %d')
                    scroll_text = time_string + " " + months.upper()  + " " + time_string
                    self.scroll_text(scroll_text)
                else:
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

    def read_alarm_from_file(self):
        '''Reads alarm string from file'''
        try:
            fd = open(self.filename, "r")
            read_string = fd.read()
            self.alarm_string = read_string
            self.alarm_hour = int(self.alarm_string[0:2])
            self.alarm_minutes = int(self.alarm_string[2:4])
            fd.close()
            print("Read alarm from file: " + str(self.alarm_hour) + ":" + str(self.alarm_minutes))
        except:
            print("File not found, please create alarm_string file")

    def write_alarm_to_file(self):
        '''Write alarm string to file'''
        try:
            print("Writing alarm to file: " + self.alarm_string)
            fd = open(self.filename, "w")
            fd.write(self.alarm_string + "\n")
            fd.close()
        except:
            print("File not found, please create alarm_string file")

    def update_alarm_string(self):
        '''Create the alarm string from the integers that indicate the alarm
        time'''
        hour_string = str(self.alarm_hour).zfill(2)
        minute_string = str(self.alarm_minutes).zfill(2)
        self.alarm_string = hour_string + minute_string


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
        pygame.mixer.music.load(self.alarm_sound_file)
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
            self.contrast = 5
            self.is_daytime = False
        elif hour <= 10 or hour >= 17:
            self.contrast = 50
            self.is_daytime = True
        else:
            self.contrast = 100
            self.is_daytime = True

    def display_text(self, text_string):
        '''Display text on the LED matrix'''
        with canvas(self.virtual) as draw:
            for i, word in enumerate(text_string):
                text(draw, (1, i*8), word, fill="white")

    def scroll_text(self, text_string):
        '''Scroll text on the LED matrix'''
        # set new viewport which fits the whole string
        virtual = viewport(self.device, width=8,
                height=len(text_string) * 8)
        # draw the string in intial position on the viewport
        with canvas(virtual) as draw:
            for i, word in enumerate(text_string):
                text(draw, (1, i*8), word, fill="white")
        # scroll the string by offsetting the viewport
        for offset in range(virtual.height - self.device.height + 1):
            virtual.set_position((0, offset))
            time.sleep(0.05)

    def text_to_speech(self, tts_string):
        self.engine.say(tts_string)
        self.engine.setProperty('rate',20) # words per minute
        self.engine.setProperty('volume',0.9)
        self.engine.runAndWait()
