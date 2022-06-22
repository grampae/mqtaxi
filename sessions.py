# so sqlite stuff
import readline
import sqlite3
import pandas as pd
import os
from mqworker import *
	
def listsession():
	dbfile = (os.path.dirname(os.path.realpath(__file__))+"/mqt-config.db")
	conn = sqlite3.connect(dbfile)
	cursor = conn.cursor()
	df = pd.read_sql_query("SELECT ID, Transport, Address, Hostname, Username, OS, ListenerHost, ListenerPort, Lastseen, Active from session", conn)
	print("\n")
	if df.empty == True:
		print("No sessions yet, connect to a mqtt listener with active agents.")
	else:
		print(df.to_string(index=False))
	print("\n")
	conn.close()
