from machine import Pin

button = Pin(13, Pin.IN, Pin.PULL_UP)

while True:
    if button.value() == 0:
        print("Button pressed")