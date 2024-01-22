import paho.mqtt.client as mqtt
import ast
import time
import tkinter as tk


def on_connect(client_oc, userdata, flags, rc):
    print("Connected with result code: " + str(rc))
    client_oc.subscribe("camera/emotions")


def on_message(client, userdata, msg):
    con_dict = msg.payload.decode("UTF-8")
    my_data = ast.literal_eval(con_dict)
    print(my_data)

    if my_data['action'] == 0:
        print("Move left at: " + time.strftime("%H:%M:%S, %m/%d/%Y"))
    elif my_data['action'] == 1:
        print("Move right at: " + time.strftime("%H:%M:%S, %m/%d/%Y"))


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("test.mosquitto.org")
client.loop_forever()
