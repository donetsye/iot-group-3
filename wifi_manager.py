import network
import time
import ntptime

class WiFiManager:
    
    
    def __init__(self, ssid, password, display=None):
        self.ssid = ssid
        self.password = password
        self.oled = display
        self.ip_address = None
        
        
    def connect(self):
        wifi = network.WLAN(network.STA_IF)  # STA stands for station mode, in station mode device acts as a client that connects to another router
        # network.AP_IF instead puts the board into access point mode (microcontroller acts like its own mini-router, broadcasting its own Wi-Fi network)
        wifi.active(True)
        
        if not wifi.isconnected():
            print("Connecting to Wi-Fi")
            wifi.connect(self.ssid, self.password)
            
            while not wifi.isconnected():
                time.sleep(0.5)
                
        self.ip_address = wifi.ifconfig()[0]  #WLAN.ifconfig([(ip, subnet, gateway, dns)])  --> 0 is ip address
        self.gateway = wifi.ifconfig()[2]
        print(f"\nWi-Fi Connected. IP: {self.ip_address}")
        
        if self.oled:
            self.oled.show_internet_connection(self.ip_address, self.gateway)
        time.sleep(2)
        
        self._sync_time()


    def _sync_time(self):
        try:
            print("Synchronizing time")
            ntptime.settime()  # it ensures, what today's date/time is
            print("Time synced via ntp")
        except Exception as e:
            print(f"Time sync failed: {e}")
