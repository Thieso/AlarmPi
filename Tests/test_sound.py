#!/usr/bin/python3
import pygame

# test the sound output of the system

pygame.mixer.init()
pygame.mixer.music.load("../alarm_sound.wav")
pygame.mixer.music.play()
while pygame.mixer.music.get_busy() == True:
    continue
