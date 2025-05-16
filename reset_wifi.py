def reset_wifi():
    """Function used to reset all Wi-fi interfaces of the Pico W, terminating any active connection"""
    import network
    from machine import Pin
    # Désactive les interfaces Wi-Fi pour nettoyer l'état
    LED_R = Pin(6, Pin.OUT)
    LED_R.on()
    
    print("🔁 Resetting all Wi-Fi interfaces...")

    # Interfaces initialization
    sta = network.WLAN(network.STA_IF) # Station (STA) interface (used to connect to existing Wi-Fi networks).
    ap = network.WLAN(network.AP_IF) # Access Point (AP) interface (used to create a Wi-Fi network that other devices can join).

    # Deactivation of both interfaces, thus resetting their states
    sta.active(False)
    ap.active(False)
    
    # Termination of any active Wi-Fi connection on both interfaces
    sta.disconnect()
    ap.disconnect()

    print("✅ Wi-Fi interfaces reset.")
    LED_R.off()