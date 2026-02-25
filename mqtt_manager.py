from umqtt.simple import MQTTClient
import time
import ujson

class MQTTManager:
    def __init__(self, client_id, broker, port, user, password, base_topic, last_will_topic, display=None):
        self.client_id = client_id
        self.broker = broker
        self.port = port
        self.user = user
        self.password = password
        self.base_topic = base_topic
        self.last_will_topic = last_will_topic
        self.oled = display
        self.client = None

    def connect(self):
        print(f"Connecting to {self.broker}")
        
        self.client = MQTTClient(
            client_id=self.client_id,
            server=self.broker,
            port=self.port,
            user=self.user,
            password=self.password,
            keepalive=60,
            ssl=True,  #encrypts connection 
            ssl_params={'server_hostname': self.broker} # since one physical server might host many different brokers, this tells the server exactly which security certificate to hand back to device during the handshake
        )
        
        #send status as json
        offline_dict = {
            "device": self.client_id,
            "status": "offline"
        }
        
        offline_json = ujson.dumps(offline_dict)  # return obj represented as a JSON string
        
        self.client.set_last_will(
            topic = self.last_will_topic,
            msg=offline_json,
            retain = True,  # server publishes will message and removes it from the session (if client who cares about it is offline, he will miss it); to avoid it -> send messages as retained (it will be stored on server)
            qos = 1  # at least once
        )
         #qos0 - no delivery guarantee
         #qos1 - at least once, may result in duplicates
         #qos2 - exactly once, highest reliability level
         #higher provides better guarantee but increases network overhead and latency
        
        self.client.connect()
        
        online_dict = {
            "device": self.client_id,
            'status': 'online'
        }
        
        online_json = ujson.dumps(online_dict)
    
        self.client.publish(
            topic = self.last_will_topic,
            msg = online_json,
            retain = True,
            qos = 1
        )
        
        print("Connected to MQTT Broker")
        
        if self.oled:
            self.oled.show_mqtt_connect()
        time.sleep(2)

    def publish_sensor_data(self, location_name, payload):
        # builds dynamic topic and publishes the payload
        loc_name = location_name.lower()
        dynamic_topic = self.base_topic + loc_name
        
        self.client.publish(dynamic_topic, payload)
        return dynamic_topic
