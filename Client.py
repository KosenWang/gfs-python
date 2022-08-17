import os
import grpc
import gfs_pb2 as pb2
import gfs_pb2_grpc as pb2_grpc
import Config as conf

master_address = conf.MASTER_ADDRESS
chunk_size = conf.CHUNK_SIZE

def add_file(filename:str, k:int):
    dir = os.path.join('data', 'client', filename)
    with open(dir, 'rb') as f:
        data = f.read()
    size = len(data)
    peer_number = (size//chunk_size + 1) + k + 1
    peers = _get_peers(peer_number)
    with grpc.insecure_channel(peers[0]) as channel:
        stub = pb2_grpc.ChunkServerStub(channel)
        response = stub.Add(pb2.AddRequest(name=filename, data=data, peers=peers[1:], k=k))
    print(response.str)


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


def delete_file(uuid:str):
    with grpc.insecure_channel(master_address) as channel:
        stub = pb2_grpc.MasterServerStub(channel)
        stub.CheckChunks(pb2.Empty())
        response = stub.DeleteFile(pb2.String(str=uuid))
    print(response.str)


def _get_file(filename:str):
    # get the chunk arrays connected with the filename
    with grpc.insecure_channel('localhost:8080') as channel:
        stub = pb2_grpc.MasterServerStub(channel)
        stub.CheckChunks(pb2.Empty())
        response = stub.GetFile(pb2.String(str=filename))
    return response.map


def _get_peers(num:int):
    # get the ip address of peers which are ready for add file and backup
    with grpc.insecure_channel(master_address) as channel:
        stub = pb2_grpc.MasterServerStub(channel)
        stub.CheckChunks(pb2.Empty())
        response = stub.GetPeers(pb2.Number(num=num))
    return response.strs




if __name__ == "__main__":
    filename = "hello.txt"
    uuid = "317b3e3200601d09a306c2405b45246ace6fd623"
    add_file(filename, 1)
    # read_file(filename)
    delete_file(uuid)