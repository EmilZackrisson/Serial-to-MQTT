import paho.mqtt.client as mqttClient
import time
import serial

broker_adress= "192.168.0.56"
port = 1883
client = mqttClient.Client("Python")
topic = "ArduinoHylla"
client.username_pw_set(username="mqtt",password="zacke")

serial = serial.Serial('/dev/ttyUSB0', 9600)
time.sleep(2)
if serial.isOpen():
	print("Serial is working")

def on_connect(client, userdata, flags, rc):
	if rc == 0:
		print("Connected to broker")

		global Connected
		Connected = True
		client.publish(topic + "/available","online")
 
	else:
		print("Connection failed")

def on_message(client, userdata, message):
	latest = message.payload
	client.publish(topic, latest)
    print(latest)

Connected = False


client.on_connect = on_connect
client.on_message = on_message

client.connect(broker_adress, port=port)

client.loop_start()

while Connected != True:
	time.sleep(0.1)

try:
	while True:
		time.sleep(1)

except KeyboardInterrupt:
	print("exiting")
	client.publish(topic + "/available","offline")
	client.disconnect()
	client.loop_stop()
	serial.close