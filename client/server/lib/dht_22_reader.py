import datetime
import json
import os
import uuid
import random
import board
import proto.grow_pb2 as proto
import adafruit_dht
from google.protobuf.json_format import Parse
seed = "DHT22"

rd = random.Random()
rd.seed(seed)
os.environ['GRPC_TRACE'] = 'all'
os.environ['GRPC_VERBOSITY'] = 'DEBUG'

class DHT22RequestHandler():
    def __init__(self):
    # Initial the dht device, with data pin connected to:
        self.dhtDevice = adafruit_dht.DHT22(board.D4)
        self.SENSOR_TYPE = "DHT22"
        self.uuid = uuid.UUID(int=rd.getrandbits(128))

    def read(self):
        temperature, humidity = -1, 1
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
        humidity, temperature = self.read()
        data = {
            'id': "SYSTEM__" + str(self.uuid),
            'timestamp': str(datetime.datetime.utcnow()),
            'data': {
                'sensor_type': self.SENSOR_TYPE,
                'sensor_id': "DHT22__01",
                'sensor_name': "GROW__DHT22__01",
                'timestamp': str(datetime.datetime.utcnow()),
                'sensor_data': [
                    {'key': 'humidity', 'value': "humidity", 'type': "str"},
                    {'key': 'temperature', 'value': "temperature", 'type': "str"},
                ]
            }
        }
        response = Parse(json.dumps(data), response_proto)
        return response

