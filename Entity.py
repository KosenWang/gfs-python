import time
import os
import hashlib

import grpc
import gfs_pb2 as pb2
import gfs_pb2_grpc as pb2_grpc
import Config as conf

master_address = conf.MASTER_ADDRESS

class Chunk():
    def __init__(self) -> None:
        self.cid = ""
        self.location = set()
        self.ttl = time.time()
    
    def save(self, cid:str, path:str, data:bytes) -> None:
        dir = os.path.join(path, cid)
        with open(dir, 'wb') as f:
            data = f.write(data)

    def backup(self, cid:str, data:bytes, address:str):
        with grpc.insecure_channel(address) as channel:
            stub = pb2_grpc.ChunkServerStub(channel)
            response = stub.FirstCommit(pb2.CopyRequest(cid=cid, data=data))
        return response.verify

    def confirm(self, cid:str, verify:bool, address:str):
        with grpc.insecure_channel(address) as channel:
            stub = pb2_grpc.ChunkServerStub(channel)
            stub.SecondCommit(pb2.ConfirmRequest(cid=cid, verify=verify))

    def add_location(self, new_address:str):
        self.location.add(new_address)

    def get_location(self) -> set: 
        return self.location

    def set_location(self, location:set):
        self.location = location

    def get_cid(self):
        return self.cid

    def set_cid(self, block:bytes):
        h = hashlib.sha1()
        h.update(block)
        self.cid = h.hexdigest()
        return self.cid
        
    def __str__(self) -> str:
        return "cid: %s, location: %s" %(self.cid, self.location)


class File():
    def __init__(self) -> None:
        self.uuid = ""
        self.chunks = []
        self.cft = 0 # Crash Fault Tolerance
        self.ttl = time.time()

    def set_cft(self, k:int):
        self.cft = k

    def get_cft(self):
        return self.cft

    def set_uuid(self):
        tmp = str(self.chunks)
        h = hashlib.sha1()
        h.update(tmp.encode('utf-8'))
        self.uuid = h.hexdigest()
        return self.uuid
    
    def get_uuid(self):
        return self.uuid

    def get_chunks(self):
        return self.chunks

    def add_chunk(self, cid:str):
        self.chunks.append(cid)

    def get_file(self, uuid:str):
        # get the chunk arrays connected with the filename
        with grpc.insecure_channel(master_address) as channel:
            stub = pb2_grpc.MasterServerStub(channel)
            stub.CheckChunks(pb2.Empty())
            response = stub.GetFile(pb2.String(str=uuid))
        return (response.chunks, response.map, response.cft)

    def get_peers(self, num:int):
        # get the ip address of peers which are ready for add file and backup
        with grpc.insecure_channel(master_address) as channel:
            stub = pb2_grpc.MasterServerStub(channel)
            stub.CheckChunks(pb2.Empty())
            response = stub.GetPeers(pb2.Number(num=num))
        return response.strs

    def read(self, filename:str, path:str):
        dir = os.path.join(path, filename)
        with open(dir, 'rb') as f:
            data = f.read()
        return data

    def write(self, uuid:str, path:str, data:bytes):
        dir = os.path.join(path, uuid)
        with open(dir, 'wb') as f:
            data = f.write(data)

    def add_to_master(self):
        with grpc.insecure_channel(master_address) as channel:
            stub = pb2_grpc.MasterServerStub(channel)
            stub.NameSpace(pb2.NameRequest(uuid=self.uuid, list=self.chunks, cft=self.cft))
    
    def __str__(self) -> str:
        return "uuid: %s, chunks: %s, cft: %s" %(self.uuid, self.chunks, self.cft)