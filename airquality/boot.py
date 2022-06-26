from lib.airqualitywifi import wifi_enable
import pycom
import lib.constants as constants

pycom.heartbeat(False)
pycom.rgbled(constants.CFG_LED_BOOT)
wifi_enable(constants.CFG_WIFI_CONNECT_TIMEOUT)
