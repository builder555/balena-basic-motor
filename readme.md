### Balena Blocks: basic motor

Gets input from MQTT and either turns on or off a specific pin on a device.

Currently supports only Balena Fin and Raspberry Pi devices.

___Usage as a block___

Add the following to your `docker-compose.yaml`:

```yaml
  motor:
    privileged: true
    build: ./basic-motor
    restart: always
    environment: 
      - INPUT=logic_1
      - PIN=27
```

The pin is set high when a message with payload "1" comes on `INPUT` topic and set low, when payload "0" comes in.

___Available variables___

- `INPUT`: name of MQTT topic to trigger the pin
- `PIN`: physical pin to use on the device
- `MAX_ON_TIME`: maximum time, in seconds, to keep the pin on continuously
- `COOLDOWN`: how long, in seconds, to keep the pin off after max_on_time is reached

___Environment variables defaults___

- `INPUT`: "input"
- `PIN`: 27
- `MAX_ON_TIME`: 30
- `COOLDOWN`: 30

___Tests___

```bash
$ PIPENV_VENV_IN_PROJECT=1 pipenv install --dev
$ pipenv shell
$ pytest -vs
```

___Standalone usage___

Device pin is activated when the block receives appropriate MQTT message.

Given the code
```python
>>> from devicemqttsub import DeviceMQTTSubWrapper
>>> from pioutput import MotorAdaptor
>>> from time import sleep
>>> motor = MotorAdaptor(pin_number=10, max_runtime=10, cooldown=30)
>>> mqtt = DeviceMQTTSubWrapper(device=motor, topic='control', start_msg=1, stop_msg=0)
>>> while True:
>>>     sleep(1)
```
Pin 10 will activate when a message with payload '1' is published under topic 'control'. It'll run for at most 10 seconds at a time.

> N.B. mqtt connects to host 'mqtt' on port 1883

_logo image by [naim](https://thenounproject.com/naim.solis/)_