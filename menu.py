from art import tprint
from cmd import Cmd
from listener import *
from sessions import *
from generate import *
import subprocess
import readline
import time
import os


ondutyp = "On-Duty > "
offdutyp = "Off-Duty > "
dbfile = (os.path.dirname(os.path.realpath(__file__))+"/mqt-config.db")
createsess()
createlisten()
def introa():
	createsess()
	os.system('clear')
	tprint('MQTaxi','random')
	print("MQTaxi: mqtt c2 client.  (type help or ?)")
	conn = sqlite3.connect(dbfile)
	cursor = conn.cursor()
	cur = conn.cursor()
	cur.execute("SELECT COUNT(1) FROM session")
	farescount = cur.fetchone()[0]
	if farescount > 0:
		print("Fares: "+str(farescount))
	else:
		print("Fares: 0")
	conn.close()
	print(("*" * 45)+"\n")

class mainmenu(Cmd):
	def do_clear(self, args):
		'''\nClear the screen\n'''
		os.system('clear')
		domainmenu()
	def do_version(self, args):
		'''\nDisplay version of MQTaxi\n'''
		print("MQTaxi version 0.1 Beta")
	def do_config(self, args):
		'''\nConfigure mqtt listeners to connect the client and generate agents\n'''
		doconfigmenu()
	def do_listeners(self, args):
		'''\nDisplay configured listeners\n'''
		listlisten()
	def do_sessions(self, args):
		'''\nDisplay active agents connected to the currently active listener\n'''
		listsession()
	def do_uselistener(self, args):
		'''\nSet a mqtt listener as active\n'''
		dropsess()
		createsess()
		activatelis()
		domainmenu()
	def do_usesession(self, args):
		'''\nConnect to an agent with a reverse shell\n'''
		taxi = (os.path.dirname(os.path.realpath(__file__))+"/taxi.py")
		subprocess.call("python3 "+taxi, shell=True)
		domainmenu()
	def do_discolistener(self, list):
		'''\nDisconnect from currently active listener\n'''
		discolistener()
		dropsess()
		domainmenu()
	def do_exit(self, args):
		'''\nExit MQTaxi\n'''
		dropsess()
		discolistener()
		quit()
class configmenu(Cmd):
	def do_clear(self, args):
		'''\nClear the screen\n'''
		os.system('clear')
		doconfigmenu()
	def do_uselistener(self, args):
		'''\nSet a mqtt listener as active\n'''
		dropsess()
		createsess()
		activatelis()
		doconfigmenu()
	def do_listeners(self, list):
		'''\nDisplay configured listeners\n'''
		listlisten()
	def do_discolistener(self, list):
		'''\nDisconnect from currently active listener\n'''
		discolistener()
		dropsess()
		doconfigmenu()
	def do_sessions(self, args):
		'''\nDisplay active agents connected to the currently active listener\n'''
		listsession()
	def do_usesession(self, args):
		'''\nConnect to an agent with a reverse shell\n'''
		taxi = (os.path.dirname(os.path.realpath(__file__))+"/taxi.py")
		subprocess.call("python3 "+taxi, shell=True)
		doconfigmenu()
	def do_back(self, args):
		'''\nReturn to main menu\n'''
		domainmenu()
	def do_add(self, args):
		'''\nAdd a mqtt listener\n'''
		addlisten()
		doconfigmenu()
	def do_remove(self, args):
		'''\nRemove a mqtt listener\n'''
		dellisten()
		doconfigmenu()
	def do_generate(self,args):
		'''\nGenerate agent to communicate with listener\n'''
		agentlist()
	def do_exit(self, args):
		'''\nExit MQTaxi\n'''
		dropsess()
		discolistener()
		quit()
def getprompt():
	conn = sqlite3.connect(dbfile)
	cursor = conn.cursor()
	cur = conn.cursor()
	cur.execute("SELECT ID FROM listener where Active = 'yes' LIMIT 1")
	if cur.fetchone():
		op.prompt = ondutyp
		og.prompt = ondutyp+"Configuration >"
	else:
		op.prompt = offdutyp
		og.prompt = offdutyp+"Configuration >"
	conn.close()
op=mainmenu()
op.doc_header = "MQTaxi main menu commands (type help or ? <topic>):"
og=configmenu()
og.doc_header = "MQTaxi listener menu commands (type help or ? <topic>):"
def doconfigmenu():
	getprompt()
	og.cmdloop(intro=introa())
def domainmenu():
	getprompt()
	op.cmdloop(intro=introa())
domainmenu()
