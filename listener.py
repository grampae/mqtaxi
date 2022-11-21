# mqtt listener stuff
import readline
import sqlite3
import pandas as pd
import os
from mqworker import *
from cryptography.fernet import Fernet


dbfile = (os.path.dirname(os.path.realpath(__file__))+"/mqt-config.db")

def addlisten():
	cipher_key = Fernet.generate_key()
	conn = sqlite3.connect(dbfile)
	cursor = conn.cursor()
	Transport = input('Specify tcp or websockets: ')
	Address = input('Listener IP or host name: ')
	Port = input('Listener port number: ')
	Private = input('Specify public or private: ')
	User = input('Enter user name or blank if not required: ')
	Pass = input('Enter password or blank if not required: ')
	cursor.execute("""
	INSERT INTO listener(Transport, Address, Port, Private, User, Pass, Key, Active)
	VALUES (?,?,?,?,?,?,?,"no")
	""", (Transport, Address, Port, Private, User, Pass, cipher_key))
	conn.commit()
	conn.close()
	
def listlisten():
	conn = sqlite3.connect(dbfile)
	cursor = conn.cursor()
	df = pd.read_sql_query("SELECT ID, Transport, Address, Port, Private, User, Active from listener", conn)
	print("\n")
	print(df.to_string(index=False))
	print("\n")
	conn.close()

def dellisten():
	delid = input('ID of mqtt listener to delete: ')
	if delid == "":
		return
	conn = sqlite3.connect(dbfile)
	cursor = conn.cursor()
	conn.execute("DELETE from listener where ID=?",(delid))
	conn.commit()
	conn.close()

def activatelis():
	sid = input('ID of mqtt listener to activate: ')
	if sid == "":
		return
	active = 'yes'
	inactive = 'no'
	conn = sqlite3.connect(dbfile)
	cursor = conn.cursor()
	conn.execute("UPDATE listener set Active = 'no'")
	conn.execute("UPDATE listener set Active = ? where ID = ?",(active, sid))
	conn.commit()
	conn.close()
	daemonmqtt()
def discolistener():
	conn = sqlite3.connect(dbfile)
	cursor = conn.cursor()
	conn.execute("UPDATE listener set Active = 'no'")
	conn.commit()
	conn.close()
