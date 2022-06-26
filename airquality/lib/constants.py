import ubinascii
import machine
# Sensor variable names
BME_GAS_VAR_NAME = 'Gas'
BME_HUMIDITY_VAR_NAME = 'Humidity'
BME_AIRQUALITY_VAR_NAME = 'AirQuality'
'''
  Authentication constants, need to be changed in order to connect
  to WIFI, Ubidots account and for general device identification
'''
AUTH_WIFI_SSID = '...'
AUTH_WIFI_PWD = '...'
AUTH_UBIDOTS_ACCESS_TOKEN = '...'
AUTH_DEVICE_NAME = "AIR_QUALITY"
UBIDOTS_API_URL = "https://industrial.api.ubidots.com/api/v1.6/devices/"
UBIDOTS_BATTERY_VAR = "BatteryLevel"
# LED light on Lopy during during boot
CFG_LED_BOOT = 0x007f00
# Connect timeout for WIFI connection attempts
CFG_WIFI_CONNECT_TIMEOUT = 5000

# Interval, in seconds, to fetch sensor data and upload to platforms
CFG_SENSOR_TRANSMISSION_INTERVAL = 30.0

# Adafruit IO (AIO) configuration
AIO_SERVER = "io.adafruit.com"
AIO_PORT = 1883
AIO_USER = "..."
AIO_KEY = "..."
AIO_CLIENT_ID = ubinascii.hexlify(machine.unique_id())  # Can be anything
AIO_FEEDS = {'gas': '.../feeds/gas', 'humidity': '.../feeds/humidity','airquality': '.../feeds/airquality'}
