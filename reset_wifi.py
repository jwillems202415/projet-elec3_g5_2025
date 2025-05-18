from machine import Pin
import time

def reset_wifi():
    """Function used to reset all Wi-fi interfaces of the Pico W, terminating any active connection"""
    import network
    from machine import Pin

    LED_W = Pin(4, Pin.OUT)

    def activity_light():
        """Makes the white led blink to indicate activity"""
        LED_W.off()
        time.sleep(0.01)
        LED_W.on()

    # Désactive les interfaces Wi-Fi pour nettoyer l'état
    
    print("🔁 Resetting all Wi-Fi interfaces...")
    activity_light()
    
    # Interfaces initialization
    sta = network.WLAN(network.STA_IF) # Station (STA) interface (used to connect to existing Wi-Fi networks).
    ap = network.WLAN(network.AP_IF) # Access Point (AP) interface (used to create a Wi-Fi network that other devices can join).

    # Deactivation of both interfaces, thus resetting their states
    activity_light()
    sta.active(False)
    activity_light()
    ap.active(False)

    # Termination of any active Wi-Fi connection on both interfaces
    sta.disconnect()
    activity_light()
    ap.disconnect()
    activity_light()

    print("✅ Wi-Fi interfaces reset.")