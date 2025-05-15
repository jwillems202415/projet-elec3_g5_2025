import network
from machine import Pin


def reset_wifi():
    # Désactive les interfaces Wi-Fi pour nettoyer l'état
    LED_R = Pin(6, Pin.OUT)
    LED_R.on()
    
    print("🔁 Resetting all Wi-Fi interfaces...")

    sta = network.WLAN(network.STA_IF)
    ap = network.WLAN(network.AP_IF)

    sta.active(False)
    ap.active(False)
    sta.disconnect()
    ap.disconnect()

    print("✅ Wi-Fi interfaces reset.")
    LED_R.off()