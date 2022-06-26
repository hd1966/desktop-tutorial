# Source https://github.com/pimoroni/bme680-python
import time
from machine import Pin
from bme680 import *
from machine import I2C,SPI,Pin
import lib.constants as constants


class BME:

    def __init__(self,  calibration_time=500):
        self.sensor = BME680_I2C(I2C())
        #cs = Pin("P11", Pin.OUT, value=1) - for SPI
        #spi = SPI(0, mode=SPI.MASTER, baudrate=400000, pins=("P10", "P9", "P8"))
        #self.sensor = BME680_SPI(spi, cs)
        self.vars = []
        #register variables (voc,airquality and humidity)
        self.humidity_var = self._register_var(constants.BME_HUMIDITY_VAR_NAME)
        self.gas_var = self._register_var(constants.BME_GAS_VAR_NAME)
        self.airquality_var = self._register_var(constants.BME_AIRQUALITY_VAR_NAME)
        # calibration
        self._warm_up(calibration_time)

    def get_vars(self):
        return self.vars
    # Register variable
    def _register_var(self, name):
        self.vars.append(name)
        return name

    # Collect sensor data
    def read(self, sensor_data):

        # Get air condition values
        gas, humidity, pressure, air_quality = self._get_values()

        # Use variable names as keys in sensor_data dictionary
        sensor_data[self.gas_var] = gas
        sensor_data[self.humidity_var] = humidity
        sensor_data[self.airquality_var]=air_quality

        # Print all
        print('Gas:', gas, 'ppm')
        print('Humidity:', humidity, '%')
        print('pressure:', pressure, 'hPa')
        print('air_quality:', air_quality, 'IAQ')
        print()
    #calibration
    def _warm_up(self, calibration_time):
        start_time = time.time()
        curr_time = time.time()
        burn_in_time = calibration_time
        burn_in_data = []
        print('Collecting gas resistance burn-in data for', calibration_time // 60
        , 'mins and', calibration_time %60, 'seconds')
        while curr_time - start_time < burn_in_time:
            curr_time = time.time()
            burn_in_data.append(self.sensor.gas)
            print('Gas: {0} Ohms'.format(self.sensor.gas))
            time.sleep(1)
        print(burn_in_data)
        self.gas_baseline = sum(burn_in_data[-5:]) / 5.0 #average value
        print('Gas baseline: {0} Ohms'.format(self.gas_baseline))
        # Set the humidity baseline to 40%, an optimal indoor humidity.
        self.hum_baseline = 40.0
        # This sets the balance between humidity and gas reading in the
        # calculation of air_quality_score (25:75, humidity:gas)
        self.hum_weighting = 0.25
# calculate air quality  with weighting (25% humidity and 75% gas). To calculate
# air quality , calculate first distance between
# measured humidity and hum_baseline(40.0 - ideal humidity) and
# distance between measured gas(voc) and gas_baseline (calculated with calibration).
#Then use weighting and calculate air quality
    def _get_values(self):
        #if self.sensor.get_sensor_data() and self.sensor.data.heat_stable:
        gas = self.sensor.gas
        gas_offset = self.gas_baseline - gas
        hum = self.sensor.humidity
        hum_offset = hum - self.hum_baseline

            # Calculate hum_score as the distance from the hum_baseline.
        if hum_offset > 0:
            hum_score = (100 - self.hum_baseline - hum_offset)
            hum_score /= (100 - self.hum_baseline)
            hum_score *= (self.hum_weighting * 100)

        else:
            hum_score = (self.hum_baseline + hum_offset)
            hum_score /= self.hum_baseline
            hum_score *= (self.hum_weighting * 100)

            # Calculate gas_score as the distance from the gas_baseline.
        if gas_offset > 0:
            gas_score = (gas / self.gas_baseline)
            gas_score *= (100 - (self.hum_weighting * 100))

        else:
            gas_score = 100 - (self.hum_weighting * 100)

            # Calculate air_quality_score.
        air_quality_score = hum_score + gas_score

        return gas, hum, self.sensor.pressure, air_quality_score
