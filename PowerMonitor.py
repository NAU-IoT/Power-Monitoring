#! /usr/bin/python

import time
from datetime import datetime
import pytz
import board
from adafruit_ina219 import ADCResolution, BusVoltageRange, INA219
import paho.mqtt.client as mqtt
import logging
import PMConfiguration as config

#enable logging
logging.basicConfig(level=logging.DEBUG)

#import variables from config file
topic = config.topic
Broker = config.broker
Load1 = config.load1
Load2 = config.load2
Load3 = config.load3
CA_Certs = config.cacert
Certfile = config.certfile
Keyfile = config.keyfile
Timezone = config.timezone
Sleeptime = config.sleeptime

# define on_connect function
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    # subscribe, which need to put into on_connect
    # if reconnect after losing the connection with the broker, it will continu>
    client.subscribe(topic)

# define on_publish function
def on_publish(client, userdata, mid):
    """
      Callback function when topic is published.
    """
    #logging.info("Data published successfully.")

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

# set the will message, when the Raspberry Pi is powered off, or the network is>
client.will_set(topic, b'Monitoring script has terminated')

#establish tls set for secure connection over port 8883
#client.tls_set(ca_certs=CA_Certs,
#               certfile=Certfile,
#               keyfile=Keyfile)

# create connection, the three parameters are broker address, broker port numbe>
client.connect(Broker, 1883, 60)


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
    currentDandT = datetime.now(pytz.timezone(Timezone))

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

    Str1 = "{:<23}  Shunt Voltage:{:9.6f}V    Load Voltage:{:6.3f}V    Current:{:9.6f}A    Power:{:9.6f}W"
    Str2 = "{:<23}  Shunt Voltage:{:9.6f}V    Load Voltage:{:6.3f}V    Current:{:9.6f}A    Power:{:9.6f}W"
    Str3 = "{:<23}  Shunt Voltage:{:9.6f}V    Load Voltage:{:6.3f}V    Current:{:9.6f}A    Power:{:9.6f}W"

    Str4 = " "

#put logging debug message here with data published to log (include topic name)
    logging.debug("\n\npublishing data to topic: {}\n".format(topic))

    logging.debug(str(currentDandT))
    logging.debug(Str1.format((Load1),(shunt_voltage1),(bus_voltage1),(current1/1000),(power1)))
    logging.debug(Str2.format((Load2),(shunt_voltage2),(bus_voltage2),(current2/1000),(power2)))
    logging.debug(Str3.format((Load3),(shunt_voltage3),(bus_voltage3),(current3/1000),(power3)))
    logging.debug("-"*100)

#publish data to topic
    client.publish(topic, Str4)
    client.publish(topic, str(currentDandT))
    client.publish(topic, Str1.format((Load1),(shunt_voltage1),(bus_voltage1),(current1/1000),(power1)))
    client.publish(topic, Str2.format((Load2),(shunt_voltage2),(bus_voltage2),(current2/1000),(power2)))
    client.publish(topic, Str3.format((Load3),(shunt_voltage3),(bus_voltage3),(current3/1000),(power3)))
    client.publish(topic, Str4)
    client.publish(topic, Str4)
    time.sleep(Sleeptime)
