#!/usr/bin/python3
import pygame
import time

# test the sound output of the system

for i in range(5):
    pygame.init()
    pygame.mixer.init(frequency=44100, size=-16, channels=1, buffer=512, devicename='Alarm')
    pygame.mixer.music.load("../alarm_sound.wav")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        time.sleep(3)
        pygame.quit()
        break
