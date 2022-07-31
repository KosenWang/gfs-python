
import sys

import grpc
import gfs_pb2 as pb2
import gfs_pb2_grpc as pb2_grpc
from concurrent import futures

class MasterServer(pb2_grpc.MasterServerServicer):

    def __init__(self) -> None:
        self.peer_table = {}
        self.chunk_table = {}
        self.name_space = {}


    def RegisterPeer(self, request, context):
        self.peer_table[request.id] = request.ip
        print(self.peer_table)
        return pb2.Empty()


    def CheckChunks(self, request, context):
        for peer in self.peer_table:
            with grpc.insecure_channel(self.peer_table[peer]) as channel:
                stub = pb2_grpc.ChunkServerStub(channel)
                reponse = stub.GetChunks(pb2.Empty())
                chunks = reponse.strs
            for chunk in chunks:
                if chunk in self.chunk_table:
                    value = self.chunk_table.get(chunk, set())
                    value.add(peer)
                else:
                    self.chunk_table[chunk] = {peer}
        print(self.chunk_table)
        return pb2.Empty()


    def NameSpace(self, request, context):
        self.name_space[request.name] = request.cid
        print(self.name_space)
        return pb2.Empty()


    def GetFile(self, request, context):
        filename = request.str
        chunks = self.name_space.get(filename, [])
        return pb2.StringList(strs=chunks)


    def GetPeers(self, request, context):
        peers = []
        for peer in self.peer_table:
            peers.append(self.peer_table[peer])
        return pb2.StringList(strs=peers)
        
    
    def FindLocation(self, request, context):
        cid = request.str
        locations = self.chunk_table.get(cid, set()) 
        peers = []
        for peer in locations:
            peers.append(self.peer_table[peer])
        return pb2.StringList(strs = peers)



def run():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    pb2_grpc.add_MasterServerServicer_to_server(MasterServer(), server)
    server.add_insecure_port('localhost:' + sys.argv[1])
    print("Master Server is Running")
    server.start()
    server.wait_for_termination()




if __name__ == "__main__":
    run()