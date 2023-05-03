# Power-Monitoring
  This repository will document the process of implementing the SB components power monitoring HAT which can be purchased [here](https://www.amazon.com/components-Monitoring-Channel-Current-Raspberry/dp/B08TC6CW9Y/ref=sr_1_3?crid=1NE1E3I6JO8NI&keywords=power+monitor+hat+raspberry+pi&qid=1664130908&sprefix=power+monitor+hat+raspberry+pi,aps,104&sr=8-3).
  
  This project also utilizes the Adafruit Powerboost 1000c which can be purchased [here](https://www.adafruit.com/product/2465) 
  
  
  The HAT is connected to the GPIO pins, in this case on a Raspberry Pi 4. 
  
  The HAT will be collecting data from the terminals and the data will be published remotely by using MQTT.

  Details on how to run the script as a service that runs on boot are included as well. 

## Components

**RASPBERRY PI 4**

   Used to run power monitoring python script
   
   
   
**POWER MONITORING HAT**

   Used to observe output of solar cell and consumption of load (load in this case is a Raspberry Pi IO Board)
  
  

**RASPBERRY PI IO Board**

  Wired through the power monitoring hat to monitor consumption
    


**SOLAR CELL**

   Wired through the power monitoring hat to monitor power output

# Running with Docker

  - Install docker:
    - `sudo apt install docker.io`
    - Check if docker is functioning `sudo docker run hello-world`
  - Clone repository to get Dockerfile and configuration files `git clone https://github.com/NAU-IoT/Power-Monitoring.git`
  - Change into docker directory `cd Power-Monitoring/pm-docker`
  - Modify PMConfiguration.py to match your current implementation `nano PMConfiguration.py`
    - Refer to comments for necessary changes
  - Build docker image in Power-Monitoring/pm-docker directory `docker build -t powermonitor .` this will take a while
  - Create a directory in a convenient location to store the docker volume. For example: /Data/PMonData
  - Create a volume to store data inside the directory created in the previous step `docker volume create --driver local 
    --opt type=none 
    --opt device=/some/local/directory 
    --opt o=bind 
    YOUR_VOLUME_NAME`
  - Execute docker container `docker run --privileged -v YOUR_VOLUME_NAME:/Data -p YOUR_PORT_NUMBER:CONTAINER_PORT_NUMBER -t -i -d --restart unless-stopped powermonitor`
    - Note for IoT Team: Your_port_number could be 31883, container_port_number should be 31883
  - Verify container is running `docker ps`
  - Done!
  - To enter the container `docker exec -it CONTAINER_ID /bin/bash`
    - This can be done to check log files or modify the container without rebuilding/restarting
    
 ### Common Errors
 
  - If error: `Got permission denied while trying to connect to the Docker daemon socket at unix ... connect: permission denied`
    - Use `sudo usermod -aG docker $USER` , log out and ssh back into system




# Running with Python & Systemctl

## Dependencies

  - Ensure I2C is enabled on the RaspberryPi

  - If pyhton 3 is installed, but pip is not, install pip using `sudo apt-get -y install python3-pip`

  - Use `sudo pip3 install adafruit-circuitpython-ina219` (required to run power monitoring HAT)

  - Install the GPIO package using `sudo apt install python3-lgpio` (Ubuntu GPIO support for versions 22.04+)
   
  - Install another GPIO package (HAT uses this package): `sudo apt-get install rpi.gpio`

  - Install mosquitto service 
    - `sudo apt-get install mosquitto mosquitto-clients`
    - `sudo systemctl enable mosquitto`
    - check if mosquitto is running `sudo systemctl status mosquitto`

  - Create your own mosquitto configuration file:
    - `cd /etc/mosquitto/conf.d`
    - `sudo nano YOUR_FILE_NAME.conf`
    - paste these lines for insecure connection:
        
       ```
       allow_anonymous true
        
       listener 1883
       ```
    - paste these lines for secure connection:
       
       ```
       allow_anonymous true
        
       listener 8883
        
       require_certificate true
       
       cafile /SOME/PATH/TO/ca.crt
        
       certfile /SOME/PATH/TO/server.crt
        
       keyfile /SOME/PATH/TO/server.key
       ``` 
    - Restart mosquitto service to recognize conf changes `sudo systemctl restart mosquitto.service`  
    - Check status to ensure mosquitto restarted successfully `sudo systemctl status mosquitto.service`
    - *refer to https://mosquitto.org/man/mosquitto-conf-5.html for conf file documentation*

  - Install the paho.mqtt library 
    - `sudo pip install paho-mqtt`

  - Install the pytz timezone library
    - `pip install pytz`


## Using the HAT

  - Clone github repository `git clone https://github.com/NAU-IoT/Power-Monitoring.git`
  - Change into Power Monitor directory `cd Power-Monitoring`
  - Modify PMConfiguration.py variable names and paths according to your implementation `nano PMConfiguration.py`
  - Set permissions to make the script executable by typing `chmod +x PowerMonitor.py` in the command line
  - To use TLS set, uncomment lines 75-77 and change 1883 to 8883 on line 80
  - IF USING TLS SET: ensure keyfile has the correct permissions for the user to run the script without error
    - If getting error **"Error: Problem setting TLS options: File not found."** use command `sudo chmod 640 YourKeyFile.key` (sets permissions so that the user and group are able to read the keyfile)
  - Run script with `./PowerMonitor.py`
    - Can also use `python3 PowerMonitor.py`
  - To see data being published, subscribe to the specified topic using command: 
    
    WITHOUT TLS: `mosquitto_sub -p 1883 -t YOUR_TOPIC -h YOUR_BROKER_IP`
    
    WITH TLS: `mosquitto_sub --cafile YOUR_CAFILE.crt --cert YOUR_CERTFILE.crt --key YOUR_KEYFILE.key -p 8883 -t YOUR_TOPIC -h YOUR_BROKER_IP`
  
  - Done!
  
  
  ## Implementing the script as a service
  
  - Create a systemd entry 
      - Change into Systemctl directory `cd Power-Monitoring/Systemctl` 
      - Modify line 8 of PowerMonitor.service to reflect the correct path `nano PowerMonitor.service`
      - Copy the .service file to correct location `sudo cp PowerMonitor.service /etc/systemd/system`
  - Create logs directory inside of the Power-Monitoring directory `mkdir logs`
  - Modify PowerMonitor.sh to include the correct paths (located inside of the Systemctl directory) `nano PowerMonitor.sh`
  - Set file permissions for PowerMonitor.sh `sudo chmod 744 Power-Monitoring/Systemctl/PowerMonitor.sh`
      - If this step is unsuccessful, here are potential solutions:
         - Change permissions further `sudo chmod 755 Power-Monitoring/Systemctl/PowerMonitor.sh`
         - Change permissions for the directory as well `sudo chmod 755 Power-Monitoring`
  - Enable the service 
      - `sudo systemctl daemon-reload`
      - `sudo systemctl enable PowerMonitor.service`
      
  - Start the service `sudo systemctl start PowerMonitor.service`
  
  - Check the status of the service `sudo systemctl status PowerMonitor.service`
  
  - Done! The service should now run on boot. 


  ### Common Errors
  
  
  `socket.gaierror: [Errno -2] Name or service not known`
  
   - Most likely an issue with the DNS name or IP address not being recognized
