from concurrent import futures

import grpc
import proto.grow_pb2_grpc as grpc_proto
import proto.grow_pb2 as proto
import lib.response_builder as response_builder
from grpc_health.v1 import health
from grpc_health.v1 import health_pb2
from grpc_health.v1 import health_pb2_grpc

from grpc_channelz.v1 import channelz

import lib.system_params_reader as system_params_reader
import lib.dht_22_reader as dht_22_reader

PARAMS_READER = system_params_reader.SystemParamsRequestHandler()
DHT22__READER = dht_22_reader.DHT22RequestHandler()

class GrowService(grpc_proto.GrowServiceServicer):
    # def __init__(self):
    #     self.
    # def __init__(self, *args, **kwargs):
    #     pass

    def read_node_info(self, request, context):
           # if request.type == proto.Request.type.SYSTEM_PARAMS__READ:
        response = PARAMS_READER.response()
        return response

    def read_DHT22(self, request, context):
           # if request.type == proto.Request.type.SYSTEM_PARAMS__READ:
        response = DHT22__READER.response()
        return response


# if __name__ == '__main__':
#     serve()
