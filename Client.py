import os
import grpc
import gfs_pb2 as pb2
import gfs_pb2_grpc as pb2_grpc


def add_file(filename:str):
    peers = _get_peers()
    data_dir = os.path.join('data', 'client', 'hello.txt')
    with open(data_dir, 'rb') as f:
        data = f.read()
    with grpc.insecure_channel(peers[0]) as channel:
        stub = pb2_grpc.ChunkServerStub(channel)
        response = stub.Add(pb2.AddRequest(name=filename, data=data, peers=peers[1:]))
    print("File added: " + response.str)


def read_file(filename:str):
    chunks = _get_file(filename)
    data = bytes()
    for cid in chunks:
        peers = _get_location(cid)
        with grpc.insecure_channel(peers[0]) as channel:
            stub = pb2_grpc.ChunkServerStub(channel)
            chunk = stub.Read(pb2.ChunkId(cid=cid))
            data += chunk.data
    print(data)


def delete_file(filename:str):
    with grpc.insecure_channel('localhost:8080') as channel:
        stub = pb2_grpc.MasterServerStub(channel)
        stub.DeleteFile(pb2.String(str=filename))
    print("Delete file: " + filename)


def _get_file(filename:str):
    with grpc.insecure_channel('localhost:8080') as channel:
        stub = pb2_grpc.MasterServerStub(channel)
        stub.CheckChunks(pb2.Empty())
        response = stub.GetFile(pb2.String(str=filename))
    return response.strs


def _get_location(cid:str):
    with grpc.insecure_channel('localhost:8080') as channel:
        stub = pb2_grpc.MasterServerStub(channel)
        response = stub.GetLocation(pb2.String(str=cid))
    return response.strs


def _get_peers():
    with grpc.insecure_channel('localhost:8080') as channel:
        stub = pb2_grpc.MasterServerStub(channel)
        stub.CheckChunks(pb2.Empty())
        response = stub.GetPeers(pb2.Empty())
    return response.strs




if __name__ == "__main__":
    filename = "hello.txt"
    add_file(filename)
    read_file(filename)
    delete_file(filename)