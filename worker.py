import paho.mqtt.client as mqtt

# Set broker here
broker = "appinfolive.com"
port = 8883
agent = ""
# Define subscriptions
topic_out = "output/#"
topic_err = "error/#"
topic_cwd = "cwd/#"
# mqtt server creds
username = 'dirtysphynx'
password = 'flatbedgiraffe'

def on_connect(client, userdata, flags, rc):
    client.subscribe(topic_out)
    client.subscribe(topic_err)
    client.subscribe(topic_cwd)
def on_message(client, userdata, msg):
    output = msg.payload.decode('UTF-8')
    print("\r\n"+output+" ", end="")

def Main():
	client = mqtt.Client()
	client.tls_set()
	client.on_connect = on_connect
	client.on_message = on_message
	client.username_pw_set(username, password)

	client.connect(broker, port, 60)
	client.loop_forever()
