#!/usr/bin/python3
import pygame

# test the sound output of the system

pygame.mixer.init(frequency=44100, size=-16, channels=1, buffer=512, devicename=None)
pygame.mixer.music.load("../alarm_sound.wav")
pygame.mixer.music.play()
while pygame.mixer.music.get_busy() == True:
    continue
pygame.mixer.music.quit()
