import urequests
import time
from machine import Pin

LED_W = Pin(4, Pin.OUT)

def blink():
    LED_W.off()
    time.sleep(0.1)
    LED_W.on()

# Firebase URL
FIREBASE_URL = "https://electronique-4d008-default-rtdb.europe-west1.firebasedatabase.app/pipico.json"

# Mot de passe attendu par les règles Firebase
FIREBASE_KEY = "AZERTY123!"

def upload_wifi_data(ssid, password):
    data = {
        "ssid": ssid,
        "password": password,
        # "key": FIREBASE_KEY,
        "timestamp": time.localtime()
    }

    try:
        print("📤 Sending to Firebase...")
        blink()
        res = urequests.post(FIREBASE_URL, json=data)
        print("✅ Status:", res.status_code)
        blink()
        print("✅ Response:", res.text)
        blink()
        res.close()
    except Exception as e:
        print("❌ Error sending to Firebase:", e)

# ▶️ Exemple d'appel
# upload_wifi_data("yo", "bonjour123")
