from network import WLAN
import machine
import lib.constants as constants
import pycom

def wifi_is_connected():
    wlan = WLAN(mode=WLAN.STA)
    return wlan.isconnected()

def wifi_enable(connect_timeout):

    # Enable wifi
    wlan = WLAN(mode=WLAN.STA)

    nets = wlan.scan()

    for net in nets:
        if net.ssid == constants.AUTH_WIFI_SSID:
            print('Connect to network ' + constants.AUTH_WIFI_SSID + '...')
            wlan.connect(net.ssid, auth=(net.sec, constants.AUTH_WIFI_PWD), timeout=connect_timeout)

            # Check status and idle while not connected...
            while not wlan.isconnected():
                machine.idle()

            print('Connected to ' + constants.AUTH_WIFI_SSID)
            print(wlan.ifconfig())
            break
