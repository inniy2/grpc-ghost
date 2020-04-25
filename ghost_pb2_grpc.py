# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import ghost_pb2 as ghost__pb2


class ghostStub(object):
    """Missing associated documentation comment in .proto file"""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.diskcheck = channel.unary_unary(
                '/ghost/diskcheck',
                request_serializer=ghost__pb2.diskRequest.SerializeToString,
                response_deserializer=ghost__pb2.APIResponse.FromString,
                )
        self.checkdefinition = channel.unary_unary(
                '/ghost/checkdefinition',
                request_serializer=ghost__pb2.definitionRequest.SerializeToString,
                response_deserializer=ghost__pb2.APIResponse.FromString,
                )
        self.cutover = channel.unary_unary(
                '/ghost/cutover',
                request_serializer=ghost__pb2.Empty.SerializeToString,
                response_deserializer=ghost__pb2.APIResponse.FromString,
                )
        self.dryrun = channel.unary_unary(
                '/ghost/dryrun',
                request_serializer=ghost__pb2.ghostRequest.SerializeToString,
                response_deserializer=ghost__pb2.APIResponse.FromString,
                )
        self.execute = channel.unary_stream(
                '/ghost/execute',
                request_serializer=ghost__pb2.ghostRequest.SerializeToString,
                response_deserializer=ghost__pb2.APIMessage.FromString,
                )
        self.executeNohup = channel.unary_unary(
                '/ghost/executeNohup',
                request_serializer=ghost__pb2.ghostRequest.SerializeToString,
                response_deserializer=ghost__pb2.APIResponse.FromString,
                )
        self.interactive = channel.unary_unary(
                '/ghost/interactive',
                request_serializer=ghost__pb2.interactiveRequest.SerializeToString,
                response_deserializer=ghost__pb2.APIResponse.FromString,
                )


class ghostServicer(object):
    """Missing associated documentation comment in .proto file"""

    def diskcheck(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def checkdefinition(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def cutover(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def dryrun(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def execute(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def executeNohup(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def interactive(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ghostServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'diskcheck': grpc.unary_unary_rpc_method_handler(
                    servicer.diskcheck,
                    request_deserializer=ghost__pb2.diskRequest.FromString,
                    response_serializer=ghost__pb2.APIResponse.SerializeToString,
            ),
            'checkdefinition': grpc.unary_unary_rpc_method_handler(
                    servicer.checkdefinition,
                    request_deserializer=ghost__pb2.definitionRequest.FromString,
                    response_serializer=ghost__pb2.APIResponse.SerializeToString,
            ),
            'cutover': grpc.unary_unary_rpc_method_handler(
                    servicer.cutover,
                    request_deserializer=ghost__pb2.Empty.FromString,
                    response_serializer=ghost__pb2.APIResponse.SerializeToString,
            ),
            'dryrun': grpc.unary_unary_rpc_method_handler(
                    servicer.dryrun,
                    request_deserializer=ghost__pb2.ghostRequest.FromString,
                    response_serializer=ghost__pb2.APIResponse.SerializeToString,
            ),
            'execute': grpc.unary_stream_rpc_method_handler(
                    servicer.execute,
                    request_deserializer=ghost__pb2.ghostRequest.FromString,
                    response_serializer=ghost__pb2.APIMessage.SerializeToString,
            ),
            'executeNohup': grpc.unary_unary_rpc_method_handler(
                    servicer.executeNohup,
                    request_deserializer=ghost__pb2.ghostRequest.FromString,
                    response_serializer=ghost__pb2.APIResponse.SerializeToString,
            ),
            'interactive': grpc.unary_unary_rpc_method_handler(
                    servicer.interactive,
                    request_deserializer=ghost__pb2.interactiveRequest.FromString,
                    response_serializer=ghost__pb2.APIResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'ghost', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ghost(object):
    """Missing associated documentation comment in .proto file"""

    @staticmethod
    def diskcheck(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ghost/diskcheck',
            ghost__pb2.diskRequest.SerializeToString,
            ghost__pb2.APIResponse.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def checkdefinition(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ghost/checkdefinition',
            ghost__pb2.definitionRequest.SerializeToString,
            ghost__pb2.APIResponse.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def cutover(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ghost/cutover',
            ghost__pb2.Empty.SerializeToString,
            ghost__pb2.APIResponse.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def dryrun(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ghost/dryrun',
            ghost__pb2.ghostRequest.SerializeToString,
            ghost__pb2.APIResponse.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def execute(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/ghost/execute',
            ghost__pb2.ghostRequest.SerializeToString,
            ghost__pb2.APIMessage.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def executeNohup(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ghost/executeNohup',
            ghost__pb2.ghostRequest.SerializeToString,
            ghost__pb2.APIResponse.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def interactive(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ghost/interactive',
            ghost__pb2.interactiveRequest.SerializeToString,
            ghost__pb2.APIResponse.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)
