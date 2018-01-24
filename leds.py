import RPi.GPIO as GPIO
import time
import random
from signal import pause
from gpiozero import LED
from gpiozero import Button as Button_gpio
from tkinter import *

leds = [LED(4),LED(15),LED(17),LED(22),LED(24),LED(6),LED(19),LED(20)]
buttons = [Button_gpio(3),Button_gpio(14),Button_gpio(18),Button_gpio(27),Button_gpio(23),Button_gpio(5),Button_gpio(13),Button_gpio(16)]

def testing():
    i=0
    while i<8:
        buttons[i].when_pressed = leds[i].on
        buttons[i].when_released = leds[i].off
        i=i+1

def hello():
    leds[i].on
    buttons[i].when_pressed = leds[i].off
    buttons[i].when_released = True
    pause()


testing()
print('oh, yeah!')
