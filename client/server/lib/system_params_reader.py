import datetime
import json
import os
import platform
import random
import uuid

import proto.grow_pb2 as proto
import psutil
from google.protobuf.json_format import ParseDict, Parse

seed = "NODE_INFO"

rd = random.Random()
rd.seed(seed)

from google.protobuf.json_format import ParseDict


class SystemParamsRequestHandler(object):
    def __init__(self):
        self.uuid = uuid.UUID(int=rd.getrandbits(128))
        self.SENSOR_TYPE = "NODE_INFO"

    def response(self):
        response_proto = proto.Response()
        cpu = str(psutil.cpu_percent())

        memory = str(psutil.virtual_memory().percent)
        # if psutil.sensors_temperatures(fahrenheit=False).keys().__contains__("cpu_thermal"):
        #     heat = str(psutil.sensors_temperatures(fahrenheit=False))["cpu_thermal"][0]
        # else:
        heat="N/A"
        wifi_stats = "n/a"# psutil.net_io_counters(pernic=True, nowrap=True)[[i for i in psutil.net_if_addrs() if i.startswith('w')][0]]
        wifi_incoming = str(wifi_stats[1])
        wifi_outgoing = str(wifi_stats[0])
        system_data = {
            'id': "SYSTEM__" + str(self.uuid),
            'timestamp': str(datetime.datetime.utcnow()),
            'data': {
                'sensor_type': self.SENSOR_TYPE,
                'sensor_id': "SYSTEM__01",
                'sensor_name': "GROW__SYSTEM__01",
                'timestamp': str(datetime.datetime.utcnow()),
                'sensor_data': [
                    {'key': 'os', 'value': str(os.uname()), 'type': "str"},
                    {'key': 'cpu', 'value': cpu, 'type': "float"},
                    {'key': 'memory', 'value': memory,'type': "float"},
                    {'key': 'cpu_temperature', 'value': heat, 'type': "float"},
                    {'key': 'wifi_incoming', 'value': wifi_incoming, 'type': "float"},
                    {'key': 'wifi_outgoing', 'value': wifi_outgoing, 'type': "float"}
                ]
            }
        }
        response = Parse(json.dumps(system_data), response_proto)

        return response

