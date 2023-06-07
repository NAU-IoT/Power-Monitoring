#! /usr/bin/python

import time
from datetime import datetime
import pytz
import board
from adafruit_ina219 import ADCResolution, BusVoltageRange, INA219
import paho.mqtt.client as mqtt
import logging
import PMConfiguration as config
import csv
import os.path

# Enable logging
logging.basicConfig(level=logging.DEBUG)

# Import variables from config file
Topic = config.topic
Port = config.port
DataPath = config.datastorage
Broker = config.broker
Load1 = config.load1
Load2 = config.load2
Load3 = config.load3
PrintLoad1 = config.printload1
PrintLoad2 = config.printload2
PrintLoad3 = config.printload3
CA_Certs = config.cacert
Certfile = config.certfile
Keyfile = config.keyfile
Timezone = config.timezone
Sleeptime = config.sleeptime

# Define on_connect function
def on_connect(client, userdata, flags, rc):
    #logging.info(f"Connected with result code {rc}")
    # subscribe, which need to put into on_connect
    client.subscribe(Topic)

# Define on_publish function
def on_publish(client, userdata, mid):
    """
      Callback function when topic is published.
    """
    # logging.info("Data published successfully.")


# Define the publish function
def publish(self, Topic, data, qos=1, retain=False):
    """
      Publish to a topic.
    """
    logging.info("Publishing to topic %s" % Topic)
    self.client.publish(Topic, data, qos=qos, retain=retain)


# Define check zero function
def check_zero(shunt, bus, current) -> tuple[float, float, float]:
    if(shunt < .0001):
        shunt = 0.0
    if(bus < .01):
        bus = 0.0
    if(current < .001):
        current = 0.0
    return shunt, bus, current
        

# Create client instance
client = mqtt.Client()
# Set callback functions for client
client.on_connect = on_connect
client.on_publish = on_publish

# Set the will message, when the client unexpedetly disconnects or terminates its connection, this will publish
client.will_set(Topic, b'Monitoring script has terminated')

# Establish tls set for secure connection over port 8883
#client.tls_set(ca_certs=CA_Certs,
#               certfile=Certfile,
#               keyfile=Keyfile)

# Create connection, the three parameters are broker address, broker port number, and keep alive time
client.connect(Broker, Port, 60) # If using TLS, Broker is the common name on the server cert

# Create i2c bus object
i2c_bus = board.I2C()

# Create 3 instances of the INA219 current sensor modules, configured to each address used by the power monitoring HAT
ina1 = INA219(i2c_bus,addr=0x40)
ina2 = INA219(i2c_bus,addr=0x41)
ina3 = INA219(i2c_bus,addr=0x42)

#print("ina219 test")

ina1.bus_adc_resolution = ADCResolution.ADCRES_12BIT_32S   # Set bus ADC resolution to 12-bit with 32-sample conversion time
ina1.shunt_adc_resolution = ADCResolution.ADCRES_12BIT_32S  # Set shunt ADC resolution to 12-bit with 32-sample conversion time
ina1.bus_voltage_range = BusVoltageRange.RANGE_16V  # Set bus voltage range to 16V

ina2.bus_adc_resolution = ADCResolution.ADCRES_12BIT_32S  # Set bus ADC resolution to 12-bit with 32-sample conversion time
ina2.shunt_adc_resolution = ADCResolution.ADCRES_12BIT_32S  # Set shunt ADC resolution to 12-bit with 32-sample conversion time
ina2.bus_voltage_range = BusVoltageRange.RANGE_16V  # Set bus voltage range to 16V

ina3.bus_adc_resolution = ADCResolution.ADCRES_12BIT_32S  # Set bus ADC resolution to 12-bit with 32-sample conversion time
ina3.shunt_adc_resolution = ADCResolution.ADCRES_12BIT_32S  # Set shunt ADC resolution to 12-bit with 32-sample conversion time
ina3.bus_voltage_range = BusVoltageRange.RANGE_16V  # Set bus voltage range to 16V

# Initialize header for CSV file
header = ['DateAndTime', 'LoadName', 'ShuntVoltage', 'LoadVoltage', 'Current', 'Power']  

timestr = time.strftime("%Y%m%d") #current date for filename
base = "PowerMonitor-" #base name of file
extension = ".csv" #.csv extension for filename
filename = base + timestr + extension #combine into filename
datastorage = DataPath + filename #append filename to end of DataPath to create one variable

# test if csv file already exists
testforfile = os.path.exists(datastorage)

