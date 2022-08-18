# gfs-python-implementation
This project is a prototype of google file system. The whole system is based on the concept of GFS. There is one single master-server for metadata control and serveral chunk-server for real data storing.

## Introduction
### Master Server
There are totally 3 tables in master-server. The first table called peer_table which is the mapping of peer's ID and peer's ip address. When one peer first registers to the master-server, these information will be stored in this table. The second table called chunk_table is the mapping of chunk's ID and the list of peers' ID where the chunk is stored. Master-server will regularly check the chunklist in each peer through some heartbeat mechanism(currently not available) and before each write/read/delete operation. The third table called name_space which is the mapping of filename and chunk array connected with this file. This table will be updated after each write/delete operation.

### Chunk Server
Chunk-server is where the data is stored. There is one list called datastore in each chunk-server which stores all the chunk's ID in this server. Also, the data flow will only happen between client and each chunk-server.

## Functionality
### Add File
When client wants to add one file to the system, first it will request the master-server to get the candidate peers' ip address. It will choose one randomly as the primary chunk-server(in GFS thesis it should be the closest one to the client's ip address) and others as secondary chunk-server. Client connects with primary chunk-server and upload data to it. For simplifying prototype, the whole data will be divided into 2 chunks rather than fixed chunk size of 64 MB as in GFS. Then each chunk will have a unique hash value based on the content as chunk ID. The primary chunk-server will backup each chunk into each secondary chunk-server. When secondary chunk-server get the cid and data, it will calculate first the data's hash is equal to cid. Only when yes it will write the chunk in local datastore. When each chunk-server write successfully, the primary chunk-server will send the file name and chunk array to master-server to update name_space.

### Read File
When client wants to read a file in system, first it will ask the master-server about the filename. Master-server will search in name_space, find the related chunk array and return to client. Then client will recursively ask master-server again about the peer ip of each chunk. Then client will choose randomly one peer to get the chunk.

### Delete File
When client wants to delete a file in system, it only needs to send the file name to the master-server. Master will check all belonging chunks and where they are stored. It will ask each peer to delete the local chunk and update the name_space and chunk_table.

## Current Config
chunk_size = 128 kB

## Example
Clone git repository:

`git clone https://github.com/KosenWang/gfs-python.git`

Open folder:

`cd gfs-python`

Run master-server:

`python MasterServer.py`

Open other 4 terminals and run 3 chunk-servers：

`python ChunkServer.py 8081 peer1`

`python ChunkServer.py 8082 peer2`

`python ChunkServer.py 8083 peer3`

`python ChunkServer.py 8084 peer4`

Open another terminal and run client:

`python Client.py`

Then the log in each terminal will show detailed process of each operation. You can change the chunk size in Config.py. But make sure the number of chunk servers is >= (file_size//chunk_size + 1) + k + 1

## TODO
1. heartbeat mechanism
2. multithreading
