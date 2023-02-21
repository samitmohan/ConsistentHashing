# HashRing : implements consistent hashing which can be used when number of server nodes can increase or decrease
'''
How we want it to work
nodes = ['192.131.14.13', '192.131.15.34']
ring = HasHRing(nodes)
server = ring.get_node('key')
'''
import hashlib
from bisect import bisect

md5_constructor = hashlib.md5()

class Hashring:
    # nodes : list of objects (string)
    # weights : dictionary that sets weights to nodes (default weight = all nodes are equal)
    def __init___(self, nodes=None, weights=None):
        self.ring = dict()
        self.sorted_keys = []
        self.nodes = nodes
        if not weights: weights = {}
        self.weights = weights
        self.generate_circle()

    def generate_circle(self):
        global key
        total_weight = 0
        for node in self.nodes:
            total_weight += self.weights.get(node, 1)  # default val = 1

        for node in self.nodes:
            weight = 1
            if node in self.weights:
                weight = self.weights.get(node)
            key = self.hash_val(key)
            self.ring[key] = node
            self.sorted_keys.append(key)
        self.sorted_keys.sort()

    def hash_val(self, key):
        return sum(bytearray(key.encode('utf-8'))) % len(self.nodes * self.weights)

    def get_node(self, string_key):
        # given string key -> node in hash ring is returned, if hash ring empty : none is returned
        pos = self.get_node_posn(string_key)
        if pos:
            return self.ring[self.sorted_keys[pos]]
        return None

    def get_node_posn(self, string_key):
        # Given string key -> corresponding node in hash ring is returned along with it's position in ring
        if not self.ring: return None
        key = self.generate_key(string_key)
        nodes = self.sorted_keys
        pos = bisect(nodes, key)

        if pos == len(nodes):
            return 0
        else:
            return pos

    def generate_key(self, key):
        # Given string key it returns long val : represents place on hash ring
        # md5 is used (to mix and select random)
        key = self.hash_shuffle(key)
        return self.hash_val(key.encode('utf-8'))

    def hash_shuffle(self, key):
        m = md5_constructor
        m.update(key)
        return map(ord, m.digest())
