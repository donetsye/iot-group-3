# wi-fi credentials
WIFI_SSID = 'zhenchikk'
WIFI_PASS = 'blablabla'

#mqtt broker settings
MQTT_DEVICE_NAME = "esp32-group03"  
MQTT_BROKER_IP = "b12450ae831942678407c69bd234209f.s1.eu.hivemq.cloud"
MQTT_PORT = 8883                
MQTT_USER = "Gruppe03"
MQTT_PASS = "Admin1234"

#mqtt topics
BASE_TOPIC = "group3/sensors/" #topics for each town will be created dynamically in main.py (group3/sensors/tettnang...)
LAST_WILL_TOPIC = 'group3/sensors/status'
