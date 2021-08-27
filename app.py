from devicemqttsub import DeviceMQTTSubWrapper
from pioutput import MotorAdaptor
from time import sleep
import os

if __name__ == '__main__':
    pin = int(os.environ.get('PIN','27'))
    input = os.environ.get('INPUT','input')
    max_runtime = int(os.environ.get('MAX_ON_TIME','30'))
    cooldown = int(os.environ.get('COOLDOWN','30'))
    motor = MotorAdaptor(pin_number=pin, max_runtime=max_runtime, cooldown=cooldown)
    mqtt = DeviceMQTTSubWrapper(device=motor, topic=input, start_msg=1, stop_msg=0)
    while True:
        sleep(1)
