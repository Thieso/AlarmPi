# Raspberry Pi Alarm Clock

Simple alarm clock using the following components

* Raspberry Pi 4
* 8x32 LED Matrix
* 3 Push Buttons
* Loudspeaker
* Sound Amplifier

![](device.jpg?raw=true)

## Dependencies 

For the LED matrix programming, the luma library is used, for installation
instructions see https://luma-led-matrix.readthedocs.io/en/latest/ 

For the sound output the pygame library is used, for more information see https://www.pygame.org/

For the text to speech output, the pyttsx3 library is used

For volume changing, the alsaaudio library is used.

## Wiring

Wiring is done according to the individual component pinout diagrams. Important
is that the raspberry pi has its own power supply because when using the same as
the LED matrix there is an undervoltage issue and the pi will not start up.
Another option is to use a boost DC-DC converter to power everything from the
same power supply.

## Sound file

The sound file can be set in `Alarm.py` with the attribute `alarm_sound_file`

## Alarm time file

For the code to work, it is assumed that there is a file containing the alarm
time. The format of the content is simply `<hours(with possible leading
zero)><minutes(with possible leading zero)>`. For example for an alarm at 8:05
the content needs to be 0805. The file location and name can be set in
`Alarm.py` with the attribute `filename`

## Buttons

The three buttons work such that the state button changes the state, the
increase button increases the hours/minutes and the decrease button decreases
them when in the correct state. 
The states are:

* 0: showing current time
* 1: changing the hour value of the alarm time
* 2: changing the minute value of the alarm time
* 3: sounding the alarm
