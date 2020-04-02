#!/usr/bin/python3
# program to test text to speech using the pyttsx3 module
import pyttsx3
import time

nth = {
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

engine = pyttsx3.init()
weekday = time.strftime('%A')
number = time.strftime('%e')
number = nth[int(number)]
months = time.strftime('%B')
tts_string = "Good Morning, today is " + weekday + " the " + number + " of " + months
engine.setProperty('rate',120) # words per minute
engine.setProperty('volume',0.9)
engine.say(tts_string)
engine.runAndWait()
