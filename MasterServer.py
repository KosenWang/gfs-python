import time

import grpc
import Config as conf
import gfs_pb2 as pb2
import gfs_pb2_grpc as pb2_grpc
from Entity import Chunk, File
from concurrent import futures


localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
address = conf.MASTER_ADDRESS

chunk = Chunk()
file = File()

class MasterServer(pb2_grpc.MasterServerServicer):

    def __init__(self) -> None:
        self.peer_table = set()
        self.chunk_table = {}
        self.name_space = {}


    def RegisterPeer(self, request, context):
        ip_address = request.ip
        self.peer_table.add(ip_address)
        print(localtime, f"{ip_address} registered to master server.")
        print()
        print("--------------------Current Peer Table--------------------")
        print(self.peer_table)
        print("----------------------------------------------------------")
        print()
        return pb2.Empty()


    def CheckChunks(self, request, context):
        self.chunk_table = {}
        for peer in self.peer_table:
            with grpc.insecure_channel(peer) as channel:
                stub = pb2_grpc.ChunkServerStub(channel)
                reponse = stub.GetChunks(pb2.Empty())
                chunks = reponse.strs
            for cid in chunks:
                if cid in self.chunk_table:
                    chunk.set_location = self.chunk_table[cid]
                    chunk.add_location(peer)
                    self.chunk_table[cid] = chunk.get_location()
                else:
                    self.chunk_table[cid] = {peer}
        print(localtime, "Checked current chunk table.")
        print()
        print("--------------------Current Chunk Table--------------------")
        print(self.chunk_table)
        print("-----------------------------------------------------------")
        print()
        return pb2.Empty()


    def NameSpace(self, request, context):
        uuid = request.uuid
        chunks = request.list
        k = request.cft

        self.name_space[uuid] = (chunks, k)
        print(localtime, f"Added file {uuid} to name space.")
        print()
        print("--------------------Current Name Space--------------------")
        print(self.name_space)
        print("----------------------------------------------------------")
        print()
        return pb2.Empty()


    def GetFile(self, request, context):
        uuid = request.str

        chunks, cft = self.name_space.get(uuid, tuple())
        chunk_map = {}
        for cid in chunks:
            location = list(self.chunk_table.get(cid, set()))
            chunk_map[cid] = pb2.StringList(strs=location)
        return pb2.ChunkList(map=chunk_map, chunks=chunks, cft=cft)


    def DeleteFile(self, request, context):
        uuid = request.str
        chunks, cft = self.name_space.get(uuid, tuple())
        for cid in chunks:
            peers = self.chunk_table.get(cid, set())
            for peer in peers:
                with grpc.insecure_channel(peer) as channel:
                    stub = pb2_grpc.ChunkServerStub(channel)
                    stub.Delete(pb2.ChunkId(cid=cid))
            self.chunk_table.pop(cid, "Not found")
        self.name_space.pop(uuid, "Not found")

        print(localtime, f"Deleted file {uuid} from system.")
        print()
        print("--------------------Current Name Space--------------------")
        print(self.name_space)
        print("----------------------------------------------------------")
        print()
        print("-------------------Current Chunk Table--------------------")
        print(self.chunk_table)
        print("----------------------------------------------------------")
        print()

        msg = f'Deleted file {uuid}'
        return pb2.String(str=msg)


    def GetPeers(self, request, context):
        num = request.num
        peers = []
        count = 0
        for peer in self.peer_table:
            peers.append(peer)
            count += 1
            if count == num:
                break
        return pb2.StringList(strs=peers)




def run():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    pb2_grpc.add_MasterServerServicer_to_server(MasterServer(), server)
    server.add_insecure_port(address)
    print("Master Server is Running")
    server.start()
    server.wait_for_termination()




if __name__ == "__main__":
    run()