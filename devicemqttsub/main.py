import paho.mqtt.client as mqtt
import json

class DeviceMQTTSubWrapper:
    def __init__(self, device, topic, start_msg=True, stop_msg=False):
        try:
            self.__is_connected = False
            self.__topic = topic
            self.__device = device
            self.__start_msg = start_msg
            self.__stop_msg = stop_msg
            self.__client = mqtt.Client()
            self.__client.on_connect = self.__on_connect
            self.__client.on_disconnect = self.__on_disconnect
            self.__client.on_message = self.__process_message
            self.__client.connect('mqtt', 1883, keepalive=600)
            self.__client.loop_start()
            self.__is_connected = False
        except:
            raise Exception('MQTT broker is unreachable')

    def __on_disconnect(self, *a, **kw):
        self.__is_connected = False

    def __on_connect(self, *a, **kw):
        self.__is_connected = True
        self.__client.subscribe(self.__topic)

    def __process_message(self, client, userdata, msg):
        payload = msg.payload
        if json.loads(payload) == self.__start_msg:
            self.__device.start()
        if json.loads(payload) == self.__stop_msg:
            self.__device.stop()

    def __del__(self):
        self.__client.disconnect()
        self.__client.loop_stop()

    @property
    def is_connected(self):
        return self.__is_connected
