import paho.mqtt.client as mqtt
import json

class DeviceMQTTSubWrapper:
    def __init__(self, device, topic, start_msg=True, stop_msg=False):
        try:
            self.__is_connected = False
            self.topic = topic
            self.device = device
            self.start_msg = start_msg
            self.stop_msg = stop_msg
            self.client = mqtt.Client()
            self.client.on_connect = self.on_connect
            self.client.on_disconnect = self.on_disconnect
            self.client.on_message = self.process_message
            self.client.connect('mqtt', 1883, keepalive=600)
            self.client.loop_start()
            self.__is_connected = False
        except:
            raise Exception('MQTT broker is unreachable')

    def on_disconnect(self, *a, **kw):
        self.__is_connected = False

    def on_connect(self, *a, **kw):
        self.__is_connected = True
        self.client.subscribe(self.topic)

    def process_message(self, client, userdata, msg):
        payload = msg.payload
        if json.loads(payload) == self.start_msg:
            self.device.start()
        if json.loads(payload) == self.stop_msg:
            self.device.stop()

    def __del__(self):
        self.client.disconnect()
        self.client.loop_stop()

    @property
    def is_connected(self):
        return self.__is_connected
