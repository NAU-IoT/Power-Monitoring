# Power-Monitoring
  This repository will document the process of implementing the SB components power monitoring HAT which can be purchased [here](https://www.amazon.com/components-Monitoring-Channel-Current-Raspberry/dp/B08TC6CW9Y/ref=sr_1_3?crid=1NE1E3I6JO8NI&keywords=power+monitor+hat+raspberry+pi&qid=1664130908&sprefix=power+monitor+hat+raspberry+pi,aps,104&sr=8-3).
  
  This project also utilizes the Adafruit Powerboost 1000c which can be purchased [here](https://www.adafruit.com/product/2465) 
  
  
  The HAT is connected to the GPIO pins, in this case on a Raspberry Pi 4. 
  
  The HAT will be collecting data from the terminals and the data will be published remotely by using MQTT.


## Components

**RASPBERRY PI 4**

   Used to run power monitoring python script
   
   
   
**POWER MONITORING HAT**

   Used to observe output of solar cell and consumption of load (load in this case is a Raspberry Pi IO Board)
  
  

**RASPBERRY PI IO Board**

  Wired through the power monitoring hat to monitor consumption
    


**SOLAR CELL**

   Wired through the power monitoring hat to monitor power output



## Dependencies

  - Ensure I2C is enabled on the RaspberryPi
  - If pyhton 3 is installed, but pip is not, install pip using `sudo apt-get -y install python3-pip`
  - Use `sudo pip3 install adafruit-circuitpython-ina219` (required to run power monitoring HAT)
  - Install the GPIO package using `sudo apt install python3-lgpio` (ubuntu GPIO support)
    - If not on ubuntu: `apt-get install rpi.gpio`
  - Install mosquitto service 
    - `sudo apt-get install mosquitto mosquitto-clients`
    - `sudo systemctl enable mosquitto`
    - check if mosquitto is running `sudo systemctl status mosquitto`
  - Install the paho.mqtt library 
    - `git clone https://github.com/eclipse/paho.mqtt.python`
    - `cd paho.mqtt.python`
    - `python3 setup.py install`
  - Install the pytz timezone library
    - `pip install pytz`


## Using the HAT

  - Clone github repository `git clone https://github.com/sbcshop/Power-Monitor-HAT.git`
  - Change into Power Monitor directory `cd Power-Monitor-HAT`
  - Change into RaspberryPi directory `cd RaspberryPi`
  - Create script to run code `nano YourFileName.py`
    - Paste code from github file PowerMonitor.py into your script
  - Create configuration script to easily modify variables within the code `nano PMConfiguration.py`
    - Paste code from github file PMConfiguration.py
      - Change variable names according to your implementation
  - Set permissions to make the script executable by typing `chmod +x SCRIPTNAME.py` in the command line
  - To use TLS set, uncomment lines 66-69 and change 1883 to 8883 on line 72 
  - IF USING TLS SET: ensure keyfile has the correct permissions for the user to run the script without error
    - If getting error **"Error: Problem setting TLS options: File not found."** use command `sudo chmod 640 YourKeyFile.key` (sets permissions so that the user and group are able to read the keyfile)
  - Run script with `./YourFileName.py`
    - Can also use `python3 YourFileName.py`
  - To see data being published, subscribe to the specified topic using command: 
    
    WITHOUT TLS: `mosquitto_sub -p 1883 -t YOUR_TOPIC -h YOUR_BROKER_IP`
    
    WITH TLS: `mosquitto_sub --cafile YOUR_CAFILE.crt --cert YOUR_CERTFILE.crt --key YOUR_KEYFILE.key -p 8883 -t YOUR_TOPIC -h YOUR_BROKER_IP`
  
  - Done!
