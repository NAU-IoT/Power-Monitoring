import paho.mqtt.client as mqtt
import logging
import time
from PiicoDev_BME280 import PiicoDev_BME280
from PiicoDev_Unified import sleep_ms
from mqtt_client import mqtt_client
import time

"""MQTT Client Class to be used for Network Communication."""

def on_connect(client, userdata, flag, rc):
    """
        Callback function when connection to the broker is established.
    """
    if (rc == 0):
        client.connected_flag = True
        logging.info("Connected to Broker! Returned code: %s\n" % rc)
    else:
        logging.info("Failed to connect. Returned code: %s\n" % rc)

def on_disconnect(client, userdata, rc):
    """
        Callback function when client has been disconnected from broker.
        mosquitto_pub/mosquitto_sub usage:
        -h: host IP Address of the machine running the Broker Software to connect to
        -t: topic Name of the topic to subscribe/publish to
        -m: message Content to publish to the topic (mosquitto_pub only)
        -d: debug Used to print request and acknowledgement messages between client and broker

    """
    logging.info("Disconnected from Broker. Returned code: %s\n" % rc)
    client.connected_flag = False
    client.disconnect_flag = True

def on_message(client, userdata, message):
    """
        Callback function for receiving messages.
    """
    msg = str(message.payload)
    logging.info("\tTopic: {}\n\tMessage: {}\n\tRetained: {}".format(message.topic, msg, message.retain))
    
    if (message.retain == 1):
        logging.info("This was a retained message.")

def on_publish(client, userdata, mid):
    """
        Callback function when topic is published.
    """
    logging.info("Data published successfully.")

def on_subscribe(client, userdata, mid, granted_qos):
    """
        Callback function when topic is subscribed.
    """
    logging.info("Topic successfully subcribed with QoS: %s" % granted_qos)

def on_log(client, userdata, level, buf):
    """
    Callback function for mqtt logger.
    """
    print("MQTTClient log: ", buf)

class MQTTClient:
    
    def __init__(self, broker_ip, client_name):
        """
        Class constructor.
        """
        self.broker_ip = broker_ip
        self.client_name = client_name
        self.msg_queue = []

        self.client = mqtt.Client(client_name)
    
        self.client.on_connect = on_connect
        self.client.on_disconnect = on_disconnect
        self.client.on_message = on_message
        self.client.on_publish = on_publish
        self.client.on_subscribe = on_subscribe
        self.client.on_log = on_log
    
    def connect(self, port=1883):
        """
        Connect to broker IP at port.
        """
        logging.info("Connecting to broker {}:{}".format(self.broker_ip, port))

        try:
            self.client.connect(self.broker_ip, port=port)
            time.sleep(2) # Wait to connect
        except Exception as error:
            print(error)
        
    def disconnect(self):
        """
        Disconnect from broker.
        """
        logging.info(f"Disconnecting from {self.broker_ip}.")
        self.client.disconnect()

    def subscribe(self, topic):
        """
        Subscribe to a topic.
        """
        logging.info("Subscribing to topic %s" % topic)
        try:
            self.client.subscribe(topic)
        except Exception as error:
            print(error)

    def publish(self, topic, data, qos=1, retain=False):
        """
        Publish to a topic.
        """
        logging.info("Publishing to topic %s" % topic)
        self.client.publish(topic, data, qos=qos, retain=retain)

    def loop_start(self):
        """
        Start the loop thread.
    
        """
        self.client.loop_start()

    def loop_stop(self):
        """
        Stop the loop thread.
        """
        self.client.loop_stop()

    def loop_forever(self):
        """
        Begin infinite loop.
        """
        self.client.loop_forever()

"""Network Class for MQTT Communication between client and server."""

class Network:
    def __init__(self, hostname: str, user: str):
        """Constructor method."""
        self.hostname = hostname
        self.user = user
        self.mqtt = MQTTClient(self.hostname, self.user)

    def disconnect(self):
        """Close the network connection."""
        self.mqtt.loop_stop()
        self.mqtt.disconnect()

    def connect(self, port=1883):
        """Connect to the network interface."""
        self.mqtt.connect(port)
        self.mqtt.loop_start()
    
    def receive(self, user=None) -> str:
        """Receive a message and return the string."""
        if user is None:
            user = self.user
        self.mqtt.subscribe(user)
        print("Waiting for a message...")
        cmd_received = False
        while not cmd_received:
            time.sleep(0.1) # Delay to throttle tight loop
        if len(self.mqtt.msg_queue) > 0:
            # Grab the message from the queue
            incoming_msg = self.mqtt.msg_queue.pop()
            return incoming_msg

    def send(self, receiver: str, msg: str):
        """Send a message, return true if successful."""
        self.mqtt.publish(receiver, msg, qos=2)

def main():

    sensor = PiicoDev_BME280() # initialize the sensor
    zeroAlt = sensor.altitude() # take an initial altitude reading

    global network
    
    
    
    client = mqtt.Client("raspberrypi")
    
    client.tls_set(ca_certs="/home/pi/etc/mosquitto/ca_certificates/ca.crt",
                                certfile="/home/pi/edge6.crt",
                                keyfile="/home/pi/edge6.key")

    broker_ip = "192.168.150.218"
    
    client.connect(broker_ip, port=8883)

    #network = Network("192.168.150.218", "192.168.150.221") #network(rPI IP(host), macbook IP(client))
    #network.mqtt.client.on_message = on_message
    #network.mqtt.client.tls_set(ca_certs="/home/pi/etc/mosquitto/ca_certificates/ca.crt",
    #                            certfile="/home/pi/edge6.crt",
    #                            keyfile="/home/pi/edge6.key")
    #logging.debug("Connecting to Network...")
    #network.connect(port=8883)
    #logging.debug("Connected to MQTT Broker.")
        
        
    while True:
        # Print data
        tempC, presPa, humRH = sensor.values() # read all data from the sensor
        pres_hPa = presPa / 100 # convert air pressurr Pascals -> hPa (or mbar, if you prefer)
    
        str1 = str(tempC)+" °C  "
        str2 = str(pres_hPa)+" hPa  "
        str3 = str(humRH)+" %RH"
        
        data = [str1, str2, str3]
        
        #subscribe(test/message)
        
        client.publish("test/message", data)
        
        #send(self, macbook, data)
        
        sleep_ms(10000)
