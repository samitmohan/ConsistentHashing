# ConsistentHashing
CH in python (basics)

Good Article : https://medium.com/@animeshblog/consistent-hashing-d23379273ade

A good hash function has the following properties:
    The function is computationally efficient and the values generated are easy for lookups
    The function, for most general use cases, behaves like a pseudorandom generator that spreads data out evenly without any noticeable correlation

1. Building storage system
    Building system in which users can upload and access files -> APIs : upload, fetch
    BTS storage has storage_nodes on which files are stored/accessed : 2 functions -> put_file, fetch_file
        puts/gets file to/from disk and sends response to main API which sends it to user.
    Avoid overwhelming of load : multiple storage_nodes (store files in distributed way)

    upload API with path of file as input -> system identifies storage_node responsible for storing this file
        How to? apply hash function to path and get storage_node index, once we get storage node we can read contents of
            file and put that file on node by invoking put_file function
---
Why Consistent Hashing?
Say we have 5 files ‘f1.txt’, ‘f2.txt’, ‘f3.txt’, ‘f4.txt’, ‘f5.txt’ if we apply the hash function to these we find that
   they are stored on storage nodes E, A, B, C, and D respectively.
Things become interesting when the system gains some more nodes it needs to be scaled to 7 nodes,
    which means now the hash function should do mod 7 instead of a mod 5.

With the new hash function the same 5 files ‘f1.txt’, ‘f2.txt’, ‘f3.txt’, ‘f4.txt’, ‘f5.txt’
    will now be associated with storage nodes D, E, F, G, A.
Here we see that changing the hash function requires us to move every single one of the 5 files to a different node.

Changing hash function every time we scale up/down and moves a lot of nodes : expensive and infeasible

---

How to consistent hashing? HashSpace/Ring : huge and constant size : so less collisions
    - keep hash function independent of the number of storage nodes
    - keep associations relative and not driven by collisions

   ____ B ____ A ________ E
all _ (nodes) before B -> serve to B node, all _ before A -> serve to A node and so on...
This way : data migrated during scale up/down : k / n where k = total keys and n = total nodes

Implement : big array of size = hash space and putting files and storing nodes on the hashed location.
    To get node -> move clockwise until you find storage_node which serves that request.

        Problem : requires huge memory to hold such a large array & iterating over this array is O(hash_space) which is as good as O(N) since hash_space size is very large.

# Better way to implement.
    2 arrays : one to hold storage nodes : node and one to hold positions of storage node in hash space : keys
    nodes[i] maps to keys[i] : both arrays in sorted as per keys

---
Hash Function in CH
total_slots : size of hash space of order 2 ^ 25r6 (since it's huge the hashfunction is independent of actual number of storage_nodes present in system and is unaffected by scale up/down events)

----
Fun : adding new node to system.
    - find position of node where it resides in hash space
    - populate new node with data its serving
    - add node in hash space

___B_____________E__
Add K
__B______K_______E____ (few requests serving from B to E now serve to K) {as more nodes added : more consistent the system is}


The data belonging to the segment B-K could be found at node E to which they were previously associated with.
 Thus the only files affected and that needs migration are in the segment B-K; and their association changes from node E to node K.

---
Assign
how to efficiently we can find the “node to the right” for a given item.
The operation to find the association has to be super fast as it is something that will be invoked for every single read
  and write that happens on the system.

O(log(n)) : First pass item to hash function and fetch position where item is hashed in HS
    This position is then searched in keys array to obtain index of first key which is greater than the position
    if no keys greater : circle back and return 0th index otherwise return the next index
