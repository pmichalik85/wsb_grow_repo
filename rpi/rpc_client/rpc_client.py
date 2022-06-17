import datetime
import random
import uuid
import grpc
import time
import proto.grow_pb2 as proto
import proto.grow_pb2_grpc as grpc_proto

class GrowRpcClient(object):
    """
    Client for gRPC functionality
    """

    def __init__(self):
        #self.host = 'localhost'
        self.host = '192.168.1.196'
        self.server_port = '50051'

        # instantiate a channel
        base_path = os.path.dirname(os.path.abspath(__file__))
        ca_cert = base_path + '/sec/ca.pem'
        private_key = open(keyfile, 'rb').read()

        

        self.channel = grpc.insecure_channel(self.host +":"+self.server_port)

        #self.channel = grpc.insecure_channel('localhost:50051')

        # bind the client and the server
        self.stub = grpc_proto.GrowServiceStub(self.channel)

    def send(self, request):
        """
        Client function to call the rpc for GetServerResponse
        """
        # if request.type == proto.Request.RequestType.SYSTEM_PARAMS__READ:
        return self.stub.read_node_info(request)
        # if request.type == proto.Request.RequestType.DHT22__READ:
        #     return self.stub.read_DHT22(request)


    def mock_request(self):
        seed = "SYSTEM"
        rd = random.Random()
        rd.seed(seed)
        id = str(uuid.UUID(int=rd.getrandbits(128)))
        request_proto = proto.Request();
        request_proto.id = "test__request_target_id::" + id
        request_proto.timestamp = str(datetime.datetime.utcnow().timestamp())
        request_proto.type = 2
        return request_proto

    def request_dht22(self):
        seed = "DHT22"
        rd = random.Random()
        rd.seed(seed)
        id = str(uuid.UUID(int=rd.getrandbits(128)))
        request_proto = proto.Request();
        request_proto.id = "dht22_test__request_target_id" + id
        request_proto.timestamp = str(datetime.datetime.utcnow().timestamp())
        request_proto.type = proto.Request.RequestType.DHT22__READ
        return request_proto


    def request_simple_led(state):
        seed = "SIMPLE_LED"
        rd = random.Random()
        rd.seed(seed)
        id = str(uuid.UUID(int=rd.getrandbits(128)))
        request_proto = proto.Request();
        request_proto.id = "simple_led_test__request_target_id" + id
        request_proto.timestamp = str(datetime.datetime.utcnow().timestamp())
        request_proto.type = proto.Request.RequestType.SIMPLE_LED__WRITE
        data = request_proto.data.add()
        data.key = "state"
        data.value = state
        data.type = "string"
        return request_proto


if __name__ == '__main__':
    client = GrowRpcClient()
    check = True
    print("GROW RPC CLI")
    while(check is True):
        cmd = str(input("n [node info], d [dht22],  q [quit]:\n"))
        if cmd == "q":
            check = False
        elif cmd == "n":
            request = client.mock_request()
            response = client.send(request)
            print("SYSTEM Request:\n{}\n\nSYSTEM Response:\n{}".format(request, response))
        elif cmd == "d":
            request = client.request_dht22()
            response = client.send(request)
            print("DHT22 Request:\n{}\n\nDHT22 Response:\n{}".format(request, response))
        elif cmd == "lon":
            request = client.request_simple_led("ON")
            response = client.send(request)
            print("SIMPLE LED Request:\n{}\n\nDHT22 Response:\n{}".format(request, response))    
        elif cmd == "lon":
            request = client.request_simple_led("OFF")
            response = client.send(request)
            print("SIMPLE LED Request:\n{}\n\nDHT22 Response:\n{}".format(request, response)) 

    # print(f'{result}')
