from time import time, sleep
from threading import Thread
from .interface import AbstractMotor
try:
    from gpiozero import LED
except:
    LED = None

class MotorAdaptor(AbstractMotor):

    def __init__(self, pin_number, max_runtime=0, cooldown=0):
        assert LED, 'This adaptor requires gpiozero library to be installed'
        self.__motor = LED(pin_number)
        self.__is_motor_on = False
        self.__max_runtime = max_runtime
        self.__max_runtime_reached = False
        self.__thread = None
        self.__cooldown_time = cooldown
        self.__stop_time = 0

    def start(self):
        if self.__is_motor_on or self.__is_cooling_down:
            return
        self.start_time = time()
        self.__motor.on()
        self.__is_motor_on = True
        self.__thread = Thread(target = self.__monitor_motor)
        self.__thread.start()

    def stop(self):
        if not self.__is_motor_on:
            return
        self.__stop_time = time()
        self.__motor.off()
        self.__is_motor_on = False

    def __monitor_motor(self):
        while self.__is_motor_on:
            sleep(0.1)
            self.__max_runtime_reached = self.__runtime > self.__max_runtime
            if self.__max_runtime_reached:
                self.stop()

    @property
    def __runtime(self):
        return (time() - self.start_time)

    @property
    def __is_cooling_down(self):
        cooldown_time_is_set = self.__cooldown_time > 0
        if not (cooldown_time_is_set and self.__max_runtime_reached):
            return False
        reached_cooldown_limit = (time() - self.__stop_time) >= self.__cooldown_time
        return not reached_cooldown_limit
