import urequests
import time

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
        res = urequests.post(FIREBASE_URL, json=data)
        print("✅ Status:", res.status_code)
        print("✅ Response:", res.text)
        res.close()
    except Exception as e:
        print("❌ Error sending to Firebase:", e)

# ▶️ Exemple d'appel
# upload_wifi_data("yo", "bonjour123")
