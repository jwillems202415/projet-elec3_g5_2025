from machine import Pin
import time

# Module taking as input a number then displays it continuously on the segmented displays.

def display_number(display_value):

    # Mapping of the four pins used to input a number into the decoder in BCD format, going from LSB to MSB
    bcd_pins = [Pin(n, Pin.OUT) for n in [18,26,22,19]]

    # Mapping of the two pins used to activate or not the two segment displays
    digits = [Pin(27, Pin.OUT), Pin(28, Pin.OUT)]

    # Table BCD 0–9, going from LSB → MSB
    BCD_CODES = [
        [0,0,0,0],  # 0
        [1,0,0,0],  # 1
        [0,1,0,0],  # 2
        [1,1,0,0],  # 3
        [0,0,1,0],  # 4
        [1,0,1,0],  # 5
        [0,1,1,0],  # 6
        [1,1,1,0],  # 7
        [0,0,0,1],  # 8
        [1,0,0,1],  # 9
    ]

    # Receives a number then "encodes" it in a format understandable by the decoder
    def set_bcd(valeur):
        code = BCD_CODES[valeur]
        for pin, bit in zip(bcd_pins, code):
            pin.value(bit)
    
    # Main loop
    while True:
        
        # Displays the left digit on the left display, then turns it off
        set_bcd(int(str(display_value)[0]))
        digits[0].value(1)
        time.sleep(0.005)
        digits[0].value(0)
        
        # Displays the right digit on the right display, then turns it off
        set_bcd(int(str(display_value)[1]))
        digits[1].value(1)
        time.sleep(0.005)
        digits[1].value(0)