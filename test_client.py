"""MQTT adaptor"""
from time import sleep
from json import dumps
from random import randint
import paho.mqtt.client as mqtt

QOS = 2


def create_client():
    """create client handle"""
    client = mqtt.Client("student2", clean_session=False)

    client.connect(host="localhost")
    client.loop_start()

    return client


def close_client(client):
    """close client"""
    client.disconnect()
    client.loop_stop()


def main():
    """main func"""
    client = create_client()
    devices = ["UPB/Mongo","UPB/Gas","Ceva/RPi"]
    for i in range(100):
        k = randint(0,2)
        bat = randint(50,100)
        hum = randint(50,100)
        tmp = randint(50,100)
        data = {
            "BAT": bat,
            "HUM": hum,
            "TMP": tmp
        }
        msg = dumps(data)
        client.publish(devices[k], msg, qos=QOS, retain=True)
        sleep(2)

    close_client(client)



if __name__ == "__main__":
    main()
