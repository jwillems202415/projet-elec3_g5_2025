# Call this script to reset all leds.

from machine import Pin

LED_R = Pin(6, Pin.OUT)
LED_B = Pin(9, Pin.OUT)
LED_W = Pin(4, Pin.OUT)

LED_R.off()
LED_R.off()
LED_W.off()