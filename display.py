from machine import I2C, Pin
import ssd1306

class OledDisplay:
    def __init__(self, scl_pin=22, sda_pin=21):
        self.i2c = I2C(0, sda=Pin(sda_pin), scl=Pin(scl_pin))
        self.display = ssd1306.SSD1306_I2C(128, 64, self.i2c)
        
    def show_internet_connection(self, ip, gateway):
        self.display.fill(0)
        self.display.text("Wi-Fi CONNECTED", 2, 5) # get pixel at x=0, y=5
        self.display.hline(0, 25, 160, 1)  
        self.display.text(f"IP:{ip}", 5, 30)
        self.display.hline(0, 40, 160, 1)
        self.display.text(f"GW:{gateway}", 5, 45)
        self.display.hline(0, 55, 160, 1)
        self.display.show()

    def show_station(self, station_num, city_name):
        self.display.fill(0) 
        self.display.text("Weather Station", 4, 5)
        self.display.hline(0, 20, 160, 1)  
        self.display.text(f"Loc{station_num}: {city_name}", 0, 30)
        self.display.text("Ready", 35, 50)
        self.display.show()
        
    def show_sending(self, station_num, city_name):
        self.display.fill(0)
        self.display.text("Weather Station", 4, 5)
        self.display.hline(0, 20, 160, 1)  
        self.display.text(f"Loc{station_num}: {city_name}", 0, 30)
        self.display.text("Sending Data", 8, 50)
        self.display.show()
        
    def show_success(self, station_num, city_name):
        self.display.fill(0)
        self.display.text("Weather Station", 4, 5)
        self.display.hline(0, 20, 160, 1)  
        self.display.text(f"Loc{station_num}: {city_name}", 0, 30)
        self.display.text("Successfuly sent", 0, 50)
        self.display.show()
        
    def show_mqtt_connect(self):
        self.display.fill(0)
        self.display.text("MQTT-Broker", 20, 5)
        self.display.text("CONNECTED", 25, 35)
        self.display.show()
        
    def show_error(self):
        self.display.fill(0) 
        self.display.text("CRASH", 36, 10)
        self.display.hline(0, 20, 160, 1)  
        self.display.text("Network Dropped", 4, 35)
        self.display.text("Restarting", 15, 50)
        self.display.show()
    
    
