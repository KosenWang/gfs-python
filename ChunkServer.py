import os
import sys
import time
import hashlib

import grpc
import gfs_pb2 as pb2
import gfs_pb2_grpc as pb2_grpc
from concurrent import futures


PATH = os.path.join('data', sys.argv[2])
localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

class ChunkServer(pb2_grpc.ChunkServerServicer):
    
    def __init__(self) -> None:
        self.datastore = set()
        ls = os.listdir(PATH)
        for cid in ls:
            self.datastore.add(cid)
        print(localtime, "Synced datastore.")
        print()
        print("--------------------Current Datastore--------------------")
        print(self.datastore)
        print("---------------------------------------------------------")
        print()
        self.register_to_master()


    def Add(self, request, context):
        chunks = []
        consist = True
        data = request.data
        filename = request.name
        peers = request.peers
        size = len(data)//2 + 1

        while True:
            chunk = data[0: size]
            # is block empty
            if not chunk:
                break
            # calculate block_uuid
            cid = self.get_cid(chunk)
            # whether backup successfully
            consist &= self.backup(cid, chunk, peers)
            self.write(cid, chunk)
            chunks.append(cid)
            self.datastore.add(cid)
            data = data[size:]

        if consist:
            print(localtime, f"Added {filename} to datastore.")
            print()
            print("--------------------Current Datastore--------------------")
            print(self.datastore)
            print("---------------------------------------------------------")
            print()
            self.add_file_to_master(filename, chunks)
            return pb2.String(str=str({filename: chunks}))
        else:
            return pb2.String(str="Add file failed. Try again!")
        

    def Copy(self, request, context):
        status = False
        data = request.data
        cid = request.cid
        if cid == self.get_cid(data):
            self.write(cid, data)
            self.datastore.add(cid)
            print(localtime, f"Back up chunk {cid} successfully.")
            print()
            print("--------------------Current Datastore--------------------")
            print(self.datastore)
            print("---------------------------------------------------------")
            print()
            status = True
        return pb2.Bool(verify=status)


    def Read(self, request, context):
        with open(os.path.join(PATH, request.cid), 'rb') as f:
            data = f.read()
        return pb2.Bytes(data=data)
    

    def Delete(self, request, context):
        cid = request.cid
        data_dir = os.path.join(PATH, cid)
        os.remove(data_dir)
        self.datastore.remove(cid)
        print(localtime, f"Deleted chunk {cid} successfully.")
        print()
        print("--------------------Current Datastore--------------------")
        print(self.datastore)
        print("---------------------------------------------------------")
        print()
        return pb2.Empty()


    def GetChunks(self, request, context):
        chunks = []
        for chunk in self.datastore:
            chunks.append(chunk)
        return pb2.StringList(strs=chunks)


    def backup(self, cid:str, chunk:bytes, peers:list):
        status = True
        for i in range(len(peers)):
            with grpc.insecure_channel(peers[i]) as channel:
                stub = pb2_grpc.ChunkServerStub(channel)
                response = stub.Copy(pb2.CopyRequest(cid=cid, data=chunk))
                status &= response.verify
        return status


    def register_to_master(self):
        with grpc.insecure_channel('localhost:8080') as channel:
            stub = pb2_grpc.MasterServerStub(channel)
            stub.RegisterPeer(pb2.RegisterRequest(id=sys.argv[2], ip='localhost:' + sys.argv[1]))


    def add_file_to_master(self, filename:str, arr:list):
        with grpc.insecure_channel('localhost:8080') as channel:
            stub = pb2_grpc.MasterServerStub(channel)
            stub.NameSpace(pb2.NameRequest(name=filename, cid=arr))


    def get_cid(self, chunk:bytes):
        h = hashlib.sha1()
        h.update(chunk)
        return h.hexdigest()

    
    def write(self, cid:str, data:bytes):
        with open(os.path.join(PATH, cid), 'wb') as f:
            f.write(data)



def run():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    pb2_grpc.add_ChunkServerServicer_to_server(ChunkServer(), server)
    server.add_insecure_port('localhost:' + sys.argv[1])
    print("Chunk Server is Running")
    server.start()
    server.wait_for_termination()




if __name__ == "__main__":
    run()