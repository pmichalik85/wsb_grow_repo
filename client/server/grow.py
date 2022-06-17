from concurrent import futures
import grpc
import grow_lib as grow
import proto.grow_pb2_grpc as grpc_proto



def serve():
    print("Starting serve function")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    grpc_proto.add_GrowServiceServicer_to_server(grow.GrowService(), server)
    # SERVICE_NAMES = (
    #     proto.DESCRIPTOR.services_by_name['PDFFormService'].full_name,
    #     reflection.SERVICE_NAME,
    # )
    # reflection.enable_server_reflection(SERVICE_NAMES, server)
    # health_pb2_grpc.add_HealthServicer_to_server(
    #     health.HealthServicer(), server)
    # # Add Channelz Servicer to the gRPC server
    # channelz.add_channelz_servicer(server)
    server.add_insecure_port('[::]:50051')

    server.start()
    server.wait_for_termination()


# def main():
#     print("Starting server main run")
#     serve()

#
#
# # Press the green button in the gutter to run the script.
if __name__ == '__main__':
    serve()

#
# # See PyCharm help at https://www.jetbrains.com/help/pycharm/
