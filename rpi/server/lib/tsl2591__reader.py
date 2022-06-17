import datetime
import json
import proto.grow_pb2 as proto
from google.protobuf.json_format import ParseDict, Parse
from python_tsl2591 import tsl2591
import uuid
import random

seed = "TSL2591"



class TSL2591Reader(object):
    def __init__(self):

        self.device_type = "TSL2591"
        rd = random.Random()
        rd.seed(self.device_type)
        self.uuid = uuid.UUID(int=rd.getrandbits(128))
        self.sensor = tsl2591()

    def read(self):
        full, ir = self.sensor.get_full_luminosity()
        lux = self.sensor.calculate_lux(full, ir)
        return lux, full, ir

    def response(self, timestamp=str(datetime.datetime.utcnow())):
        response_proto = proto.GrowResponse()
        lux, full, ir = self.read()
        system_data = {
            'id': "TSL2591__" + str(self.uuid),
            'timestamp': timestamp,
            'status': response_proto.Status.OK,
            'state': {
                'device_type': self.device_type,
                'device_id': "TSL2591__01",
                'device_name': "GROW__TSL2591__01",
                'timestamp': str(datetime.datetime.utcnow()),
                'data': [
                    {'key': 'lux', 'value': str(lux), 'type': "float"},
                    {'key': 'full', 'value': str(full), 'type': "int64"},
                    {'key': 'ir', 'value': str(ir),'type': "int64"}
                ]
            }
        }
        response = Parse(json.dumps(system_data), response_proto)
        return response