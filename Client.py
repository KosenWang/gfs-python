import os
import grpc
import gfs_pb2 as pb2
import gfs_pb2_grpc as pb2_grpc


def add_file(filename:str):
    peers = _get_peers()
    data_dir = os.path.join('data', 'client', filename)
    with open(data_dir, 'rb') as f:
        data = f.read()
    with grpc.insecure_channel(peers[0]) as channel:
        stub = pb2_grpc.ChunkServerStub(channel)
        response = stub.Add(pb2.AddRequest(name=filename, data=data, peers=peers[1:]))
    print("File added: " + response.str)


def read_file(filename:str):
    chunks = _get_file(filename)
    print(chunks)
    data = bytes()
    for cid in chunks:
        peers = chunks[cid].strs 
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
    # get the chunk arrays connected with the filename
    with grpc.insecure_channel('localhost:8080') as channel:
        stub = pb2_grpc.MasterServerStub(channel)
        stub.CheckChunks(pb2.Empty())
        response = stub.GetFile(pb2.String(str=filename))
    return response.map


def _get_peers():
    # get the ip address of peers which are ready for add file and backup
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