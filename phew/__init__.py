__version__ = "0.0.2"

# highly recommended to set a lowish garbage collection threshold
# to minimise memory fragmentation as we sometimes want to
# allocate relatively large blocks of ram.
import gc, os, machine
gc.threshold(50000)

# phew! the Pico (or Python) HTTP Endpoint Wrangler
from . import logging

from machine import Pin
# determine if remotely mounted or not, changes some behaviours like
# logging truncation
remote_mount = False
try:
  os.statvfs(".") # causes exception if remotely mounted (mpremote/pyboard.py)
except:
  remote_mount = True

LED_W = Pin(4, Pin.OUT)

def activity_light():
    """Makes the white led blink to indicate activity"""
    LED_W.off()
    time.sleep(0.01)
    LED_W.on()

def get_ip_address():
  import network
  try:
    return network.WLAN(network.STA_IF).ifconfig()[0]
  except:
    return None

def is_connected_to_wifi():
  import network, time
  wlan = network.WLAN(network.STA_IF)
  return wlan.isconnected()

# helper method to quickly get connected to wifi
def connect_to_wifi(ssid, password, timeout_seconds=10):
  import network, time

  statuses = {
    network.STAT_IDLE: "idle",
    network.STAT_CONNECTING: "connecting",
    network.STAT_WRONG_PASSWORD: "wrong password",
    network.STAT_NO_AP_FOUND: "access point not found",
    network.STAT_CONNECT_FAIL: "connection failed",
    network.STAT_GOT_IP: "got ip address"
  }
  print(f"DEBUG : Connecting to {ssid} with password {password}")
  wlan = network.WLAN(network.STA_IF)
  wlan.active(True)    
  wlan.connect(ssid, password)
  start = time.ticks_ms()
  status = wlan.status()

  logging.debug(f"  - {statuses[status]}")
  while not wlan.isconnected() and (time.ticks_ms() - start) < (timeout_seconds * 1000):
      current_status = wlan.status()
      activity_light()
      print(f"Status: {current_status} ({statuses.get(current_status, 'unknown')})")
      time.sleep(1)
  print(f"[!] Final status: {wlan.status()} ({statuses.get(wlan.status(), 'unknown')})")
    


  if wlan.status() == network.STAT_GOT_IP:
    return wlan.ifconfig()[0]
  logging.debug(f"  - Final status: {statuses.get(wlan.status(), wlan.status())}")

  return None


# helper method to put the pico into access point mode
def access_point(ssid, password = None):
  import network

  # start up network in access point mode  
  wlan = network.WLAN(network.AP_IF)
  wlan.config(essid=ssid)
  if password:
    wlan.config(password=password)
  else:    
    wlan.config(security=0) # disable password
  wlan.active(True)

  return wlan
