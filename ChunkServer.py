import os
import sys
import time
import zfec

import grpc
import gfs_pb2 as pb2
import gfs_pb2_grpc as pb2_grpc
from Entity import Chunk, File
import Config as conf
from concurrent import futures



PATH = os.path.join('data', sys.argv[2])
ADDRESS = 'localhost:' + sys.argv[1]

master_address = conf.MASTER_ADDRESS
chunk_size = conf.CHUNK_SIZE
localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

class ChunkServer(pb2_grpc.ChunkServerServicer):
    
    def __init__(self) -> None:
        self.datastore = {}
        self.cache = {}

        ls = os.listdir(PATH)
        for cid in ls:
            chunk = Chunk()
            chunk(cid, ADDRESS)
            self.datastore[cid] = chunk
        print(localtime, "Synced datastore.")
        print()
        print("--------------------Current Datastore--------------------")
        self.print_datastore()
        print("---------------------------------------------------------")
        print()
        self.register_to_master()


    def Add(self, request, context):
        data = request.data
        name = request.name
        peers = request.peers
        k = request.k

        consist = True
        file = File() 
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
        
        chunk = Chunk()
        # first commit
        for i in range(n+k):
            cid = chunk.set_cid(blocks[i])
            file.add_chunk(cid)
            # whether backup successfully
            consist &= chunk.backup(cid, blocks[i], peers[i])
        
        
        # second commit
        file.set_filename(name)
        file.set_cft(k)
        uuid = file.set_uuid()
        chunks = file.get_chunks()
        msg = ""
        if consist:
            for i in range(n+k):
                chunk.confirm(chunks[i], True, peers[i])
            file.add_to_master(master_address)
            msg = f"Added {name} {uuid}"
        else:
            for i in range(n+k):
                chunk.confirm(chunks[i], False, peers[i])
            msg = f"Add {name} failed. Try again!"
        
        return pb2.String(str=msg)
        

    def FirstCommit(self, request, context):
        data = request.data
        cid = request.cid

        status = False
        chunk = Chunk()
        chunk.set_cid(data)
        if cid == chunk.get_cid():
            self.cache[cid] = data
            print(localtime, f"added chunk {cid} to cache.")
            print()
            print("--------------------Current Cache--------------------")
            print(self.cache)
            print("---------------------------------------------------------")
            print()
            status = True
        return pb2.Bool(verify=status)


    def SecondCommit(self, request, context):
        cid = request.cid
        verify = request.verify

        if verify:
            chunk = Chunk()
            chunk(cid, ADDRESS)
            chunk.save(self.cache[cid], PATH)
            self.datastore[cid] = chunk
            print(localtime, f"added chunk {cid} to datastore.")
            print()
            print("--------------------Current Datastore--------------------")
            self.print_datastore()
            print("---------------------------------------------------------")
            print()
            self.cache.pop(cid, "Not found")
        else:
            self.cache.pop(cid, "Not found")

        print(localtime, f"removed chunk {cid} from cache.")
        print()
        print("--------------------Current Cache--------------------")
        print(self.cache)
        print("---------------------------------------------------------")
        print()
        return pb2.Empty()


    def Read(self, request, context):
        with open(os.path.join(PATH, request.cid), 'rb') as f:
            data = f.read()
        return pb2.Bytes(data=data)
    

    def Delete(self, request, context):
        cid = request.cid
        data_dir = os.path.join(PATH, cid)
        os.remove(data_dir)
        self.datastore.pop(cid, "Not found")
        print(localtime, f"Deleted chunk {cid} from datastore.")
        print()
        print("--------------------Current Datastore--------------------")
        self.print_datastore()
        print("---------------------------------------------------------")
        print()
        return pb2.Empty()


    def GetChunks(self, request, context):
        chunks = []
        for cid in self.datastore:
            chunk = self.datastore.get(cid, Chunk())
            chunks.append(chunk.get_cid())
        return pb2.StringList(strs=chunks)


    def backup(self, cid:str, block:bytes, peers:list):
        status = True
        for i in range(len(peers)):
            with grpc.insecure_channel(peers[i]) as channel:
                stub = pb2_grpc.ChunkServerStub(channel)
                response = stub.Copy(pb2.CopyRequest(cid=cid, data=block))
                status &= response.verify
        return status


    def register_to_master(self):
        with grpc.insecure_channel(master_address) as channel:
            stub = pb2_grpc.MasterServerStub(channel)
            stub.RegisterPeer(pb2.RegisterRequest(ip=ADDRESS))


    def print_datastore(self):
        for cid in self.datastore:
            print(self.datastore[cid])


def run():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    pb2_grpc.add_ChunkServerServicer_to_server(ChunkServer(), server)
    server.add_insecure_port(ADDRESS)
    print("Chunk Server is Running")
    server.start()
    server.wait_for_termination()




if __name__ == "__main__":
    run()