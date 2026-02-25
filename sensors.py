from machine import I2C, Pin
import time, math
import bme280 #bme280 bosch library, for this project is also compatible, just like bmp280;
import ahtx0

class WeatherSensors:
    def __init__(self, scl_pin=22, sda_pin=21, sea_level_pressure=1021):
        self.i2c = I2C(0, sda=Pin(sda_pin), scl=Pin(scl_pin))
        self.bme = bme280.BME280(address=0x77, i2c=self.i2c)
        self.sensor_temp_hum = ahtx0.AHT20(self.i2c)
        self.sea_level_pressure = sea_level_pressure
        
        time.sleep(0.5)

    
    def read_all(self, current_sea_level=1013.25):  # 1013.25 default value (mean sea value MSL in the ISA)
        # read and parse pressure and altitude
        data = self.bme.values[1]  
        pressure = float(data.replace('hPa', ''))
        
        # use live api value for the altitude calculation
        altitude = 44330.0 * (1.0 - math.pow(pressure / current_sea_level, 1 / 5.255))
        
        # read temperature and humidity
        temp = self.sensor_temp_hum.temperature
        hum = self.sensor_temp_hum.relative_humidity
        
        # return all data as dictionary
        return {
            "temperature": round(temp, 1),
            "humidity": round(hum, 1),
            "pressure": round(pressure, 2),
            "altitude": round(altitude, 1)
        }


