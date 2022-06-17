import datetime
import json
import os
import uuid
import random
import proto.grow_pb2 as proto
import adafruit_dht
import board

from google.protobuf.json_format import Parse
seed = "DHT22"

rd = random.Random()
rd.seed(seed)

class DHT22Reader():
    def __init__(self):
    # Initial the dht device, with data pin connected to:
    
        self.dhtDevice = adafruit_dht.DHT22(board.D4)
        self.SENSOR_TYPE = "DHT22"
        self.uuid = uuid.UUID(int=rd.getrandbits(128))

    def read(self):
        temperature = ""
        humidity = ""
        try:
            # Print the values to the serial port
            temperature = str(self.dhtDevice.temperature)
            humidity = str(self.dhtDevice.humidity)
        except RuntimeError as error:
            # Errors happen fairly often, DHT's are hard to read, just keep going
            print(error.args[0])
        except Exception as error:
            self.dhtDevice.exit()
            raise error
        return temperature, humidity

    def response(self):
        response_proto = proto.GrowResponse()
        temperature, humidity = self.read()
        data = {
            'id': "SYSTEM__" + str(self.uuid),
            'timestamp': str(datetime.datetime.utcnow()),
            'state': {
                'device_type': self.SENSOR_TYPE,
                'device_id': "DHT22__01",
                'device_name': "GROW__DHT22__01",
                'timestamp': str(datetime.datetime.utcnow()),
                'data': [
                    {'key': 'air_humidity', 'value': humidity, 'type': "str"},
                    {'key': 'air_temperature', 'value': temperature, 'type': "str"},
                ]
            }
        }
        response = Parse(json.dumps(data), response_proto)
        return response

        