import proto.grow_pb2 as grow_proto


import random
import uuid
import datetime

class RequestBuilder(object):
    def __init__(self):
        self.request = None
        self.init_timestamp = None

    def _new(self):
        self.request = grow_proto.GrowRequest()
        self.init_timestamp = str(datetime.datetime.utcnow())

    def id(self, seed_prefix):
        self._new()
        seed = "{0}{1}".format(seed_prefix, self.request.timestamp)
        rd = random.Random()
        rd.seed(seed)
        self.request.id = "{0}::{1}".format(seed_prefix, str(uuid.UUID(int=rd.getrandbits(128))).replace("-", ""))
        return self

    def timestamp(self):
        self.request.timestamp = self.init_timestamp
        return self

    def type(self, request_type):
        # if request_type in self.request_template.GrowRequestType.DESCRIPTOR.values_by_number\
        #         and request_type != self.request_template.GrowRequestType.Value('UNKNOWN'):
        self.request.type = request_type
        return self

    def options(self, options=None):
        if options:
            for options_item in options:
                new_options = self.request.options.add()
                for key, value in options_item.items():
                    new_options.key = key
                    new_options.value = value
        return self

    def data(self, data=None):
        if data:
            for data_item in data:
                new_data = self.request.data.add()
                for key, value in data_item.items():
                    new_data.key = key
                    new_data.value = value
                    new_data.type = value
        return self

    def build(self):
        return self.request



class RequestFactory(object):
    def __init__(self):
        self.request_builder = RequestBuilder()

    def system_monitor_request(self):
        return self.request_builder\
            .id("SYSTEM_MONITOR")\
            .timestamp()\
            .type(grow_proto.GrowRequestType.Value("SYSTEM_PARAMS__READ"))\
            .build()

    def tsl2591_request(self):
        return self.request_builder\
            .id("TSL2591")\
            .timestamp()\
            .type(grow_proto.GrowRequestType.Value("TSL2591__READ"))\
            .build()

    def dht22_request(self):
        return self.request_builder\
            .id("TSL2591")\
            .timestamp()\
            .type(grow_proto.GrowRequestType.Value("DHT22__READ"))\
            .build()

    def soil_moisture_sensor_request(self):
        return self.request_builder\
            .id("SOIL_MOISTURE_SENSOR")\
            .timestamp()\
            .type(grow_proto.GrowRequestType.Value("SOIL_MOISTURE_SENSOR__READ"))\
            .build()

    def simple_led_request(self, mode="OPERATOR", state="ON"):
        data = [
            {"mode": mode},
            {"state": state},
        ]
        return self.request_builder\
            .id("SIMPLE_LED")\
            .timestamp()\
            .type(grow_proto.GrowRequestType.Value("SIMPLE_LED__OPERATOR"))\
            .data(data)\
            .build()

    def tsl2591_subscription(self):
        return self.request_builder\
            .id("TSL2591_STREAM")\
            .timestamp()\
            .type(grow_proto.GrowRequestType.Value("TSL2591__STREAM_START"))\
            .build()


# if __name__ == '__main__':
#     request_builder = RequestBuilder()
#     request_factory = RequestFactory(request_builder)
#     request1 = request_factory.system_monitor_request()
#     request2 = request_factory.tsl2591_request()
#     print(request1,"\n",request2)

# enum GrowRequestType {
#   UNKNOWN = 0;
#   ALL__READ = 1;
#   SYSTEM_PARAMS__READ = 2;
#   DHT22__READ = 3;
#   SIMPLE_LED__OPERATOR = 4;
#   SIMPLE_LED__AUTO = 5;
#   TSL2591__READ = 6;
#   TSL2591__STREAM_START = 7;
#   TSL2591__STREAM_END = 8;
# }