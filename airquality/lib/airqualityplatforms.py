import urequests as requests # https://github.com/jotathebest/micropython-lib/blob/master/urequests/urequests.py
import lib.constants as constants
from lib.umqtt import MQTTClient  # For use of MQTT protocol to talk to Adafruit IO
import time

# Base class for all platforms
class Platform:

    # Constructor
    def __init__(self):
        pass

    # Prepare API for specific platform
    def init_with_context(self, var_list):
        pass

    # Transmit dictionary of variable names and their values to platform
    def transmit(self, sensor_data):
        pass

    def report_battery_level(battery_level):
        pass


# With platformubidots using tutorial:
# https://help.ubidots.com/en/articles/961994-connect-any-pycom-board-to-ubidots-using-wi-fi-over-http



# Ubidots platform connecting over WIFI and sending data using HTTP
class PlatformUbidots(Platform):

    # Constructor
    def __init__(self):
        Platform.__init__(self)

    # Prepare and initialize with context
    def init_with_context(self, var_list):
        pass



    # Sends the request. Please reference the REST API reference https://ubidots.com/docs/api/
    def transmit(self, values):
        try:

            url = constants.UBIDOTS_API_URL + constants.AUTH_DEVICE_NAME
            print("Post to " + url)
            headers = {"X-Auth-Token": constants.AUTH_UBIDOTS_ACCESS_TOKEN, "Content-Type": "application/json"}

            # Build JSON - payload
            #create empty dictionary
            data = {}
            # Convert to json format
            for key in values.keys():
                data[key] = {"value": values[key]}

            # No need to send in case no variables exist...
            if data is not None:
                print(data)
                req = requests.post(url=url, headers=headers, json=data)
                return req.json()
            else:
                pass
        except:
            pass

    # For Ubidots, just populate a dictionary with a battery level variable and transmit
    def report_battery_level(self, battery_level):
        battery_level_data = {}
        battery_level_data[constants.UBIDOTS_BATTERY_VAR] = battery_level
        self.transmit(battery_level_data)

# Adafruit platform connecting over WIFI and sending data using  MQTT
class PlatformAdafruit(Platform):

    # Constructor
    def __init__(self):
        # Use the MQTT protocol to connect to Adafruit IO
        self.client = MQTTClient(constants.AIO_CLIENT_ID, constants.AIO_SERVER, constants.AIO_PORT, constants.AIO_USER, constants.AIO_KEY)
        self.client.connect()    # Connects to Adafruit IO using MQTT

    def getClient(self):
        return self.client

    # Prepare and initialize with context
    def init_with_context(self, var_list):
        pass

    # Send temperature and humidity to Adafruit alternately to stay under rate limit
    def transmit(self, values):
        gas = values[constants.BME_GAS_VAR_NAME ]        # gas(VOC) on BME
        humidity = values[constants.BME_HUMIDITY_VAR_NAME ]     # relative humidity BME
        airquality = values[constants.BME_AIRQUALITY_VAR_NAME ]#calculated airquality
        print(gas)
        print(humidity)
        print(airquality)
        try:
            self.client.publish(topic=constants.AIO_FEEDS['gas'], msg=str(gas))  # Send to Adafruit IO
            print("gas_score to adafruit IO sent via mqtt")
            self.client.publish(topic=constants.AIO_FEEDS['humidity'], msg=str(humidity))  # Send to Adafruit IO
            print("Humidity sent to adafruit IO via mqtt")
            self.client.publish(topic=constants.AIO_FEEDS['airquality'], msg=str(airquality))  # Send to Adafruit IO
            print("AirQuality sent adafruit IO sent via mqtt ")

        except Exception as e:
            print("FAILED")
