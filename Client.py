import os
import zfec
import grpc
from Entity import Chunk
import gfs_pb2 as pb2
import gfs_pb2_grpc as pb2_grpc
import Config as conf

master_address = conf.MASTER_ADDRESS
chunk_size = conf.CHUNK_SIZE
path = os.path.join('data', 'client')

def add_file(filename:str, k:int):
    dir = os.path.join(path, filename)
    with open(dir, 'rb') as f:
        data = f.read()
    size = len(data)
    peer_number = (size//chunk_size + 1) + k + 1
    peers = _get_peers(peer_number)
    with grpc.insecure_channel(peers[0]) as channel:
        stub = pb2_grpc.ChunkServerStub(channel)
        response = stub.Add(pb2.AddRequest(name=filename, data=data, peers=peers[1:], k=k))
    print(response.str)


def read_file(uuid:str):
    chunks, mp, k = _get_file(uuid)
    data = bytes()
    chunk = Chunk()
    tmp = []
    # get data of each block
    for cid in chunks:
        peers = mp[cid].strs 
        with grpc.insecure_channel(peers[0]) as channel:
            stub = pb2_grpc.ChunkServerStub(channel)
            response = stub.Read(pb2.ChunkId(cid=cid))
            tmp.append(response.data)
    # verify consistency
    m = len(chunks)
    n = m - k
    index = []
    for i in range(m):
        index.append(i)
        if (chunk.set_cid(tmp[i]) != chunks[i]):
            del tmp[i]
            index.remove(i)
    # decode chunks
    try:
        if (len(tmp) == m):
            # all chunks are consistent
            blocks = zfec.Decoder(n, m).decode(tmp[:n], index[:n])
        else:
            # if <= k chunks are not consistent
            blocks = zfec.Decoder(n, m).decode(tmp, index)
        # combine data
        for block in blocks:
            data += block.rstrip(chr(0).encode())
        # write data    
        with open(os.path.join(path, uuid), 'wb') as f:
            f.write(data)
    except Exception:
        print(f'more than {k} chunks are not consistent.')
    

def delete_file(uuid:str):
    with grpc.insecure_channel(master_address) as channel:
        stub = pb2_grpc.MasterServerStub(channel)
        stub.CheckChunks(pb2.Empty())
        response = stub.DeleteFile(pb2.String(str=uuid))
    print(response.str)


def _get_file(uuid:str):
    # get the chunk arrays connected with the filename
    with grpc.insecure_channel(master_address) as channel:
        stub = pb2_grpc.MasterServerStub(channel)
        stub.CheckChunks(pb2.Empty())
        response = stub.GetFile(pb2.String(str=uuid))
    return (response.chunks, response.map, response.cft)


def _get_peers(num:int):
    # get the ip address of peers which are ready for add file and backup
    with grpc.insecure_channel(master_address) as channel:
        stub = pb2_grpc.MasterServerStub(channel)
        stub.CheckChunks(pb2.Empty())
        response = stub.GetPeers(pb2.Number(num=num))
    return response.strs




if __name__ == "__main__":
    filename = "test.txt"
    uuid = "97d170e1550eee4afc0af065b78cda302a97674c"
    add_file(filename, 1)
    read_file(uuid)
    delete_file(uuid)