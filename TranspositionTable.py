class TranspositionTable:
    def __init__(self, size):
        self.size = size
        self.table = [None] * size

    def _hash(self, key):
        return hash(key) % self.size

    def insert(self, key, data):
        self.table[self._hash(key)] = data

    def get(self, key):
        return self.table[self._hash(key)]
