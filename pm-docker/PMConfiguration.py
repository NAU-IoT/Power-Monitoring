topic = "PowerMonitoring" #topic name
port = YOUR_MQTT_PORT_NUMBER #port to be used by mqtt; IoT Team: use port 31883
datastorage = "/Data/" #path to store the local csv files, no need to change this
broker = "YOUR BROKER NAME" #broker name or broker IP; IoT Team: use localhost, supervisor IP address, or supervisor DNS name
load1 = "YOUR LOAD 1"  #load connected to 0x40 terminals; IoT Team: use IOBoard host name
load2 = "YOUR LOAD 2"  #load connected to the 0x41 terminals
load3 = "YOUR LOAD 3"  #load connected to the 0x42 terminals
printload1 = True #boolean value to indicate if load1 is connected, if it is set to false the data will not be printed to logs
printload2 = False #boolean value to indicate if load2 is connected, if it is set to false the data will not be printed to logs
printload3 = False #boolean value to indicate if load3 is connected, if it is set to false the data will not be printed to logs
cacert = "/SOME/PATH/TO/ca.crt" #path to cafile, leave as is if not using keys
certfile = "/SOME/PATH/TO/server.crt" #path to certfile, leave as is if not using keys
keyfile = "/SOME/PATH/TO/server.key" #path to keyfile, leave as is if not using keys
timezone = 'US/Arizona' #timezone for timestamps, consult pytz list of timezones for acceptable timezones at https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568
sleeptime = 10 #wait 10 seconds between publishing data
