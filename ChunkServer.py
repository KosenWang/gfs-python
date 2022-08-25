import os
import sys
import time

import grpc
import gfs_pb2 as pb2
import gfs_pb2_grpc as pb2_grpc
from Entity import Chunk
import Config as conf
from concurrent import futures



path = os.path.join('data', sys.argv[2])
address = 'localhost:' + sys.argv[1]

master_address = conf.MASTER_ADDRESS
chunk_size = conf.CHUNK_SIZE
localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
chunk = Chunk()

class ChunkServer(pb2_grpc.ChunkServerServicer):
    
    def __init__(self) -> None:
        self.datastore = set()
        self.cache = {}

        ls = os.listdir(path)
        for cid in ls:
            self.datastore.add(cid)
        print(localtime, "Synced datastore.")
        print()
        print("--------------------Current Datastore--------------------")
        print(self.datastore)
        print("---------------------------------------------------------")
        print()
        self.register_to_master()


    def FirstCommit(self, request, context):
        data = request.data
        cid = request.cid

        status = False
        if cid == chunk.set_cid(data):
            self.cache[cid] = data
            print(localtime, f"added chunk {cid} to cache.")
            print()
            print("--------------------Current Cache--------------------")
            print(self.cache)
            print("-----------------------------------------------------")
            print()
            status = True
        return pb2.Bool(verify=status)


    def SecondCommit(self, request, context):
        cid = request.cid
        verify = request.verify

        if verify:
            chunk.save(cid, path, self.cache[cid])
            self.datastore.add(cid)
            print(localtime, f"added chunk {cid} to datastore.")
            print()
            print("--------------------Current Datastore--------------------")
            print(self.datastore)
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
        with open(os.path.join(path, request.cid), 'rb') as f:
            data = f.read()
        return pb2.Bytes(data=data)
    

    def Delete(self, request, context):
        cid = request.cid
        data_dir = os.path.join(path, cid)
        os.remove(data_dir)
        self.datastore.remove(cid)
        print(localtime, f"Deleted chunk {cid} from datastore.")
        print()
        print("--------------------Current Datastore--------------------")
        print(self.datastore)
        print("---------------------------------------------------------")
        print()
        return pb2.Empty()


    def GetChunks(self, request, context):
        chunks = []
        for cid in self.datastore:
            chunks.append(cid)
        return pb2.StringList(strs=chunks)


    def register_to_master(self):
        with grpc.insecure_channel(master_address) as channel:
            stub = pb2_grpc.MasterServerStub(channel)
            stub.RegisterPeer(pb2.RegisterRequest(ip=address))




def run():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    pb2_grpc.add_ChunkServerServicer_to_server(ChunkServer(), server)
    server.add_insecure_port(address)
    print("Chunk Server is Running")
    server.start()
    server.wait_for_termination()




if __name__ == "__main__":
    run()