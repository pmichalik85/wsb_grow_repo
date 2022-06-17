import random
import uuid
import datetime


class RequestBuilder(object):
    def __init__(self, request_template):
        self.request = None
        self.init_timestamp = None
        self.request_template = request_template

    def _new(self):
        self.request = self.request_template
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
        if request_type in type(self.request_template).GrowRequestType.DESCRIPTOR.values_by_number\
                and request_type != type(self.request_template).GrowRequestType.Value('UNKNOWN'):
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
        return self

    def build(self):
        return self.request


