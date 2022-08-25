# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import gfs_pb2 as gfs__pb2


class ChunkServerStub(object):
    """The chunk server
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Read = channel.unary_unary(
                '/gfs.ChunkServer/Read',
                request_serializer=gfs__pb2.ChunkId.SerializeToString,
                response_deserializer=gfs__pb2.Bytes.FromString,
                )
        self.FirstCommit = channel.unary_unary(
                '/gfs.ChunkServer/FirstCommit',
                request_serializer=gfs__pb2.CopyRequest.SerializeToString,
                response_deserializer=gfs__pb2.Bool.FromString,
                )
        self.SecondCommit = channel.unary_unary(
                '/gfs.ChunkServer/SecondCommit',
                request_serializer=gfs__pb2.ConfirmRequest.SerializeToString,
                response_deserializer=gfs__pb2.Empty.FromString,
                )
        self.Delete = channel.unary_unary(
                '/gfs.ChunkServer/Delete',
                request_serializer=gfs__pb2.ChunkId.SerializeToString,
                response_deserializer=gfs__pb2.Empty.FromString,
                )
        self.GetChunks = channel.unary_unary(
                '/gfs.ChunkServer/GetChunks',
                request_serializer=gfs__pb2.Empty.SerializeToString,
                response_deserializer=gfs__pb2.StringList.FromString,
                )


class ChunkServerServicer(object):
    """The chunk server
    """

    def Read(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def FirstCommit(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SecondCommit(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Delete(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetChunks(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ChunkServerServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Read': grpc.unary_unary_rpc_method_handler(
                    servicer.Read,
                    request_deserializer=gfs__pb2.ChunkId.FromString,
                    response_serializer=gfs__pb2.Bytes.SerializeToString,
            ),
            'FirstCommit': grpc.unary_unary_rpc_method_handler(
                    servicer.FirstCommit,
                    request_deserializer=gfs__pb2.CopyRequest.FromString,
                    response_serializer=gfs__pb2.Bool.SerializeToString,
            ),
            'SecondCommit': grpc.unary_unary_rpc_method_handler(
                    servicer.SecondCommit,
                    request_deserializer=gfs__pb2.ConfirmRequest.FromString,
                    response_serializer=gfs__pb2.Empty.SerializeToString,
            ),
            'Delete': grpc.unary_unary_rpc_method_handler(
                    servicer.Delete,
                    request_deserializer=gfs__pb2.ChunkId.FromString,
                    response_serializer=gfs__pb2.Empty.SerializeToString,
            ),
            'GetChunks': grpc.unary_unary_rpc_method_handler(
                    servicer.GetChunks,
                    request_deserializer=gfs__pb2.Empty.FromString,
                    response_serializer=gfs__pb2.StringList.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'gfs.ChunkServer', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ChunkServer(object):
    """The chunk server
    """

    @staticmethod
    def Read(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/gfs.ChunkServer/Read',
            gfs__pb2.ChunkId.SerializeToString,
            gfs__pb2.Bytes.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def FirstCommit(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/gfs.ChunkServer/FirstCommit',
            gfs__pb2.CopyRequest.SerializeToString,
            gfs__pb2.Bool.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SecondCommit(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/gfs.ChunkServer/SecondCommit',
            gfs__pb2.ConfirmRequest.SerializeToString,
            gfs__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Delete(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/gfs.ChunkServer/Delete',
            gfs__pb2.ChunkId.SerializeToString,
            gfs__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetChunks(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/gfs.ChunkServer/GetChunks',
            gfs__pb2.Empty.SerializeToString,
            gfs__pb2.StringList.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)


class MasterServerStub(object):
    """master server
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.RegisterPeer = channel.unary_unary(
                '/gfs.MasterServer/RegisterPeer',
                request_serializer=gfs__pb2.RegisterRequest.SerializeToString,
                response_deserializer=gfs__pb2.Empty.FromString,
                )
        self.CheckChunks = channel.unary_unary(
                '/gfs.MasterServer/CheckChunks',
                request_serializer=gfs__pb2.Empty.SerializeToString,
                response_deserializer=gfs__pb2.Empty.FromString,
                )
        self.GetFile = channel.unary_unary(
                '/gfs.MasterServer/GetFile',
                request_serializer=gfs__pb2.String.SerializeToString,
                response_deserializer=gfs__pb2.ChunkList.FromString,
                )
        self.DeleteFile = channel.unary_unary(
                '/gfs.MasterServer/DeleteFile',
                request_serializer=gfs__pb2.String.SerializeToString,
                response_deserializer=gfs__pb2.String.FromString,
                )
        self.GetPeers = channel.unary_unary(
                '/gfs.MasterServer/GetPeers',
                request_serializer=gfs__pb2.Number.SerializeToString,
                response_deserializer=gfs__pb2.StringList.FromString,
                )
        self.NameSpace = channel.unary_unary(
                '/gfs.MasterServer/NameSpace',
                request_serializer=gfs__pb2.NameRequest.SerializeToString,
                response_deserializer=gfs__pb2.Empty.FromString,
                )


class MasterServerServicer(object):
    """master server
    """

    def RegisterPeer(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CheckChunks(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetFile(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteFile(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetPeers(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def NameSpace(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_MasterServerServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'RegisterPeer': grpc.unary_unary_rpc_method_handler(
                    servicer.RegisterPeer,
                    request_deserializer=gfs__pb2.RegisterRequest.FromString,
                    response_serializer=gfs__pb2.Empty.SerializeToString,
            ),
            'CheckChunks': grpc.unary_unary_rpc_method_handler(
                    servicer.CheckChunks,
                    request_deserializer=gfs__pb2.Empty.FromString,
                    response_serializer=gfs__pb2.Empty.SerializeToString,
            ),
            'GetFile': grpc.unary_unary_rpc_method_handler(
                    servicer.GetFile,
                    request_deserializer=gfs__pb2.String.FromString,
                    response_serializer=gfs__pb2.ChunkList.SerializeToString,
            ),
            'DeleteFile': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteFile,
                    request_deserializer=gfs__pb2.String.FromString,
                    response_serializer=gfs__pb2.String.SerializeToString,
            ),
            'GetPeers': grpc.unary_unary_rpc_method_handler(
                    servicer.GetPeers,
                    request_deserializer=gfs__pb2.Number.FromString,
                    response_serializer=gfs__pb2.StringList.SerializeToString,
            ),
            'NameSpace': grpc.unary_unary_rpc_method_handler(
                    servicer.NameSpace,
                    request_deserializer=gfs__pb2.NameRequest.FromString,
                    response_serializer=gfs__pb2.Empty.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'gfs.MasterServer', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class MasterServer(object):
    """master server
    """

    @staticmethod
    def RegisterPeer(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/gfs.MasterServer/RegisterPeer',
            gfs__pb2.RegisterRequest.SerializeToString,
            gfs__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CheckChunks(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/gfs.MasterServer/CheckChunks',
            gfs__pb2.Empty.SerializeToString,
            gfs__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetFile(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/gfs.MasterServer/GetFile',
            gfs__pb2.String.SerializeToString,
            gfs__pb2.ChunkList.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DeleteFile(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/gfs.MasterServer/DeleteFile',
            gfs__pb2.String.SerializeToString,
            gfs__pb2.String.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetPeers(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/gfs.MasterServer/GetPeers',
            gfs__pb2.Number.SerializeToString,
            gfs__pb2.StringList.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def NameSpace(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/gfs.MasterServer/NameSpace',
            gfs__pb2.NameRequest.SerializeToString,
            gfs__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
