from machine import Pin
import json
import time
import urequests
import _thread

FIREBASE_URL = "https://electronique-4d008-default-rtdb.europe-west1.firebasedatabase.app/pipico.json"

LED_R = Pin(6, Pin.OUT)

def get_victims_count_from_firebase():
    """Getting the number of victims from the database"""
    try:
        response = urequests.get(FIREBASE_URL)
        
        if response.status_code == 200:
            data = response.json()
            response.close()
            
            # Compter le nombre d'entrées dans les données
            if data is None:
                count = 0
            elif isinstance(data, dict):
                count = len(data)
            elif isinstance(data, list):
                count = len(data)
            else:
                count = 0
                
            print(f"Number of victims: {count}")
            return count
        else:
            LED_R.on()
            print(f"Error when fetching data: {response.status_code}")
            response.close()
            return 0
    except Exception as e:
        print(f"Exception when fetching data: {e}")
        LED_R.on()
        try:
            response.close()
        except:
            pass
        # En cas d'erreur, retourner 0
        return 0

def display_victims_count_for_duration(display_value, duration_seconds):
    try:
        bcd_pins = [Pin(n, Pin.OUT) for n in [18, 26, 22, 19]]
        digits = [Pin(27, Pin.OUT), Pin(28, Pin.OUT)]

        BCD_CODES = [
            [0, 0, 0, 0],  # 0
            [1, 0, 0, 0],  # 1
            [0, 1, 0, 0],  # 2
            [1, 1, 0, 0],  # 3
            [0, 0, 1, 0],  # 4
            [1, 0, 1, 0],  # 5
            [0, 1, 1, 0],  # 6
            [1, 1, 1, 0],  # 7
            [0, 0, 0, 1],  # 8
            [1, 0, 0, 1],  # 9
        ]

        def set_bcd(value):
            code = BCD_CODES[value]
            for pin, bit in zip(bcd_pins, code):
                pin.value(bit)

        # Ensure the number is an integer
        try:
            number = int(display_value)
        except:
            number = 0
        number = max(0, min(number, 99))

        # Extract digits
        if number < 10:
            left_digit = 0
            right_digit = number
        else:
            left_digit = (number // 10) % 10
            right_digit = number % 10

        start_time = time.time()
        while time.time() - start_time < duration_seconds:
            # Display left digit
            set_bcd(left_digit)
            digits[0].value(1)
            time.sleep(0.005)
            digits[0].value(0)

            # Display right digit
            set_bcd(right_digit)
            digits[1].value(1)
            time.sleep(0.005)
            digits[1].value(0)
    except Exception as e:
        print(f"Error in display: {e}")
        LED_R.on()
        try:
            LED_R.off()
            for digit in digits:
                digit.value(0)
        except:
            pass
        LED_R.on()

# Fonction pour afficher continuellement le nombre de victimes
def display_victims_count_loop():
    update_interval = 30 # Récupérer les données toutes les 30 secondes
    last_known_count = 0 # Variable pour stocker le dernier compte connu
    
    while True:
        try:
            count = get_victims_count_from_firebase()
            if count > 0 or count == 0 and last_known_count == 0:
                # Mettre à jour seulement si un nombre valide est reçu
                last_known_count = count
            
            # Afficher le nombre pendant l'intervalle de mise à jour
            display_time = 5
            cycles = max(1, update_interval // display_time)
            
            for _ in range(cycles):
                display_victims_count_for_duration(last_known_count, display_time)
                time.sleep(0.1)
            
        except Exception as e:
            print(f"Error in display loop: {e}")
            LED_R.on()
            # Afficher quand même la dernière valeur connue en cas d'erreur
            try:
                LED_R.off()
                display_victims_count_for_duration(last_known_count, 5)
            except:
                pass
                LED_R.on()
            time.sleep(5)

# Fonction pour démarrer l'affichage dans un thread séparé
def start_display():
    try:
        _thread.start_new_thread(display_victims_count_loop, ())
        print("Number of victims display started")
    except Exception as e:
        print(f"Error when starting the display: {e}")
        LED_R.on()
        try:
            time.sleep(2)
            LED_R.off()
            _thread.start_new_thread(display_victims_count_loop, ())
        except:
            LED_R.on()
            print("Could not start a thread for the display.")