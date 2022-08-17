import time
import os
import hashlib

import grpc
import gfs_pb2 as pb2
import gfs_pb2_grpc as pb2_grpc


class Chunk():
    def __init__(self) -> None:
        self.cid = ""
        self.location = set()
        self.ttl = time.time()

    def __call__(self, cid:str, address:str) -> None:
        self.cid = cid
        self.location = {address}
    
    def save(self, data:bytes, dir:str) -> None:
        with open(os.path.join(dir, self.cid), 'wb') as f:
            f.write(data)

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

    def get_location(self):
        return self.location

    def get_cid(self):
        return self.cid

    def set_cid(self, block:bytes):
        h = hashlib.sha1()
        h.update(block)
        self.cid = h.hexdigest()

    def __str__(self) -> str:
        return "cid: %s, location: %s" %(self.cid, self.location)


class File():
    def __init__(self) -> None:
        self.filename = ""
        self.uuid = ""
        self.chunks = []
        self.ttl = time.time()

    def __str__(self) -> str:
        return "file: %s, uuid: %s, chunks: %s" %(self.filename, self.uuid, self.chunks)

    def __call__(self, filename:str, uuid:str, chunks:list) -> None:
        self.filename = filename
        self.uuid = uuid
        self.chunks = chunks

    def set_filename(self, filename:str):
        self.filename = filename

    def set_uuid(self, data:bytes):
        # need to be hash of chunks
        h = hashlib.sha1()
        h.update(data)
        self.uuid = h.hexdigest()
        return self.uuid
    
    def get_uuid(self):
        return self.uuid

    def get_chunks(self):
        return self.chunks

    def add_chunk(self, cid:str):
        self.chunks.append(cid)

    def add_to_master(self, master_address:str):
        with grpc.insecure_channel(master_address) as channel:
            stub = pb2_grpc.MasterServerStub(channel)
            stub.NameSpace(pb2.NameRequest(name=self.filename, uuid=self.uuid, list=self.chunks))