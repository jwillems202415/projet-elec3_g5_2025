# import network
# import time
# import utime

# ssid = "pico_test"
# password = "12345678"

# print("→ Starting WiFi test...")

# # try : 
# wlan = network.WLAN(network.STA_IF)

# wlan.active(True)
# wlan.connect(ssid, password)

# for i in range(15):
#     status = wlan.status()
#     print(f"Status: {status}")
#     if wlan.isconnected():
#         print("✅ Connected! IP:", wlan.ifconfig()[0])
#         break
#     time.sleep(1)
# if wlan.isconnected():
#     print("✅ Connected to local network")
#     print("IP address:", wlan.ifconfig()[0])
# else:
#     print("❌ Not connected")

# print("❌ Final status:", wlan.status())
# utime.sleep(5)
# print("→ Disconnecting...")
# wlan.active(False)
# wlan.disconnect()
# # except Exception as e:
# print("❌ Error initializing WLAN:")
# wlan = None
import network
import time
import utime

# ❗ Désactive AP mode s'il est actif
network.WLAN(network.AP_IF).active(False)
network.WLAN(network.STA_IF).active(False)
network.WLAN(network.STA_IF).disconnect()
network.WLAN(network.AP_IF).disconnect()

ssid = "pico_test"
password = "12345678"

print("→ Starting WiFi test...")

try:
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)

    for i in range(15):
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
    print("→ Disconnecting...")
    wlan.disconnect()
    wlan.active(False)

except Exception as e:
    print("❌ Error initializing WLAN:", e)
    wlan = None
