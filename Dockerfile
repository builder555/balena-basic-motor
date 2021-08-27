FROM balenalib/%%BALENA_ARCH%%-debian-python

WORKDIR /usr/src/app

RUN /usr/local/bin/python3.9 -m pip install --upgrade pip
RUN apt-get update -y && apt-get install build-essential
RUN /usr/local/bin/python3.9 -m pip install requests RPi.Gpio gpiozero paho-mqtt

COPY . .

CMD ["python3", "app.py"]