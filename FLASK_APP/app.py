import logging
import eventlet
import json
from flask import Flask, render_template
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['MQTT_BROKER_URL'] = 'broker.hivemq.com'  # use the free broker from HIVEMQ
app.config['MQTT_BROKER_PORT'] = 1883  # default port for non-tls connection
app.config['MQTT_USERNAME'] = ''  # set the username here if you need authentication for the broker
app.config['MQTT_PASSWORD'] = ''  # set the password here if the broker demands authentication
app.config['MQTT_KEEPALIVE'] = 5  # set the time interval for sending a ping to the broker to 5 seconds
app.config['MQTT_TLS_ENABLED'] = False  # set TLS to disabled for testing purposes

mqtt = Mqtt(app)
socketio = SocketIO(app)
bootstrap = Bootstrap(app)

@app.route('/')
def index():
    return render_template('index.html')

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    #Sub 2 chosen topics 
    print('on connect')
    mqtt.subscribe('Topic/TempHumi')
    mqtt.subscribe('Topic/Mois')

# @mqtt.on_message()
# def handle_mqtt_message(client, userdata, message):
#     topic=message.topic    
#     #data = handle_message(message)
#     print('topic')
#     print('topic123')
#     print('topic214')
#     print(message.payload.decode())
#     print(topic)
#     print(client)
#     print(userdata)
#     print(message)
#     mqtt.publish('Topic/TempHumi','Hello World this is payload')

def handle_message(message):
    payload=json.loads(message.payload.decode())
    data = dict()
    if message.topic == "Topic/TempHumi":
        data = dict(
        temp= payload[0]["values"][0],
        humid= payload[0]["values"][1],
    )
    if message.topic == "Topic/Mois":
        data = dict(
            mois = payload[0]["values"][0],
        )        
    return data

@socketio.on('publish')
def handle_publish(json_str):
    data = json.loads(json_str)
    mqtt.publish(data['topic'], data['message'])
    # print('publish')

@socketio.on('subscribe')
def handle_subscribe(json_str):
    data = json.loads(json_str)
    mqtt.subscribe(data['topic'])
    # print('subcribe')

@socketio.on('unsubscribe_all')
def handle_unsubscribe_all():
    mqtt.unsubscribe_all()

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )
    socketio.emit('mqtt_message', data=data)