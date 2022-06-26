from lib.airqualityplatforms import PlatformUbidots
from lib.airqualityplatforms import PlatformAdafruit
import lib.bme
from lib.airqualitywifi import wifi_is_connected
import pycom
import machine
import time
import lib.constants as constants
from machine import I2C, Pin,SPI
from lib.bme import BME
from lib.umqtt import MQTTClient  # For use of MQTT protocol to talk to Adafruit IO
from lib.buzzer import Buzzer
#led
led=Pin("P22", Pin.OUT,pull = Pin.PULL_DOWN)
#buzzer
buzz=Buzzer(Pin("P23"))
cs=Pin("P11", Pin.OUT, value=1)
bme = BME(calibration_time=5)
# Dictionary of sensor data
sensor_data = {}
# platforms in this case ubidots and adafruit
all_platforms = []
# List of all sensor's variables
sensor_var_list = bme.get_vars()
# Add ubidots platform
all_platforms.append(PlatformUbidots())
adf=PlatformAdafruit()
# Add adafruiplatform platform
all_platforms.append(adf)
# Allow all platforms to prepare, pass the variable list in case any platform needs it
for platform in all_platforms:
    platform.init_with_context(sensor_var_list)
# Main loop
while True:
    led.value(0)
    # Reset device in case we lost WIFI
    if not wifi_is_connected():
        machine.reset()
    adf.getClient().check_msg()# Action a message if one is received. Non-blocking.
    # New dictionary each cycle, populated by sensors
    sensor_data = {}
    read_result=bme.read(sensor_data)
    if sensor_data[constants.BME_AIRQUALITY_VAR_NAME] <95.0:
        buzz.play_bls()#play song
        led.value(1)
    # Iterate all registered platforms and transmit data from sensors
    for platform in all_platforms:
        platform.transmit(sensor_data)
    # Sleep until next cycle
    time.sleep(constants.CFG_SENSOR_TRANSMISSION_INTERVAL)
