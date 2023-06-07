# Power-Monitoring
  This repository will document the process of implementing the SB components power monitoring HAT which can be purchased [here](https://www.amazon.com/components-Monitoring-Channel-Current-Raspberry/dp/B08TC6CW9Y/ref=sr_1_3?crid=1NE1E3I6JO8NI&keywords=power+monitor+hat+raspberry+pi&qid=1664130908&sprefix=power+monitor+hat+raspberry+pi,aps,104&sr=8-3).
  
  The HAT is connected to the GPIO pins, in this case on a Raspberry Pi 4. 
  
  The HAT will be collecting data from the terminals and the data will be published remotely by using MQTT.

## Components

**RASPBERRY PI 4**

   Used to run power monitoring python script
   
   
   
**POWER MONITORING HAT**

   Used to observe consumption of given load (loads in this case are a Raspberry Pi IOBoard, Jetson Nano, and another RPi4)
  
  

**RASPBERRY PI IOBOARD**

  Wired through the power monitoring hat to monitor consumption
    

# Running with Docker

  - Install docker:
  ```
  sudo apt install docker.io
  ```
  - Check if docker is functioning:
  ```
  sudo docker run hello-world
  ```
  - Clone repository to get Dockerfile and configuration files: 
  ```
  git clone https://github.com/NAU-IoT/Power-Monitoring.git
  ```
  - Change into directory: 
  ```
  cd Power-Monitoring
  ```
  - Modify PMConfiguration.py to match your current implementation: 
    - Refer to comments for necessary changes
  ```
  nano PMConfiguration.py
  ```
  - OPTIONAL: To change the docker containers time zone, edit line 33 in the Dockerfile. A list of acceptable time zones can be found at https://en.wikipedia.org/wiki/List_of_tz_database_time_zones 
  - Build docker image in Power-Monitoring directory, this will take a while: 
  ```
  docker build -t powermonitor .
  ```
  - Create a directory in a convenient location to store the docker volume. For example: 
  ```
  mkdir -p Data/PMonData
  ```
  - Create a volume to store data inside the directory created in the previous step:
  ```
  docker volume create --driver local 
    --opt type=none 
    --opt device=/SOME/LOCAL/DIRECTORY 
    --opt o=bind 
    YOUR_VOLUME_NAME
  ```
  - Execute docker container in Power-Monitoring/pm-docker directory:
    - Note for IoT Team: Your_port_number could be 31883, container_port_number should be 31883
  ```
  docker run --privileged -v YOUR_VOLUME_NAME:/Data -p YOUR_PORT_NUMBER:CONTAINER_PORT_NUMBER -t -i -d --restart unless-stopped powermonitor
  ```
  - Verify container is running: 
  ```
  docker ps
  ```
  - Done!
  
  ### Notes
  - To see data being published, subscribe to the specified topic using command: 
    
    WITHOUT TLS:
    
    IoT Team: PORT_NUMBER should be 31883 (number in PMConfiguration.py)
    ```
    mosquitto_sub -p PORT_NUMBER -t YOUR_TOPIC -h YOUR_BROKER_IP
    ```
    
    Example command:
    ```
    mosquitto_sub -p 31883 -t PowerMonitoring -h localhost
    ```
    
    WITH TLS: 
    ```
    mosquitto_sub --cafile YOUR_CAFILE.crt --cert YOUR_CERTFILE.crt --key YOUR_KEYFILE.key -p 8883 -t YOUR_TOPIC -h YOUR_BROKER_IP
    ```
    
    Example command:
    ```
    mosquitto_pub --cafile /home/michael/cafile.crt --cert /home/michael/certfile.crt --key /home/michael/keyfile.key -p 8883 -d -h localhost -t PowerMonitoring
    ```
    
    Expected output format:
    <img width="858" alt="Screen Shot 2023-06-07 at 2 02 16 PM" src="https://github.com/NAU-IoT/Power-Monitoring/assets/72172361/47a0c848-3795-42cb-afd2-d8fb52ee67d0">


    
  - To enter the container:
    - This can be done to check log files or modify the container without rebuilding/restarting
  ```
  docker exec -it CONTAINER_ID /bin/bash
  ```
    
 ### Common Errors
 
  - If error: `Got permission denied while trying to connect to the Docker daemon socket at unix ... connect: permission denied`
    - Run command, then log out and ssh back into system:
  ```
  sudo usermod -aG docker $USER
  ```



# Running with Python & Systemctl

## Dependencies

  - Ensure I2C is enabled on the RaspberryPi

  - If python 3 is installed, but pip is not, install pip using: 
  ```
  sudo apt-get -y install python3-pip
  ```

  - Install package to run power monitoring HAT:
  ```
  sudo pip3 install adafruit-circuitpython-ina219
  ``` 

  - Install the GPIO package (Ubuntu GPIO support for versions 22.04+):
  ```
  sudo apt install python3-lgpio
  ```
   
  - Install another GPIO package (HAT uses this package): 
  ```
  sudo apt-get install rpi.gpio
  ```

  - Install mosquitto service: 
  ```
  sudo apt-get install mosquitto mosquitto-clients
  ```
  ```
  sudo systemctl enable mosquitto
  ```
  - Check if mosquitto is running: 
  ```
  sudo systemctl status mosquitto
  ```

  - Create your own mosquitto configuration file:
  ```
  cd /etc/mosquitto/conf.d
  ```
  ```
  sudo nano YOUR_FILE_NAME.conf
  ```
  - Paste these lines for insecure connection:
        
  ```
  allow_anonymous true
        
  listener 1883
  ```
  - Paste these lines for secure connection:
       
  ```
  allow_anonymous true
        
  listener 8883
        
  require_certificate true
       
  cafile /SOME/PATH/TO/ca.crt
        
  certfile /SOME/PATH/TO/server.crt
        
  keyfile /SOME/PATH/TO/server.key
  ``` 
  
  - Restart mosquitto service to recognize conf changes: 
  ```
  sudo systemctl restart mosquitto.service
  ```  
  - Check status to ensure mosquitto restarted successfully: 
  ```
  sudo systemctl status mosquitto.service
  ```
  - *refer to https://mosquitto.org/man/mosquitto-conf-5.html for official conf file documentation*

  - Install the paho.mqtt library: 
  ```
  sudo pip install paho-mqtt
  ```

  - Install the pytz timezone library:
  ```
  pip install pytz
  ```


## Using the HAT

  - Clone github repository: 
  ```
  git clone https://github.com/NAU-IoT/Power-Monitoring.git
  ```
  - Change into Power Monitor directory: 
  ```
  cd Power-Monitoring
  ```
  - Modify PMConfiguration.py variable names and paths according to your implementation: 
  ```
  nano PMConfiguration.py
  ```
  - Set permissions to make the script executable by running: 
  ```
  chmod +x PowerMonitor.py
  ```
  - To use TLS set, uncomment lines 78-80 in PowerMonitorpy and change port to 8883 in PMConfiguration.py
  - IF USING TLS SET: ensure keyfile has the correct permissions for the user to run the script without error
    - If getting `Error: Problem setting TLS options: File not found.` use the following command (sets permissions so that the user and group are able to read the keyfile):
    ```
    sudo chmod 640 YourKeyFile.key
    ```
  - Run script with: 
  ```
  ./PowerMonitor.py
  ```
  - Can also run with: 
  ```
  python3 PowerMonitor.py
  ```
  - To see data being published, subscribe to the specified topic using command: 
    
    WITHOUT TLS:
    
    ```
    mosquitto_sub -p PORT_NUMBER -t YOUR_TOPIC -h YOUR_BROKER_IP
    ```
    
    Example command:
    ```
    mosquitto_sub -p 1883 -t HomeNetwork -h localhost
    ```
    
    WITH TLS: 
    ```
    mosquitto_sub --cafile YOUR_CAFILE.crt --cert YOUR_CERTFILE.crt --key YOUR_KEYFILE.key -p 8883 -t YOUR_TOPIC -h YOUR_BROKER_IP
    ```
    
    Example command:
    ```
    mosquitto_pub --cafile /home/michael/cafile.crt --cert /home/michael/certfile.crt --key /home/michael/keyfile.key -p 8883 -d -h localhost -t HomeNetwork
    ```
  
  - Done!
  
  
  ## Implementing the script as a service
  
  - Create a systemd entry 
      - Change into Systemctl directory: 
      ```
      cd Power-Monitoring/Systemctl
      ``` 
      - Modify line 9 of PowerMonitor.service to reflect the correct path: 
      ```
      nano PowerMonitor.service
      ```
      - Copy the .service file to correct location: 
      ```
      sudo cp PowerMonitor.service /etc/systemd/system
      ```
  - Create logs directory inside of the Power-Monitoring directory: 
  ```
  mkdir logs
  ```
  - Modify PowerMonitor.sh to include the correct paths (located inside of the Systemctl directory) 
  ```
  nano PowerMonitor.sh
  ```
  - Set file permissions for PowerMonitor.sh: 
  ```
  sudo chmod 744 Power-Monitoring/Systemctl/PowerMonitor.sh
  ```
  - If previous step is unsuccessful, here are potential solutions:
      - Change permissions further 
      ```
      sudo chmod 755 Power-Monitoring/Systemctl/PowerMonitor.sh
      ```
      - Change permissions for the directory as well: 
      ```
      sudo chmod 755 Power-Monitoring
      ```
  - Enable the service: 
  ```
  sudo systemctl daemon-reload
  ```
  ```
  sudo systemctl enable PowerMonitor.service
  ```
      
  - Start the service: 
  ```
  sudo systemctl start PowerMonitor.service
  ```
  
  - Check the status of the service: 
  ```
  sudo systemctl status PowerMonitor.service
  ```
  
  - Done! The service should now run on boot. 


  ### Common Errors
  
  
  `socket.gaierror: [Errno -2] Name or service not known`
  
   - Most likely an issue with the DNS name or IP address not being recognized
