import network
import time
from machine import Pin

# White LED
LED_W = Pin(4, Pin.OUT)

def activity_light():
    LED_W.off()
    time.sleep(0.01)
    LED_W.on()

# Proper WiFi reset routine
def reset_wifi_interfaces():
    try:
        sta = network.WLAN(network.STA_IF)
        ap = network.WLAN(network.AP_IF)

        if ap.active():
            print("⏳ Disabling AP interface...")
            ap.active(False)
            activity_light()
        
        if sta.active():
            print("⏳ Disconnecting STA interface...")
            sta.disconnect()
            activity_light()
            time.sleep(0.5)
            print("⏳ Deactivating STA interface...")
            sta.active(False)
            activity_light()

        print("✅ Interfaces reset successfully")

    except Exception as e:
        print("🚨 Error resetting interfaces:", e)

reset_wifi_interfaces()

ssid = "iphone_xr"
password = "C-982927"

print("⏳ Starting WiFi test...")
activity_light()

try:
    sta = network.WLAN(network.STA_IF)
    sta.active(True)
    activity_light()

    print(f"Connecting to SSID: {ssid}")
    sta.connect(ssid, password)
    activity_light()

    for i in range(15):
        if sta.isconnected():
            ip = sta.ifconfig()[0]
            print(f"✅ Connected! IP: {ip}")
            break
        print(f"⌛ Waiting... Status: {sta.status()}")
        time.sleep(1)
        activity_light()
    else:
        print("🚨 Could not connect.")
        print("📶 Final status:", sta.status())

except Exception as e:
    print("🚨 Error during WLAN operation:", e)