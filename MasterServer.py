
import sys
import time

import grpc
import gfs_pb2 as pb2
import gfs_pb2_grpc as pb2_grpc
from concurrent import futures


localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

class MasterServer(pb2_grpc.MasterServerServicer):

    def __init__(self) -> None:
        self.peer_table = {}
        self.chunk_table = {}
        self.name_space = {}


    def RegisterPeer(self, request, context):
        peer = request.id
        ip_address = request.ip
        self.peer_table[peer] = ip_address
        print(localtime, f"{peer} registered to master server.")
        print()
        print("--------------------Current Peer Table--------------------")
        print(self.peer_table)
        print("----------------------------------------------------------")
        print()
        return pb2.Empty()


    def CheckChunks(self, request, context):
        self.chunk_table = {}
        for peer in self.peer_table:
            with grpc.insecure_channel(self.peer_table[peer]) as channel:
                stub = pb2_grpc.ChunkServerStub(channel)
                reponse = stub.GetChunks(pb2.Empty())
                chunks = reponse.strs
            for chunk in chunks:
                if chunk in self.chunk_table:
                    value = self.chunk_table.get(chunk,set())
                    value.add(peer)
                else:
                    self.chunk_table[chunk] = {peer}
        print(localtime, "Checked current chunk table.")
        print()
        print("--------------------Current Chunk Table--------------------")
        print(self.chunk_table)
        print("-----------------------------------------------------------")
        print()
        return pb2.Empty()


    def NameSpace(self, request, context):
        filename = request.name
        chunks = request.cid
        self.name_space[filename] = chunks
        print(localtime, f"Added {filename} to name space.")
        print()
        print("--------------------Current Name Space--------------------")
        print(self.name_space)
        print("----------------------------------------------------------")
        print()
        return pb2.Empty()


    def GetFile(self, request, context):
        filename = request.str
        chunks = self.name_space.get(filename, [])
        return pb2.StringList(strs=chunks)


    def DeleteFile(self, request, context):
        filename = request.str
        chunks = self.name_space.get(filename, [])
        for cid in chunks:
            peers = self.get_location(cid)
            for peer in peers:
                with grpc.insecure_channel(peer) as channel:
                    stub = pb2_grpc.ChunkServerStub(channel)
                    stub.Delete(pb2.ChunkId(cid=cid))
            self.chunk_table.pop(cid)
        self.name_space.pop(filename)
        print(localtime, f"Deleted {filename} from system.")
        print()
        print("--------------------Current Name Space--------------------")
        print(self.name_space)
        print("----------------------------------------------------------")
        print()
        print("-------------------Current Chunk Table--------------------")
        print(self.chunk_table)
        print("----------------------------------------------------------")
        print()
        return pb2.Empty()


    def GetPeers(self, request, context):
        peers = []
        for peer in self.peer_table:
            peers.append(self.peer_table[peer])
        return pb2.StringList(strs=peers)
        
    
    def GetLocation(self, request, context):
        cid = request.str
        locations = self.chunk_table.get(cid, set()) 
        peers = []
        for peer in locations:
            peers.append(self.peer_table[peer])
        return pb2.StringList(strs = peers)

    
    def get_location(self, cid:str):
        locations = self.chunk_table.get(cid, set()) 
        peers = []
        for peer in locations:
            peers.append(self.peer_table[peer])
        return peers



def run():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    pb2_grpc.add_MasterServerServicer_to_server(MasterServer(), server)
    server.add_insecure_port('localhost:' + sys.argv[1])
    print("Master Server is Running")
    server.start()
    server.wait_for_termination()




if __name__ == "__main__":
    run()