# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Update package list
RUN apt-get update

# Install apt dependencies
RUN apt-get install -y python3 python3-pip python3-smbus python3-dev i2c-tools python3-lgpio software-properties-common

# Install pip dependencies
RUN pip install adafruit-circuitpython-ina219 rpi.gpio paho-mqtt pytz

# Add latest mosquitto repo
RUN apt-add-repository ppa:mosquitto-dev/mosquitto-ppa

# Install mosqutto and cron
RUN apt-get install -y mosquitto mosquitto-clients cron

# Install timezone dependencies and establish docker container timezone
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install tzdata
ENV TZ=America/Phoenix
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Copy necessary files to local docker container environment
COPY mosquitto.conf /etc/mosquitto/
ADD PMConfiguration.yaml /PMConfiguration.yaml
ADD PowerMonitor.py /PowerMonitor.py
ADD PowerMonitor.sh /PowerMonitor.sh
ADD crontab /etc/cron.d/simple-cron

# Create necessary files and directories inside docker container
RUN touch /var/log/cron.log
RUN mkdir -p /Data
RUN mkdir -p /Data/logs

# Establish correct permissions for files
RUN chmod 0644 /etc/cron.d/simple-cron
RUN chmod +x /PowerMonitor.py
RUN chmod +x /PowerMonitor.sh

# Start services in container (sleep command to give mosquitto time to start before using)
CMD service mosquitto start \
    && sleep 5 \
    && cron \
# Uncomment below line and comment out the above line for debugging, otherwise script will not execute until cron execution
#   && ./PowerMonitor.sh \ 
    && bash


