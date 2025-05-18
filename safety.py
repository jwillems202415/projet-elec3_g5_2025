# Modules used for the safety of the device
from machine import Pin
import network
import sys

LED_R = Pin(6, Pin.OUT) # Capture mode / setup mode
LED_B = Pin(9, Pin.OUT) # Transmission mode / AP mode
LED_W = Pin(4, Pin.OUT)

BUTTON = Pin(13, Pin.IN, Pin.PULL_UP) # Emergency stop button

HC_TRIGGER = Pin(15, Pin.OUT)
HC_ECHO = Pin(14, Pin.IN)

def shutdown():
    """Function called for a shutdown of the system."""
    print("Shutting down system...")

    # Disconnect from Wi-Fi
    wlan = network.WLAN(network.STA_IF)
    if wlan.active():
        wlan.disconnect()
        wlan.active(False)

    # Turn off all LEDs
    LED_R.off()
    LED_W.off()
    LED_W.off()

    # Stop further execution
    print("Done.")
    sys.exit()  # This halts the main script, but won't turn off power.

# Emergency button

def shutdown_watchdog():
    """If the button is pressed, the whole device shuts down"""
    
    while True:
        if BUTTON.value() == 0:  # Button is pressed
            print("🛑 Shutdown button pressed!")
            shutdown()

# Proximity sensor

def mesure_distance():
    """Sends a pulse on the proximity sensor to get a distance measurement"""
    # Envoi d'une impulsion de 10 µs sur Trigger
    trigger.value(0)
    time.sleep_us(2)
    trigger.value(1)
    time.sleep_us(10)
    trigger.value(0)

    # Lecture de la durée de l'impulsion Echo
    duree = time_pulse_us(echo, 1, 30000)  # 30 ms max
    if duree < 0:
        return None  # hors de portée

    # Conversion en centimètres (aller-retour /2, ~29.1 µs/cm)
    distance = (duree / 2) / 29.1
    return distance

def distance_monitor_thread():
    """The thread used by the proximity sensor to monitor the distance"""
    global stop_thread
    while not stop_thread:
        dist = mesure_distance()
        if dist is None:
            print("Distance: Out of reach")
        else:
            print("Distance: {:.2f} cm".format(dist))
            if dist < 40:
                print("Obstacle detected at less than 40 cm. Shutdown initiated.")
                shutdown()
        time.sleep(1)
