class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [[] for _ in range(self.size)]

    def hash_function(self, key):
        return hash(key) % self.size

    def insert(self, key, value):
        key_hash = self.hash_function(key)
        key_value = [key, value]

        for pair in self.table[key_hash]:
            if pair[0] == key:
                pair[1] = value
                return True
        self.table[key_hash].append(key_value)
        return True

    def get(self, key):
        key_hash = self.hash_function(key)
        for pair in self.table[key_hash]:
            if pair[0] == key:
                return pair[1]
        return None

    def delete(self, key):
        key_hash = self.hash_function(key)
        for index, pair in enumerate(self.table[key_hash]):
            if pair[0] == key:
                del self.table[key_hash][index]
                return True
        return False
