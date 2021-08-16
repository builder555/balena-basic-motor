from devicemqttsub import DeviceMQTTSubWrapper
from pioutput import MotorAdaptor
from time import sleep

if __name__ == '__main__':
    motor = MotorAdaptor(pin_number=27, max_runtime=30, cooldown=30)
    mqtt = DeviceMQTTSubWrapper(device=motor, topic='control', start_msg=1, stop_msg=0)
    while True:
        sleep(1)
