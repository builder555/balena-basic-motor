### Balena Blocks: basic motor

Gets input from MQTT and either turns on or off a specific pin on a device.

Currently supports only Balena Fin and Raspberry Pi devices.

_Installation_

Add the following to your `docker-compose.yaml`:

```yaml
  basic-motor:
    privileged: true
    build: ./basic-motor
    restart: always
```

_Tests_

```bash
$ PIPENV_VENV_IN_PROJECT=1 pipenv install --dev
$ pipenv shell
$ pytest -vs
```

_Usage_

Device pin is activated when the block receives appropriate MQTT message.

Given the code
```python
>>> from devicemqttsub import DeviceMQTTSubWrapper
>>> from pioutput import MotorAdaptor
>>> motor = MotorAdaptor(pin_number=10, max_runtime=30, cooldown=30)
>>> mqtt = DeviceMQTTSubWrapper(device=motor, topic='control', start_msg=1, stop_msg=0)
```
Pin 10 will activate when a message with payload '1' is published under topic 'control'.
