import json
import os
import platform
import random
from subprocess import check_output
from re import findall 

import time, uuid
import requests
import psutil
import datetime
import proto.grow_pb2 as proto
import psutil
from google.protobuf.json_format import ParseDict, Parse

seed = "SYSTEM"

rd = random.Random()
rd.seed(seed)

from google.protobuf.json_format import ParseDict


class SystemParamsRequestHandler(object):
    def __init__(self):
        self.uuid = uuid.UUID(int=rd.getrandbits(128))
        self.device_type = "SYSTEM"

    def get_temp(self):
        temp = check_output(["vcgencmd","measure_temp"]).decode("UTF-8")
        return(findall("\d+\.\d+",temp)[0])

    def response(self, timestamp=str(datetime.datetime.utcnow())):
        response_proto = proto.GrowResponse()
        cpu = str(psutil.cpu_percent())

        memory = str(psutil.virtual_memory().percent)
        # if psutil.sensors_temperatures(fahrenheit=False).keys().__contains__("cpu_thermal"):
        #     heat = str(psutil.sensors_temperatures(fahrenheit=False))["cpu_thermal"][0]
        # else:
        cpu_temp = self.get_temp()
        #wifi_stats =  ["in", "out"]#psutil.net_io_counters(pernic=True, nowrap=True)[[i for i in psutil.net_if_addrs() if i.startswith('w')][0]]
        # wifi_incoming = str(wifi_stats[1])
        # wifi_outgoing = str(wifi_stats[0])
        system_data = {
            'id': "SYSTEM__" + str(self.uuid),
            'timestamp': timestamp,
            'status': response_proto.Status.OK,
            'state': {
                'device_type': self.device_type,
                'device_id': "SYSTEM__01",
                'device_name': "GROW__SYSTEM__01",
                'timestamp': str(datetime.datetime.utcnow()),
                'data': [
                    {'key': 'os', 'value': str(os.uname()), 'type': "str"},
                    {'key': 'cpu', 'value': cpu, 'type': "float"},
                    {'key': 'memory', 'value': memory,'type': "float"},
                    {'key': 'cpu_temperature', 'value': cpu_temp, 'type': "float"},
                    # {'key': 'wifi_incoming', 'value': wifi_incoming, 'type': "float"},
                    # {'key': 'wifi_outgoing', 'value': wifi_outgoing, 'type': "float"}
                ]
            }
        }
        response = Parse(json.dumps(system_data), response_proto)

        return response

