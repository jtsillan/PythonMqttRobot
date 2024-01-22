import random
import paho.mqtt.client as mqtt
import time
import json


EMOTIONS = ["angry", "scared", "sad", "happy", "neutral", "disgust", "surprised"]
data_keys = ["person_id", "emotion", "emotion_confidence"]
data_dict = dict.fromkeys(data_keys)
info_keys = ["info"]
info_dict = dict.fromkeys(info_keys)
emotion_index = 0
mqtt_topic = "emotions/finland"


def on_message(client_on_message, userdata, message):
    print("Client is: ", client_on_message)
    print("Userdata is: ", userdata)
    print("message received ", str(message.payload.decode("utf-8")))
    print("message topic=", message.topic)
    print("message qos=", message.qos)
    print("message retain flag=", message.retain)


def on_connect(client_on_connect, userdata, flags, rc):
    if rc == 0:
        print("connected OK Returned code=", rc)
    else:
        print("Bad connection Returned code=", rc)


while True:
    try:
        client = mqtt.Client("BIP1")
        client.on_message = on_message
        client.on_connect = on_connect
        # client.connect("localhost")
        client.connect("test.mosquitto.org")
        emotion_prefix = random.randint(0, 6)
        emotion_prob = random.uniform(0.4, 0.9)
        data_dict["person_id"] = emotion_index
        data_dict["emotion"] = EMOTIONS[emotion_prefix]
        data_dict["emotion_confidence"] = emotion_prob
        print(json.dumps(data_dict))
        # client.publish("/bip/emotion", json.dumps(data_dict), 1)
        client.publish(mqtt_topic, json.dumps(data_dict), 1)
        emotion_index += 1
        time.sleep(2)

        if emotion_prefix == 3:
            info_dict["info"] = "Too many persons in front off the camera"
            # client.publish("/bip/emotion", json.dumps(info_dict), 1)
            client.publish(mqtt_topic, json.dumps(info_dict), 1)
            print(json.dumps(info_dict))
            time.sleep(2)
        elif emotion_prefix == 2:
            info_dict["info"] = "Ready for a new person"
            # client.publish("/bip/emotion", json.dumps(info_dict), 1)
            client.publish(mqtt_topic, json.dumps(info_dict), 1)
            print(json.dumps(info_dict))
            time.sleep(2)

    except Exception as ex:
        print(ex)
