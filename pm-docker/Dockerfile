# syntax=docker/dockerfile:1

FROM ubuntu:22.04

RUN apt-get update

RUN apt-get install -y python3 python3-pip

RUN apt-get install -y python3-smbus python3-dev i2c-tools

RUN pip3 install adafruit-circuitpython-ina219

RUN apt-get install -y python3-lgpio

RUN pip install rpi.gpio

RUN apt install -y software-properties-common

RUN apt-add-repository ppa:mosquitto-dev/mosquitto-ppa

RUN apt-get update

RUN apt-get install -y mosquitto mosquitto-clients

COPY mosquitto.conf /etc/mosquitto/

RUN pip3 install paho-mqtt

RUN pip install pytz

ADD PMConfiguration.py /PMConfiguration.py

ADD PowerMonitor.py /PowerMonitor.py

ADD PowerMonitor.sh /PowerMonitor.sh

ADD Data /Data

RUN mkdir -p /Data/logs

RUN chmod +x /PowerMonitor.py

RUN chmod +x /PowerMonitor.sh

CMD service mosquitto start \
    && ./PowerMonitor.sh \
    && bash
