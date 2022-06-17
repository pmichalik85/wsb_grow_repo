import datetime

import proto.grow_pb2 as proto


class ResponseBuilder(object):
    def __init__(self, request_proto):
        self.request_proto = request_proto;
        self.response_proto = proto.Response();

    def id(self, response_id):
        id_with_no_prefix = response_id.split(":")[1]
        self.response_proto.id = "response:" + id_with_no_prefix
        return self

    def timestamp(self):
        # self.response_proto.timestamp = case_id
        # self.response_proto.sub_case_id = sub_case_id
        return self

    def output_buffers(self):
        return self

    def build(self):
        self.response_proto.timestamp = str(datetime.datetime.utcnow().timestamp())
        return self.response_proto

# message Response {
#   optional string case_id = 1;
#   optional string sub_case_id = 2;
#   repeated PdfBuffer target_buffers = 3;
# }
# message PdfBuffer{
#   optional string name = 1;
#   repeated bytes buffer = 2;
# }
