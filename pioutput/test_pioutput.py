import pytest
from unittest.mock import MagicMock
from unittest.mock import patch
from pioutput import MotorAdaptor
from time import sleep
from threading import Thread

class TestPiOutputAdaptor:

    def test_assigns_correct_pin_number(self):
        fake_pin_constructor = MagicMock()
        fake_pin_constructor.initialized_with = lambda a: a in fake_pin_constructor.call_args.args
        pin_number = 1583
        with patch('pioutput.main.LED', new=fake_pin_constructor):
            MotorAdaptor(pin_number)
            assert fake_pin_constructor.initialized_with(pin_number)

    def test_turns_pin_ON_when_STARTING_motor(self, fake_pin, motor):
        motor.start()
        assert fake_pin.on.called

    def test_turns_pin_OFF_when_STOPPING_motor(self, fake_pin, motor):
        motor.start()
        motor.stop()
        assert fake_pin.off.called

    def test_cannot_start_motor_when_already_running(self, fake_pin, motor):
        motor.start()
        assert fake_pin.on.call_count == 1
        motor.start()
        assert fake_pin.on.call_count == 1

    def test_cannot_stop_motor_when_already_stopped(self, fake_pin, motor):
        motor.start()
        motor.stop()
        assert fake_pin.off.call_count == 1
        motor.stop()
        assert fake_pin.off.call_count == 1
    
    def test_using_adaptor_without_gpiozero_installed_throws_a_meaningful_exception(self):
        with pytest.raises(Exception) as e:
            MotorAdaptor(5)
        assert e.value.args[0] == 'This adaptor requires gpiozero library to be installed'


@pytest.mark.usefixtures('patch_led')
@pytest.mark.usefixtures('patch_thread')
@pytest.mark.usefixtures('patch_time')
@pytest.mark.usefixtures('patch_sleep')
class TestPiOutputTimeouts:
    def test_can_limit_maximum_continuous_motor_run(self, fake_pin, fake_time, fake_thread):
        motor = MotorAdaptor(1, max_runtime=10)
        motor.start()
        assert not fake_pin.off.called
        fake_time.forward(seconds=15)
        fake_thread.wait_to_finish()
        assert fake_pin.off.called

    def test_enforce_cooldown_period_after_maxing_out_runtime(self, fake_pin, fake_time, fake_thread):
        motor = MotorAdaptor(1, max_runtime=10, cooldown=30)
        motor.start()
        assert fake_pin.on.call_count == 1
        fake_time.forward(seconds=20)
        # assert fake_pin.off.called
        motor.start()
        assert fake_pin.on.call_count == 1
    
    def test_can_restart_after_cooldown(self, fake_pin, fake_time, fake_thread):
        motor = MotorAdaptor(1, max_runtime=10, cooldown=30)
        motor.start()
        assert fake_pin.on.call_count == 1
        fake_time.forward(seconds=20)
        fake_thread.wait_to_finish()
        fake_time.forward(seconds=60)
        motor.start()
        assert fake_pin.on.call_count == 2
    
    def test_do_not_enforce_cooldown_if_ran_for_a_short_time(self, fake_pin, fake_time, fake_thread):
        motor = MotorAdaptor(1, max_runtime=10, cooldown=30)
        motor.start()
        assert fake_pin.on.call_count == 1
        fake_time.forward(seconds=5)
        motor.stop()
        motor.start()
        assert fake_pin.on.call_count == 2

@pytest.fixture
def patch_led(fake_pin):
    with patch('pioutput.main.LED', return_value=fake_pin):
        yield

@pytest.fixture
def patch_thread(fake_thread):
    with patch('pioutput.main.Thread', new=fake_thread):
        yield

@pytest.fixture
def patch_time(fake_time):
    with patch('pioutput.main.time', new=fake_time):
        yield

@pytest.fixture
def patch_sleep():
    with patch('pioutput.main.sleep'):
        yield

# in gpiozero library a good pin writer is an LED
# so we use LED-like properties in this adaptor
@pytest.fixture
def fake_pin():
    pin_writer = MagicMock()
    pin_writer.on = MagicMock()
    pin_writer.off = MagicMock()
    yield pin_writer

@pytest.fixture
def motor(fake_pin):
    with patch('pioutput.main.LED', return_value=fake_pin):
        yield MotorAdaptor(12345)

@pytest.fixture
def fake_time():
    f_time = MagicMock(return_value=500)
    def forward(seconds):
        f_time.return_value += seconds
    f_time.forward = forward
    yield f_time

@pytest.fixture
def fake_thread():
    class FT:
        def __new__(cls, target):
            cls.thread = Thread(target=target)
            return super(FT, cls).__new__(cls)
        @classmethod
        def start(cls):
            cls.thread.start()
        @classmethod
        def wait_to_finish(cls):
            cls.thread.join()
    return FT
