from devicemqttsub import DeviceMQTTSubWrapper
from pioutput import MotorAdaptor
from time import sleep
import os

if __name__ == '__main__':
    pin = int(os.environ.get('pin'))
    input = os.environ.get('input')
    motor = MotorAdaptor(pin_number=pin, max_runtime=30, cooldown=30)
    mqtt = DeviceMQTTSubWrapper(device=motor, topic=input, start_msg=1, stop_msg=0)
    while True:
        sleep(1)
