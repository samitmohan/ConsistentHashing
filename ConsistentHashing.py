# Building storage system
import hashlib
import bisect
from bisect import bisect_left, bisect_right


class StorageNode:
  pass

storage_nodes = [
  StorageNode(name="B", host="10.131.217.11"),
  StorageNode(name="C", host="10.131.142.46"),
  StorageNode(name="D", host="10.131.114.17"),
  StorageNode(name="E", host="10.131.189.18")
]


def hash_fn(key):
  # sums bytes present in key and mod with size (generates op in range of 0-4)
  return sum(bytearray(key.encode('utf-8'))) % 5


def upload(path):
  # hash function to get index of storage node:
  index = hash_fn(path)
  node = storage_nodes[index]
  return node.put_file(path)


def fetch(path):
  index = hash_fn(path)
  node = storage_nodes[index]
  return node.fetch_file(path)


def hash_fun_ch(key: str, total_slots: int) -> int:
  hsh = hashlib.sha256()
  # converting data into bytes
  hsh.update(bytes(key.encode('utf-8')))
  # HEX -> int
  return int(hsh.hexdigest(),
              16) % total_slots  # string.hexdigits is a pre-initialized string used as string constants


def add_node(self, node: StorageNode) -> int:
  # adds new node in system and returns key from hash space where it was placed
  # handling error when hash space is full
  if len(self.keys) == self.total_slots:
    raise Exception("Full")
  key = hash_fun_ch(node.host, self.total_slots)  # key and slots
  # find index where key should be inserted in keys array : index where storageNode will be added in nodes array
  # We find the index of the smallest key greater than the position in the sorted keys array using binary search.
  index = bisect(self.keys, key)  # bisect : returns position -> if element already present : rightmost position is
  # returned
  # if we've already seen key (node already present) : collision
  if index and self.keys[index - 1] == key:
    raise Exception("Collision")

  # insert node and key
  self.nodes.insert(index, node)
  self.keys.insert(index, key)

  return key


def remove_node(self, node: StorageNode) -> int:
  # removes node and returns key from hash space on which node was placed
  if len(self.keys) == 0:
    raise Exception("Hash Space is empty")
  key = hash_fun_ch(node.host, self.total_slots)
  # find index where key resides in the keys
  index = bisect_left(self.keys, key)  # bisect_left : returns position -> if element already present : leftmost
  # position is returned

  # if key do not exist raise exception
  if index >= len(self.keys) or self.keys[index] != key:
    raise Exception("Node does not exist")

  # remove from both keys and nodes array
  self.keys.pop(index)
  self.nodes.pop(index)
  return key


def assign(self, item: str) -> str:
  # given item function returns node it is associated with
  key = hash_fun_ch(item, self.total_slots)
  # first node to the right of this key : if bisect_right returns index which is out of bounds : circle back (% size)
  index = bisect_right(self.keys, key) % len(self.keys)

  return self.nodes[index]