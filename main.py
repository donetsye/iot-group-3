import time
import machine
import ujson
from machine import Pin

from sensors import WeatherSensors
from display import OledDisplay
from sealevel_api import SeaLevelPressure
from wifi_manager import WiFiManager
from mqtt_manager import MQTTManager

import config

LOCATIONS = ["Tettnang", "Meckenbeuren", "Kressbronn"]
current_loc_index = 0

button = Pin(17, Pin.IN, Pin.PULL_DOWN)

oled = OledDisplay()
sensors = WeatherSensors()  
api_weather = SeaLevelPressure()


# network classes
wifi = WiFiManager(config.WIFI_SSID, config.WIFI_PASS, display=oled)

mqtt = MQTTManager(
    client_id = config.MQTT_DEVICE_NAME,
    broker = config.MQTT_BROKER_IP,
    port = config.MQTT_PORT,
    user = config.MQTT_USER,
    password = config.MQTT_PASS,
    base_topic = config.BASE_TOPIC,
    last_will_topic = config.LAST_WILL_TOPIC,
    display = oled
)


def restart_esp():
    print("Critical Error. Restarting in 5 seconds")
    oled.show_error()
    time.sleep(5)
    machine.reset()


try:
    print("Starting Setup")
    wifi.connect()
    mqtt.connect()
    
    oled.show_station(current_loc_index + 1, LOCATIONS[current_loc_index])
    print(f"Current location: {LOCATIONS[current_loc_index]}")
    
except Exception as e:
    print(f"Startup error: {e}")
    restart_esp()



print("Initial button state:", button.value())  #debugging



#main loop
while True:
    if button.value() == 1: # constantly loops, waiting for the button pin to drop to 0 (which means the button is pressed down, connecting the circuit to Ground)
        time.sleep(0.05) # debounce the first press
        
        if button.value() == 1: #yes/no check
            # wait for the user to release the first click
            while button.value() == 1: # holding pattern
                time.sleep(0.02) 
            
            # start the doubleclick waiting window
            double_click_detected = False
            #wait_timer = 0.0
            start_time = time.ticks_ms() # Record the exact starting millisecond
            
            while time.ticks_diff(time.ticks_ms(), start_time) < 400: #gives 400 milliseconds to press the button a second time
                if button.value() == 1:
                    # second press detected, debounce it
                    time.sleep(0.05)
                    if button.value() == 1:
                        double_click_detected = True
                        
                        
                        # wait for the user to release second click
                        while button.value() == 1:
                            time.sleep(0.02)
                        break # exit the waiting window early

            if double_click_detected:
                # double click to switch location
                current_loc_index += 1
                if current_loc_index >= len(LOCATIONS):
                    current_loc_index = 0 #infinite loop through locations, if we exceeded or location's length
                
                loc_number = current_loc_index + 1
                current_location_name = LOCATIONS[current_loc_index]
                
                oled.show_station(loc_number, current_location_name)
                print(f"Location changed to: {current_location_name} (ID: {loc_number})")
                
            else:
                # single click to send data to broker
                loc_number = current_loc_index + 1
                current_location_name = LOCATIONS[current_loc_index]
                print(f"\nReading sensors for {current_location_name}")
                
                oled.show_sending(loc_number, current_location_name)
                
                try:
                    live_sea_level = api_weather.fetch_current(current_location_name)
                    sensor_data = sensors.read_all(current_sea_level=live_sea_level)
                    
                    sensor_data["device"] = config.MQTT_DEVICE_NAME
                    sensor_data["location"] = current_location_name
                    sensor_data["location_id"] = loc_number
                    sensor_data["timestamp"] = time.time() + 946684800 #unix time stamp, 1.1.1970
                    
                    payload = ujson.dumps(sensor_data)  
                
                    published_topic = mqtt.publish_sensor_data(current_location_name, payload)
                    
                    print(f"Successfully sent")
                    oled.show_success(loc_number, current_location_name)
                    
                    print(f"Topic: {published_topic}")
                    print(f"Payload: {payload}")
                    
                    time.sleep(1)
                    oled.show_station(loc_number, current_location_name)
                    
                except OSError:
                    print("Connection lost. Attempting Wi-Fi and MQTT reconnect")
                    try:
                        wifi.connect()
                        mqtt.connect()
                    except:
                        restart_esp()
                except Exception as e:
                    print(f"Error reading sensors: {e}")

    time.sleep(0.05)


