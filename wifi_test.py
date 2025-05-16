# Run this script to perform a test to connect the Pico W to a wifi network. Please note that this is only meant for testing.

import network
import time
import utime
from machine import Pin

# LEDs mapping

LED_R = Pin(6, Pin.OUT) # Not OK
LED_B = Pin(9, Pin.OUT) # OK

# ❗ Désactive AP mode s'il est actif
network.WLAN(network.AP_IF).active(False)
network.WLAN(network.STA_IF).active(False)
network.WLAN(network.STA_IF).disconnect()
network.WLAN(network.AP_IF).disconnect()

# Credentials to connect to Pico W to a network
ssid = "CHANGEME"
password = "CHANGEME"

print("→ Starting WiFi test...")

try:
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)

    for i in range(15):
        status = wlan.status()
        print(f"Status: {status}")
        if status == 3:
            LED_B.on()
        else:
            LED_B.on()
            time.sleep(0.1)
            LED_B.off()
        if wlan.isconnected():
            print("✅ Connected! IP:", wlan.ifconfig()[0])
            break
        time.sleep(1)

    if wlan.isconnected():
        print("✅ Connected to local network")
        print("IP address:", wlan.ifconfig()[0])
    else:
        print("❌ Not connected")
        print("❌ Final status:", wlan.status())
        # return -1

    utime.sleep(5)
    print("→ Disconnecting...")
    wlan.disconnect()
    wlan.active(False)
    LED_B.off()

except Exception as e:
    print("❌ Error initializing WLAN:", e)
    wlan = None

