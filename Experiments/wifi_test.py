# Run this script to perform a connectivity test to your wifi network.

import network
import time
import utime
from machine import Pin

# LEDs mapping

LED_W = Pin(4, Pin.OUT)

def activity_light():
    """Makes the white led blink to indicate activity"""
    LED_W.off()
    time.sleep(0.01)
    LED_W.on()


# ❗ Désactive AP mode s'il est actif
network.WLAN(network.AP_IF).active(False)
activity_light()
network.WLAN(network.STA_IF).active(False)
activity_light()
network.WLAN(network.STA_IF).disconnect()
activity_light()
network.WLAN(network.AP_IF).disconnect()
activity_light()

# Credentials to connect to Pico W to a network
ssid = "iphone_xr"
password = "C-982927"

print("→ Starting WiFi test...")
activity_light()

try:
    wlan = network.WLAN(network.STA_IF)
    activity_light()
    wlan.active(True)
    activity_light()
    wlan.connect(ssid, password)
    activity_light()

    for i in range(15):
        activity_light()
        status = wlan.status()
        print(f"Status: {status}")
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

    utime.sleep(5)
    print("→ Disconnecting...")
    activity_light()
    wlan.disconnect()
    activity_light()
    wlan.active(False)
    activity_light()

except Exception as e:
    print("❌ Error initializing WLAN:", e)
    activity_light()
    wlan = None
    utime.sleep(5)
