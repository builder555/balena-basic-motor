from abc import ABC, abstractmethod
class AbstractMotor(ABC):

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass
