import datetime
import random
import uuid
from enum import Enum

import grpc
import os
import proto.grow_pb2_grpc as grpc_proto
import logging

#from libs.request_factory import RequestFactory
from rpc_client.libs.request_factory import RequestFactory

class Mode(Enum):
    SINGLE = 0
    BATCH = 1
    STREAM = 2

class GrowRpcClient(object):
    """
    Client for gRPC functionality
    """

    def __init__(self):
        # self.host = 'localhost'
        self.host = '192.168.1.196'
        self.server_port = '50051'
        # self.channel = None
        self.request_factory = RequestFactory()
        # # instantiate a channel
        # options = {
        #     'grpc.ssl_target_name_override': 'localhost',
        #     'grpc.default_authority': 'localhost'
        # }
        # base_path = os.path.dirname(os.path.abspath(__file__))
        # ca_cert = base_path + '/sec/ca-cert.pem'
        # cert = bytes(open(ca_cert).read(), 'UTF8');
        # creds = grpc.ssl_channel_credentials(cert)
        self.channel = grpc.insecure_channel('192.168.1.196:50051')
        # self.channel = grpc.secure_channel('192.168.1.196:50051', creds, options)
        # bind the client and the server
        self.stub = grpc_proto.GrowServiceStub(self.channel)

    def request_factory(self):
        return self.request_factory


    def send(self, request_iterator):
        """
        Client function to call the rpc for GetServerResponse
        """
        messages = self.stub.sendRequest(request_iterator)
        try:
            for message in messages:
                yield message
        except StopIteration:
            return

    def subscribe_tsl2591(self):
        """
        Client function to call the rpc for GetServerResponse
        """
        request = self.request_factory.tsl2591_subscription()
        response_stream = self.stub.streamTSL2591(request)
        try:
            for response in response_stream:
                yield response
        except StopIteration:
            return


    def read_tsl2591(self, batch_size=1):
        return self.send(iter(batch_size * [self.request_factory.tsl2591_request()]))

    def led_on(self):
        request = self.request_factory.simple_led_request(mode="OPERATOR", state="ON")
        logging.debug(request)
        return self.send(iter([request]))

    def led_off(self):
        request = self.request_factory.simple_led_request(mode="OPERATOR", state="OFF")
        logging.debug(request)
        return self.send(iter([request]))

    def led_auto(self):
        request = self.request_factory.simple_led_request(mode="AUTO")
        logging.debug(request)
        return self.send(iter([request]))
        # requestes_iter = iter([request])
        # res = client.send(requestes_iter)
        # for q in res:_
        #     print("{}\n".format(q))

    def read_system_monitor(self, batch_size=1):
        return self.send(iter(batch_size * [self.request_factory.system_monitor_request()]))

    def read_dht22(self, batch_size=1):
        return self.send(iter(batch_size * [self.request_factory.dht22_request()]))

    def soil_moisture_sensor(self, batch_size=1):
        requests = self.request_factory.soil_moisture_sensor_request()
        return self.send(iter(batch_size * [requests]))

    def request_gen(self, function, count=1):
        for i in range(count):
            yield function()

    # def mock_request(self):
    #     seed = "SYSTEM"
    #     rd = random.Random()
    #     rd.seed(seed)
    #     request_id = str(uuid.UUID(int=rd.getrandbits(128)))
    #     request_proto = proto.GrowRequest()
    #     request_proto.id = "test__request_target_id::" + request_id
    #     request_proto.timestamp = str(datetime.datetime.utcnow().timestamp())
    #     request_proto.type = proto.GrowRequestType.Value('SYSTEM_PARAMS__READ')
    #     return request_proto
    #
    # def request_dht22(self):
    #     seed = "DHT22"
    #     rd = random.Random()
    #     rd.seed(seed)
    #     request_id = str(uuid.UUID(int=rd.getrandbits(128)))
    #     request_proto = proto.GrowRequest()
    #     request_proto.id = "dht22_test__request_target_id" + request_id
    #     request_proto.timestamp = str(datetime.datetime.utcnow().timestamp())
    #     request_proto.type = proto.GrowRequestType.Value('DHT22__READ')
    #     return request_proto
    #
    # def request_simple_led(self, state):
    #     seed = "SIMPLE_LED"
    #     rd = random.Random()
    #     rd.seed(seed)
    #     request_id = str(uuid.UUID(int=rd.getrandbits(128)))
    #     request_proto = proto.GrowRequest()
    #     request_proto.id = "simple_led_test__request_target_id" + request_id
    #     request_proto.timestamp = str(datetime.datetime.utcnow().timestamp())
    #     request_proto.type = proto.GrowRequestType.Value('SIMPLE_LED__OPERATOR')
    #     data = request_proto.data.add()
    #     data.key = "state"
    #     data.value = state
    #     data.type = "string"
    #     return request_proto
    #
    # def request_tsl2591(self):
    #     seed = "TSL2591"
    #     rd = random.Random()
    #     rd.seed(seed)
    #     request_id = str(uuid.UUID(int=rd.getrandbits(128)))
    #     request_proto = proto.GrowRequest()
    #     request_proto.id = "tsl2591_test__request_target_id" + request_id
    #     request_proto.timestamp = str(datetime.datetime.utcnow().timestamp())
    #     request_proto.type = proto.GrowRequestType.Value('TSL2591__READ')
    #     return request_proto
    #
    # def request_tsl2591_stream_start(self, seconds):
    #     seed = "TSL2591-STREAM-START"
    #     rd = random.Random()
    #     rd.seed(seed)
    #     request_id = str(uuid.UUID(int=rd.getrandbits(128)))
    #     request_proto = proto.GrowRequest()
    #     request_proto.id = "tsl2591_stream_start_test__request_target_id" + request_id
    #     request_proto.timestamp = str(datetime.datetime.utcnow().timestamp())
    #     request_proto.type = proto.GrowRequestType.Value('TSL2591__STREAM_START')
    #     data = request_proto.data.add()
    #     data.key = "frquency_in_seconds"
    #     data.value = str(seconds)
    #     data.type = "string"
    #     return request_proto


def make_iter(list):
    return iter(list)

if __name__ == '__main__':
    client = GrowRpcClient()
    check = True
    print("GROW RPC CLI")
    while check is True:
        cmd = str(input("n [node info], d [dht22], lu [led on (up)] , ld [led off (down)], tsl [tsl2591], q [quit]:\n"))
        if cmd == "q":
            check = False
        elif cmd == "n":
            # data = client.send(iter([request]))
            res = client.read_system_monitor()
            for q in (res):
                print("{}\n".format(q))
        elif cmd == "d":
            res = client.read_dht22()
            for q in (res):
                print("{}\n".format(q))
        elif cmd == "lu":
            res = client.led_on()
            for q in res:
                print("{}\n".format(q))
        elif cmd == "la":
            res = client.led_auto()
            for q in res:
                print("{}\n".format(q))
        elif cmd == "m":
            res = client.soil_moisture_sensor()
            for q in res:
                print("{}\n".format(q))
        # elif cmd == "ld":
        #     request = client.request_simple_led("OFF")
        #     requestes_iter = iter([request])
        #     res = client.send(requestes_iter)
        #     for q in res:
        #         print("{}\n".format(q))
        #     # print("SIMPLE LED Request:\n{}\n\nSIMPLE LED Response:\n{}".format(request, response))
        # elif cmd == "tsl":
        #     cache = []
        #     while True:
        #         request = client.request_tsl2591()
        #         requestes_iter = iter([request])
        #         res = client.send(requestes_iter)
        #         for q in res:
        #             print("{}\n".format(q))
        elif cmd == "str":
            res = client.tsl2591_request()
            while True:
              print(next(res))


        # elif cmd == "all":
        #     system_monitor = client.mock_request()
        #     tsl2591 = client.request_tsl2591()
        #     led_on = client.request_simple_led("ON")
        #     led_off = client.request_simple_led("OFF")
        #     requestes = [system_monitor, tsl2591, led_on]
        #     requestes_iter = iter(requestes)
        #     # for request in requestes_iter:
        #     #     print("{}\n".format(request))
        #     www = client.send(requestes_iter)
        #     for q in www:
        #         print("{}\n".format(q))

            # print(responses)

    # print(f'{result}')

