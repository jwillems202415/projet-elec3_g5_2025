# Call the following function to display a number on the two displays.

from machine import Pin
import time

def display_number(display_value):
    bcd_pins = [Pin(n, Pin.OUT) for n in [18, 26, 22, 19]]
    digits = [Pin(27, Pin.OUT), Pin(28, Pin.OUT)]

    BCD_CODES = [
        [0, 0, 0, 0],  # 0
        [1, 0, 0, 0],  # 1
        [0, 1, 0, 0],  # 2
        [1, 1, 0, 0],  # 3
        [0, 0, 1, 0],  # 4
        [1, 0, 1, 0],  # 5
        [0, 1, 1, 0],  # 6
        [1, 1, 1, 0],  # 7
        [0, 0, 0, 1],  # 8
        [1, 0, 0, 1],  # 9
    ]

    def set_bcd(value):
        code = BCD_CODES[value]
        for pin, bit in zip(bcd_pins, code):
            pin.value(bit)

    while True:
        # Ensure the number is an integer
        number = int(display_value)

        # Extract digits
        if number < 10:
            left_digit = 0
            right_digit = number
        else:
            left_digit = (number // 10) % 10
            right_digit = number % 10

        # Display left digit
        set_bcd(left_digit)
        digits[0].value(1)
        time.sleep(0.005)
        digits[0].value(0)

        # Display right digit
        set_bcd(right_digit)
        digits[1].value(1)
        time.sleep(0.005)
        digits[1].value(0)
