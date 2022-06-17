import RPi.GPIO as GPIO
from time import sleep
import datetime
import json
import os
import uuid
import random
import proto.grow_pb2 as proto
from google.protobuf.json_format import Parse


seed = "SIMPLE_LED"
rd = random.Random()
rd.seed(seed)

class SimpleLedDriver(object):
    
    def __init__(self, bcm_pin_number=26):
        self.singnal_pin = bcm_pin_number
        self.state = "OFF"
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.singnal_pin, GPIO.OUT)
        self.devic_type = "SIMPLE_LED"
        self.uuid = uuid.UUID(int=rd.getrandbits(128))
        self.check_led()

    def check_led(self):
        print('LED CHECK: 10 x puled up and down in pulse manner')
        for i in range(10):
            GPIO.output(self.singnal_pin, GPIO.HIGH)
            if(i%2==0):
                sleep(0.4)
            else:
                sleep(0.3)
            GPIO.output(self.singnal_pin, GPIO.LOW)
            sleep(0.1)
        print("OK")
        
    def get_mode(self, request):
        print(request)
        for element in request.data:
            if element.key == "mode":
                return element.value        

    def get_state(self, request):
        print(request)
        for element in request.data:
            if element.key == "state":
                return element.value 

    def set_state(self, state):
        if state == "ON":
            self.state = "ON"
            self._power_on()
        elif state == "OFF":
            self.state = "OFF"
            self._power_off()

    def set_mode(self, mode):
        if mode in ["OPERATOR", "AUTO"]:
            self.mode = mode         
    
    def _power_on(self):
        GPIO.output(self.singnal_pin, GPIO.HIGH)

    def _power_off(self):
        GPIO.output(self.singnal_pin, GPIO.LOW)

    def response(self, request, timstamp=str(datetime.datetime.utcnow())):
        mode =  self.get_mode(request)        
        state = self.get_state(request)
        self.set_state(state)
        self.set_mode(mode)        
        response_proto = proto.GrowResponse()
        respone_data = {
            'id': "{0}__{1}".format(self.devic_type, str(self.uuid)),
            'timestamp': timstamp,
            'status': response_proto.Status.OK,
            'state': {
                'device_type': self.devic_type,
                'device_id':  self.devic_type + "__01",
                'device_name': "GROW__" + self.devic_type + "__01",
                'timestamp': str(datetime.datetime.utcnow()),
                'data': [
                    {'key': 'mode', 'value': self.mode, 'type': "str"},                    
                    {'key': 'state', 'value': self.state, 'type': "str"},

                ]
            }
        }
        response = Parse(json.dumps(respone_data), response_proto)
        return response




# def main():
#     stateON = "ON"
#     stateOFF = "OFF"
#     requestON = led_request(stateON)
#     led = SimpleLedDriver(26)
#     print(led.response(requestON))
#     sleep(3)
#     requestOFF = led_request(stateOFF)
#     print(led.response(requestOFF))

# if __name__ == '__main__':
#     main()

    
# def request_dht22(self):
#     seed = "SYSTEM"
#     rd = random.Random()
#     rd.seed(seed)
#     id = str(uuid.UUID(int=rd.getrandbits(128)))
#     request_proto = proto.Request();
#     request_proto.id = "dht22_test__request_target_id" + id
#     request_proto.timestamp = str(datetime.datetime.utcnow().timestamp())
#     request_proto.type = proto.Request.RequestType.DHT22__READ
#     target = request_proto.targets.add()
#     target.id = "dht22_test__request_target_id"
#     target.channel_name = "dht22_test__channel_name"
#     target.address = self.host
#     return request_proto
    
    
# message Request
# {
#   optional string id = 1;
#   optional string timestamp = 2;
#   optional RequestType type = 3;
#   optional Options options = 4;
#   optional Data data = 5;

#   enum RequestType {
#     UNKNOWN = 0;
#     ALL__READ = 1;
#     SYSTEM_PARAMS__READ = 2;
#     DHT22__READ = 3;
#     SIMPLE_LED__WRITE = 4;
#     TSL2591__READ = 5;
#   }
  
#   message Options {
#     optional string key = 1;
#     optional string value = 2;
#   }
# }