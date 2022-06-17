from concurrent import futures
import time
import grpc
import proto.grow_pb2_grpc as grpc_proto
import proto.grow_pb2 as proto

from threading import Thread
import datetime

from grpc_channelz.v1 import channelz

import lib.system_params__getter as system_monitor
import lib.simple_led__setter as simple_led
import lib.tsl2591__reader as tsl2591__reader
import lib.dht22__reader as dht22__reader
import lib.capacitive_soil_moisture_sensor__reader as capacitive_soil_moisture_sensor__reader

class GrowServiceDeviceInit(object):
    def __init__(self, simple_led_driver_pin):
        self.devices = {
            "system_monitor": system_monitor.SystemParamsRequestHandler(),
            "simple_led": simple_led.SimpleLedDriver(simple_led_driver_pin),
            "tsl2591": tsl2591__reader.TSL2591Reader(),
            "dht22": dht22__reader.DHT22Reader(),
            "soil_moisture_sensor": capacitive_soil_moisture_sensor__reader.CapacitiveSoilMositureSensorReader("A0")
        }

    def system(self):
        return self.devices['system_monitor']

    def simple_led(self):
        return self.devices['simple_led']

    def tsl2591(self):
        return self.devices['tsl2591']

    def dht22(self):
        return self.devices['dht22']

    def capacitive_soil_moisture_sensor(self):
        return self.devices['soil_moisture_sensor']

class GrowService(grpc_proto.GrowServiceServicer):
    def __init__(self, simple_led_pin):
        self.system = GrowServiceDeviceInit(simple_led_pin)
        self.devices = self.system.devices
        self.settings = {
            "tsl2591_stream" : 0,
            "led_auto": 1
        }
        self.monitor_tsl2591 = Thread(target=self.monitor_tsl2591_and_maintain_led)
        self.monitor_tsl2591.start()

    def monitor_tsl2591_and_maintain_led(self):
        while True:
            if self.settings['led_auto'] == 1:
                lux, full, ir = self.devices['tsl2591'].read()
                if(lux <= 15.0):
                    #print("["+str(datetime.datetime.utcnow())+"]    LUX =" + str("%.2f" % lux) +"      < 20.0[lux]           LED ON")
                    self.devices['simple_led'].set_state("ON")
                    
                else:
                    #print("["+str(datetime.datetime.utcnow())+"]    LUX =" + str("%.2f" % lux) +"      20 20.0[lux],         LED OFF")
                    self.devices['simple_led'].set_state("OFF")
                time.sleep(0.5)
            

    def sendRequest(self, request_iterator, context):
        for r in request_iterator:
            try:
                if r.type == proto.GrowRequestType.Value('SYSTEM_PARAMS__READ'):
                    yield self.devices['system_monitor'].response()
                elif r.type == proto.GrowRequestType.Value('TSL2591__READ'):
                    yield self.devices['tsl2591'].response()
                elif r.type == proto.GrowRequestType.Value('DHT22__READ'):
                    yield self.devices['dht22'].response()         
                elif r.type == proto.GrowRequestType.Value('SOIL_MOISTURE_SENSOR__READ'):
                    yield self.devices['soil_moisture_sensor'].response()                                 
                elif r.type == proto.GrowRequestType.Value('SIMPLE_LED__OPERATOR'):
                    for item in r.data:
                        if item.key == 'mode':
                            if( item.value=="AUTO"):
                                self.settings['led_auto'] = 1
                            else:
                                self.settings['led_auto'] = 0
                        yield self.devices['simple_led'].response(r)    
            except StopIteration:
                return

    def streamTSL2591(self, init_request, context):
        if init_request.type == proto.GrowRequestType.Value('TSL2591__STREAM_START'):
            self.settings['tsl2591_stream'] = 1;
            for option in init_request.data:
                if option.key == "frquency_in_seconds":
                    frquency_in_seconds = int(option.value)
                    print(str(frquency_in_seconds) + " sec")

            while self.settings['tsl2591_stream'] == 1:
                yield self.devices['tsl2591'].response()
                time.sleep(frquency_in_seconds)

                


