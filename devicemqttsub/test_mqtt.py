import pytest
import json
from unittest.mock import MagicMock, patch
from devicemqttsub import DeviceMQTTSubWrapper as DeviceSub


class TestWrapperWithException:
    def test_raise_exception_when_mqtt_is_unreachable(self, fake_device):
        with pytest.raises(Exception) as e:
            DeviceSub(device=fake_device, topic='remote-sensor')
        assert e.value.args[0] == 'MQTT broker is unreachable'

@pytest.mark.usefixtures('patch_mqtt')
class TestWrapper:
    def test_can_connect_to_mqtt_server(self, fake_device, fake_mqtt_client):
        mqtt = DeviceSub(device=fake_device, topic='remote-sensor', start_msg=15, stop_msg=-10)
        fake_mqtt_client.on_connect()
        assert mqtt.is_connected

    def test_STARTS_device_when_receives_START_signal(self, fake_device, fake_mqtt_client):
        DeviceSub(device=fake_device, topic='remote-sensor', start_msg=15, stop_msg=-10)
        fake_mqtt_client.on_message(None, None, FakeMQTTMessage('15'))
        assert fake_device.start.called

    def test_STOPS_device_when_receives_STOP_signal(self, fake_device, fake_mqtt_client):
        DeviceSub(device=fake_device, topic='remote-sensor', start_msg=15, stop_msg=-10)
        fake_mqtt_client.on_message(None, None, FakeMQTTMessage('-10'))
        assert fake_device.stop.called
        assert not fake_device.start.called

    def test_can_use_json_object_as_signals(self, fake_device, fake_mqtt_client):
        DeviceSub(device=fake_device, topic='remote-sensor', start_msg={"device": 15, "active": True}, stop_msg=-10)
        fake_mqtt_client.on_message(None, None, FakeMQTTMessage('{"device":15, "active":true}'))
        assert fake_device.start.called


@pytest.fixture
def fake_device():
    return MagicMock()

@pytest.fixture
def fake_mqtt_client():
    client = MagicMock()
    client.get_publish_payload = lambda: client.publish.call_args.kwargs.get('payload')
    client.get_publish_topic = lambda: client.publish.call_args.kwargs.get('topic')
    return client

@pytest.fixture()
def patch_mqtt(fake_mqtt_client):
    fake_mqtt = MagicMock()
    fake_mqtt.Client = MagicMock(return_value=fake_mqtt_client)
    with patch('devicemqttsub.main.mqtt', new=fake_mqtt):
        yield

class FakeMQTTMessage:
    def __init__(self, payload):
        self.payload = payload
    def payload(self):
        return self.payload