if(testforfile):
    # File exists, append to file so it is not overwritten 
    file = open(datastorage, 'a')
    writer = csv.writer(file)

else:
    # File does not exist, open new file for writing and write header
    file = open(datastorage, 'w')
    writer = csv.writer(file)

    # Write the header
    writer.writerow(header)


# Infinite loop to read and log data
while True:

    timestr = time.strftime("%Y%m%d") #update current date for newfilename
    newfilename = base + timestr + extension #combine into new filename

    # Test if it is a new day, i.e. newfile name has the new date in it
    if(newfilename != filename):
        file.close()       #close old file
        filename = newfilename  #set filename to new date filename
        datastorage = DataPath + filename #update variable
        file = open(datastorage, 'w')   #open new file with current date
        writer = csv.writer(file)
        writer.writerow(header) #write the header to the new file

    currentDandT = datetime.now(pytz.timezone(Timezone))  # Get current date and time 

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

    # Check if shunt v, load v, or current are 0
    shunt_voltage1, bus_voltage1, current1 = check_zero(shunt_voltage1, bus_voltage1, current1)  
    shunt_voltage2, bus_voltage2, current2 = check_zero(shunt_voltage2, bus_voltage2, current2)
    shunt_voltage3, bus_voltage3, current3 = check_zero(shunt_voltage3, bus_voltage3, current3)
    
    # Format strings with data values
    Str1 = "{:<23}  Shunt Voltage:{:9.6f}V    Load Voltage:{:6.3f}V    Current:{:9.6f}A    Power:{:9.6f}W"
    Str2 = "{:<23}  Shunt Voltage:{:9.6f}V    Load Voltage:{:6.3f}V    Current:{:9.6f}A    Power:{:9.6f}W"
    Str3 = "{:<23}  Shunt Voltage:{:9.6f}V    Load Voltage:{:6.3f}V    Current:{:9.6f}A    Power:{:9.6f}W"

    Str4 = " "

    # Logging info
    logging.debug("\n\npublishing data to topic: {}\n".format(Topic))
    logging.debug(str(currentDandT))
    if(PrintLoad1):
        if((shunt_voltage1 != None) and (bus_voltage1 != None) and (current1 != None) and (power1 != None)):
           logging.debug(Str1.format((Load1),(shunt_voltage1),(bus_voltage1),(current1/1000),(power1)))
        else:
           logging.debug(f"\n {Load1} data contained null value")
    if(PrintLoad2):
        if((shunt_voltage2 != None) and (bus_voltage2 != None) and (current2 != None) and (power2 != None)):
           logging.debug(Str2.format((Load2),(shunt_voltage2),(bus_voltage2),(current2/1000),(power2)))
        else:
           logging.debug(f"\n {Load2} data contained null value")
    if(PrintLoad3):
        if((shunt_voltage3 != None) and (bus_voltage3 != None) and (current3 != None) and (power3 != None)):
           logging.debug(Str3.format((Load3),(shunt_voltage3),(bus_voltage3),(current3/1000),(power3)))
        else:
           logging.debug(f"\n {Load3} data contained null value")
    logging.debug("-"*100)

    # Publish data to topic
    client.publish(Topic, Str4)
    client.publish(Topic, str(currentDandT))
    if(PrintLoad1):
        client.publish(Topic, Str1.format((Load1),(shunt_voltage1),(bus_voltage1),(current1/1000),(power1)))
    if(PrintLoad2):
        client.publish(Topic, Str2.format((Load2),(shunt_voltage2),(bus_voltage2),(current2/1000),(power2)))
    if(PrintLoad3):
        client.publish(Topic, Str3.format((Load3),(shunt_voltage3),(bus_voltage3),(current3/1000),(power3)))
    client.publish(Topic, Str4)
    client.publish(Topic, Str4)


    # Write data to csv file
    data1 = [currentDandT, Load1, round(shunt_voltage1, 6), round(bus_voltage1, 3), round(current1/1000, 6), round(power1, 6)]
    data2 = [currentDandT, Load2, round(shunt_voltage2, 6), round(bus_voltage2, 3), round(current2/1000, 6), round(power2, 6)]
    data3 = [currentDandT, Load3, round(shunt_voltage3, 6), round(bus_voltage3, 3), round(current3/1000, 6), round(power3, 6)]
    if(PrintLoad1 and (None not in data1)):
        writer.writerow(data1)
    if(PrintLoad2 and (None not in data2)):
        writer.writerow(data2)
    if(PrintLoad3 and (None not in data3)):
        writer.writerow(data3)

    file.flush() # Flush data to disk

    time.sleep(Sleeptime)
