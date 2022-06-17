import datetime
import json
import os
import uuid
import random
import proto.grow_pb2 as proto
import board
from google.protobuf.json_format import Parse
import lib.ads1x15 as ads1x15
import time
import lib.utils as utils
seed = "SOIL_MOISTURE"

rd = random.Random()
rd.seed(seed)


class CapacitiveSoilMositureSensorReader(object):
    def __init__(self, ads1x15_channel):
        self.ads1x15_channel = ads1x15_channel
        self.ads1x15 = ads1x15.AdcADS1x15(self.ads1x15_channel)
        self.SENSOR_TYPE = "SOIL_MOISTURE"
        self.uuid = uuid.UUID(int=rd.getrandbits(128))
        self.upperboundry = 1600.0
        self.lowerboundry = 1200.0


    def read(self):
        mositure = ""
        try:
            # Print the values to the serial port
            mositure_raw = self.ads1x15.convert()
            mositure = utils.Utils.normalize(mositure_raw, self.lowerboundry, self.upperboundry)
        except RuntimeError as error:
            # Errors happen fairly often, DHT's are hard to read, just keep going
            print(error.args[0])
        except Exception as error:
            raise error
        return mositure_raw, mositure

    def response(self):
        response_proto = proto.GrowResponse()
        moisture_raw, moisture = self.read()
        if moisture > 100:
            moisture = 100
        if moisture < 0:
            moisture = 0    
        data = {
            'id': "SOIL_MOISTURE__" + str(self.uuid),
            'timestamp': str(datetime.datetime.utcnow()),
            'state': {
                'device_type': self.SENSOR_TYPE,
                'device_id': "SOIL_MOISTURE__01",
                'device_name': "GROW__SOIL_MOISTURE__01",
                'timestamp': str(datetime.datetime.utcnow()),
                'data': [
                    {'key': 'moisture_raw', 'value': str(moisture_raw), 'type': "str"},
                    {'key': 'moisture', 'value': str(moisture), 'type': "str"},                    
                ]
            }
        }
        response = Parse(json.dumps(data), response_proto)
        return response


if __name__ == '__main__':
    sum = 0
    for i in range(1, 31):
        adc = ads1x15.AdcADS1x15(0)
        mositure_raw = adc.convert()
        mositure = utils.Utils.normalize(mositure_raw, 2550.0, 2700.0)
        sum+= mositure_raw
        print(i,  "          ", sum/(i), "          ", mositure_raw, "          ", mositure)
        time.sleep(1)