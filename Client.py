import os
import zfec
import grpc

from Entity import Chunk, File
import gfs_pb2 as pb2
import gfs_pb2_grpc as pb2_grpc
import Config as conf

master_address = conf.MASTER_ADDRESS
chunk_size = conf.CHUNK_SIZE
path = os.path.join('data', 'client')
file = File() 
chunk = Chunk()

def add_file(name:str, k:int):
    data = file.read(name, path)
    size = len(data)
    peer_number = (size//chunk_size + 1) + k
    peers = file.get_peers(peer_number)
    consist = True
    tmp = [] # store data of each block, wait for ec alogrithm
    # divide origin data
    while True:
        block = data[0: chunk_size]
        # is block empty
        if not block:
            break
        block = bytes(block).ljust(chunk_size, b'\x01')
        tmp.append(block)
        data = data[chunk_size:]
    
    n = len(tmp) # number of origin blocks
    blocks = zfec.Encoder(n, n + k).encode(tmp)

    # first commit
    for i in range(n+k):
        cid = chunk.set_cid(blocks[i])
        file.add_chunk(cid)
        # whether backup successfully
        consist &= chunk.backup(cid, blocks[i], peers[i])    
    
    # second commit
    file.set_cft(k)
    uuid = file.set_uuid()
    chunks = file.get_chunks()
    if consist:
        for i in range(n+k):
            chunk.confirm(chunks[i], True, peers[i])
        file.add_to_master()
        msg = f"Added {name} {uuid}"
    else:
        for i in range(n+k):
            chunk.confirm(chunks[i], False, peers[i])
        msg = f"Add {name} failed. Try again!"
    print(msg)


def read_file(uuid:str):
    chunks, mp, k = file.get_file(uuid)
    data = bytes()
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
            data += block.rstrip(b'\x01')
        # write data    
        file.write(uuid, path, data)
    except Exception:
        print(f'more than {k} chunks are not consistent.')
    

def delete_file(uuid:str):
    with grpc.insecure_channel(master_address) as channel:
        stub = pb2_grpc.MasterServerStub(channel)
        stub.CheckChunks(pb2.Empty())
        response = stub.DeleteFile(pb2.String(str=uuid))
    print(response.str)




if __name__ == "__main__":
    filename = "test.txt"
    uuid = "f4fd33e24bdb265b9c90479a92fcb2e0e26b7b52"
    add_file(filename, 1)
    read_file(uuid)
    delete_file(uuid)