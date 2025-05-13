import network
def reset_wifi():

    # Désactive les interfaces Wi-Fi pour nettoyer l'état
    print("🔁 Resetting all Wi-Fi interfaces...")

    sta = network.WLAN(network.STA_IF)
    ap = network.WLAN(network.AP_IF)

    sta.active(False)
    ap.active(False)
    sta.disconnect()
    ap.disconnect()

    print("✅ Wi-Fi interfaces reset.")
    
