# Power-Monitoring
  This repository will document the process of implementing the SB components power monitoring HAT which can be purchased [here](https://www.amazon.com/components-Monitoring-Channel-Current-Raspberry/dp/B08TC6CW9Y/ref=sr_1_3?crid=1NE1E3I6JO8NI&keywords=power+monitor+hat+raspberry+pi&qid=1664130908&sprefix=power+monitor+hat+raspberry+pi,aps,104&sr=8-3).
  
  This project also utilizes the Adafruit Powerboost 1000c which can be purchased [here](https://www.adafruit.com/product/2465) 
  
  
  The HAT is connected to the GPIO pins, in this case on a Raspberry Pi Zero. 
  
  The HAT will be collecting data from it's inputs and the data will be published remotely by using MQTT.


## Components

**RASPBERRY PI ZERO**

   Used to run power monitoring python script
   
   
   
**POWER MONITORING HAT**

   Used to observe output of solar cell and consumption of load (load in this case is Raspberry Pi 3 or 4)
  
  

**RASPBERRY PI 3 or 4**

  Wired through the power monitoring hat to monitor consumption
    


**SOLAR CELL**

   Wired through the power monitoring hat to monitor power output



## Dependencies

  - Ensure I2C is enabled on the RaspberryPi
  - Use `sudo pip3 install adafruit-circuitpython-ina219` (required to run power monitoring HAT)
  
## Using the HAT

  - Clone github repository `git clone https://github.com/sbcshop/Power-Monitor-HAT.git`
  - Change into Power Monitor directory `cd Power-Monitor-HAT`
  - Change into RaspberryPi directory `cd RaspberryPi`
  - Create script to run code `nano [YourFileName].py`
  - Paste code from github file PowerMonitor.py into your script
  - Change code according to your implementation, I.E. topic, servers, etc...
  - Run script with `python3 [YourFileName].py`
  - Done!
