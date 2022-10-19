#! /usr/bin/python

import time
import board
from adafruit_ina219 import ADCResolution, BusVoltageRange, INA219
import paho.mqtt.client as mqtt
import logging

#define the topic
topic = "[YOUR TOPIC HERE]"

# define on_connect function
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    # subscribe to the specified topic
    client.subscribe(topic)

# define on_publish function
def on_publish(client, userdata, mid):
    """
      Callback function when topic is published.
    """
    logging.info("Data published successfully.")

# define on_subscribe function
def on_subscribe(client, userdata, mid, granted_qos):
    """
      Callback function when topic is subscribed.
    """
    logging.info("Topic successfully subscribed with QoS: %s" % granted_qos)

# the callback function, it will be triggered when receiving messages
def on_message(client, userdata, msg):
    print(f"{msg.topic} {msg.payload}")

#define the publish function
def publish(self, topic, data, qos=1, retain=False):
    """
      Publish to a topic.
    """
    logging.info("Publishing to topic %s" % topic)
    self.client.publish(topic, data, qos=qos, retain=retain)


#create client instance
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish
client.on_subscribe = on_subscribe

# set the will message, when the Raspberry Pi is powered off, or the network is interrupted
client.will_set(topic, b'{"status": "Off"}')

#establish tls set for secure connection over port 8883
client.tls_set(ca_certs="/SOME/PATH/TO/ca.crt", #change path and central authority cert as necessary
               certfile="/SOME/PATH/TO/server.crt", #change path and certfile as necessary
               keyfile="/SOME/PATH/TO/server.key") #change path and keyfile as necessary

# create connection, the three parameters are broker address, broker port number, keepalive (only broker address and broker port number are required)
client.connect("[YOUR BROKER IP]", 8883, 60)


i2c_bus = board.I2C()

ina1 = INA219(i2c_bus,addr=0x40)
ina2 = INA219(i2c_bus,addr=0x41)
ina3 = INA219(i2c_bus,addr=0x42)

print("ina219 test")

ina1.bus_adc_resolution = ADCResolution.ADCRES_12BIT_32S
ina1.shunt_adc_resolution = ADCResolution.ADCRES_12BIT_32S
ina1.bus_voltage_range = BusVoltageRange.RANGE_16V

ina2.bus_adc_resolution = ADCResolution.ADCRES_12BIT_32S
ina2.shunt_adc_resolution = ADCResolution.ADCRES_12BIT_32S
ina2.bus_voltage_range = BusVoltageRange.RANGE_16V

ina3.bus_adc_resolution = ADCResolution.ADCRES_12BIT_32S
ina3.shunt_adc_resolution = ADCResolution.ADCRES_12BIT_32S
ina3.bus_voltage_range = BusVoltageRange.RANGE_16V


# measure and display loop
while True:
    bus_voltage1 = ina1.bus_voltage        # voltage on V- (load side)
    shunt_voltage1 = ina1.shunt_voltage    # voltage between V+ and V- across the shunt
    power1 = ina1.power
    current1 = ina1.current                # current in mA

    bus_voltage2 = ina2.bus_voltage        # voltage on V- (load side)
    shunt_voltage2 = ina2.shunt_voltage    # voltage between V+ and V- across the shunt
    power2 = ina2.power
    current2 = ina2.current                # current in mA

    bus_voltage3 = ina3.bus_voltage        # voltage on V- (load side)
    shunt_voltage3 = ina3.shunt_voltage    # voltage between V+ and V- across the shunt
    power3 = ina3.power
    current3 = ina3.current                # current in mA

    Str1 = "RASPBERRYPI: PSU Voltage:{:6.3f}V    Shunt Voltage:{:9.6f}V    Load Voltage:{:6.3f}V    Power:{:9.6f}W    Current:{:9.6f}A"
    Str2 = "SOLAR CELL:  PSU Voltage:{:6.3f}V    Shunt Voltage:{:9.6f}V    Load Voltage:{:6.3f}V    Power:{:9.6f}W    Current:{:9.6f}A"
    Str3 = "OTHER LOAD:  PSU Voltage:{:6.3f}V    Shunt Voltage:{:9.6f}V    Load Voltage:{:6.3f}V    Power:{:9.6f}W    Current:{:9.6f}A"

    Str4 = " "
    
    #Publish data to topic then wait 5 seconds before looping again
    client.publish(topic, Str1.format((bus_voltage1 + shunt_voltage1),(shunt_voltage1),(bus_voltage1),(power1),(current1/1000)))
    client.publish(topic, Str2.format((bus_voltage2 + shunt_voltage2),(shunt_voltage2),(bus_voltage2),(power2),(current2/1000)))
    client.publish(topic, Str3.format((bus_voltage3 + shunt_voltage3),(shunt_voltage3),(bus_voltage3),(power3),(current3/1000)))
    client.publish(topic, Str4)
    client.publish(topic, Str4)
    client.publish(topic, Str4)
    time.sleep(5)

