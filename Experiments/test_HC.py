from machine import Pin, time_pulse_us
import time
import sys  # Required to exit the program

# Configuration des broches
trigger = Pin(15, Pin.OUT)
echo = Pin(14, Pin.IN)

LED_R = Pin(6, Pin.OUT)

def mesure_distance():
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

while True:
    dist = mesure_distance()
    if dist is None:
        print("Distance : hors de portée")
    else:
        print("Distance : {:.2f} cm".format(dist))
        if dist < 40:
            print("Obstacle détecté à moins de 40 cm. Arrêt du programme.")
            LED_R.value(1)
            break  # Sortie de la boucle

    time.sleep(1)
