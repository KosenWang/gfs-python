import os
import grpc
import gfs_pb2 as pb2
import gfs_pb2_grpc as pb2_grpc


def add_file():
    filename = "hello"
    peers = _get_peers()
    print(peers)
    data_dir = os.path.join('data', 'client', 'hello.txt')
    with open(data_dir, 'rb') as f:
        data = f.read()
    with grpc.insecure_channel(peers[0]) as channel:
        stub = pb2_grpc.ChunkServerStub(channel)
        response = stub.Add(pb2.AddRequest(name=filename, data=data, peers=peers[1:]))
    print("File added: " + response.str)


def read_file():
    filename = 'hello'
    chunks = _get_file(filename)
    data = bytes()
    for cid in chunks:
        peers = _get_location(cid)
        with grpc.insecure_channel(peers[0]) as channel:
            stub = pb2_grpc.ChunkServerStub(channel)
            chunk = stub.Read(pb2.ReadRequest(cid=cid))
            data += chunk.data
    print(data)


def _get_file(filename:str):
    with grpc.insecure_channel('localhost:8080') as channel:
        stub = pb2_grpc.MasterServerStub(channel)
        stub.CheckChunks(pb2.Empty())
        response = stub.GetFile(pb2.String(str=filename))
    return response.strs


def _get_location(cid:str):
    with grpc.insecure_channel('localhost:8080') as channel:
        stub = pb2_grpc.MasterServerStub(channel)
        stub.CheckChunks(pb2.Empty())
        response = stub.FindLocation(pb2.String(str=cid))
    return response.strs


def _get_peers():
    with grpc.insecure_channel('localhost:8080') as channel:
        stub = pb2_grpc.MasterServerStub(channel)
        stub.CheckChunks(pb2.Empty())
        response = stub.GetPeers(pb2.Empty())
    return response.strs


if __name__ == "__main__":
    # add_file()
    read_file()