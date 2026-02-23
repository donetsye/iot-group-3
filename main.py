import time
import machine
import ujson
from umqtt.simple import MQTTClient
from airpressure import WeatherSensors 

MQTT_SERVER = "broker.hivemq.com"
CLIENT_ID = "esp32_projekt_temp"
TOPIC_DATA = "sensor/temp"



def connect_mqtt():
    global client
    print(f"Verbinde mit Broker {MQTT_SERVER}...")
    client = MQTTClient(CLIENT_ID, MQTT_SERVER)
    client.connect()
    print("Verbunden mit MQTT Broker!")



def restart_esp():
    print("Fehler! Starte neu in 5 Sekunden...")
    time.sleep(5)
    machine.reset()




try:
    print("Initialisiere Sensoren...")
    sensors = WeatherSensors()  # create sensor object
except Exception as e:
    print(f"Sensor Fehler: {e}")
    restart_esp()



try:
    connect_mqtt()
except OSError as e:
    restart_esp()




while True:
    try:
        sensor_data = sensors.read_all()
        
        # convert python dictionary into a JSON string
        payload = ujson.dumps(sensor_data)
        
        # publish to the broker
        client.publish(TOPIC_DATA, payload)
        print(f"Gesendet: {payload}")
        
    except OSError as e:
        print("Sensor- oder Netzwerkfehler. Versuche Reconnect...")
        try:
            client.connect()
        except:
            restart_esp()
            
    time.sleep(10)
