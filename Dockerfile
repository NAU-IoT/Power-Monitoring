# syntax=docker/dockerfile:1

FROM ubuntu:22.04

RUN apt-get update

RUN apt-get install -y python3 python3-pip

RUN apt-get install -y python3-smbus python3-dev i2c-tools

RUN pip3 install adafruit-circuitpython-ina219

RUN apt-get install -y python3-lgpio

RUN pip install rpi.gpio

RUN apt-get install -y software-properties-common

RUN apt-add-repository ppa:mosquitto-dev/mosquitto-ppa

RUN apt-get install -y mosquitto mosquitto-clients

RUN apt-get -y install cron

COPY mosquitto.conf /etc/mosquitto/

RUN pip3 install paho-mqtt

RUN pip install pytz

RUN DEBIAN_FRONTEND=noninteractive apt-get -y install tzdata

ENV TZ=America/Phoenix

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

ADD PMConfiguration.py /PMConfiguration.py

ADD PowerMonitor.py /PowerMonitor.py

ADD PowerMonitor.sh /PowerMonitor.sh

ADD crontab /etc/cron.d/simple-cron

RUN touch /var/log/cron.log

RUN mkdir -p /Data

RUN mkdir -p /Data/logs

RUN chmod 0644 /etc/cron.d/simple-cron

RUN chmod +x /PowerMonitor.py

RUN chmod +x /PowerMonitor.sh

# sleep command to give mosquitto time to start before using.
CMD service mosquitto start \
    && sleep 5 \
    && cron \
# Uncomment below line and comment out the above line for debugging, otherwise script will not execute until cron execution
#   && ./PowerMonitor.sh \ 
    && bash

