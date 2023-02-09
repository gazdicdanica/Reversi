import random
from map import Map


class HashMap(object):
    def __init__(self, capacity=11):
        self._data = capacity * [None]
        self._capacity = capacity
        self._size = 0
        self.prime = 109345121

        self._a = 1 + random.randrange(self.prime - 1)
        self._b = random.randrange(self.prime)

    def __len__(self):
        return self._size

    def _hash(self, x):
        hashed_value = (hash(x) * self._a + self._b) % self.prime
        compressed = hashed_value % self._capacity
        return compressed

    def __getitem__(self, key):
        bucket_index = self._hash(key)
        return self._bucket_getitem(bucket_index, key)

    def __setitem__(self, key, value):
        bucket_index = self._hash(key)
        self._bucket_setitem(bucket_index, key, value)

    def __delitem__(self, key):
        bucket_index = self._hash(key)
        self._bucket_delitem(bucket_index, key)

    def _bucket_getitem(self, index, key):
        raise NotImplementedError()

    def _bucket_setitem(self, bucket_index, key, value):
        raise NotImplementedError()

    def _bucket_delitem(self, bucket_index, key):
        raise NotImplementedError()

    def items(self):
        raise NotImplementedError()


class Hashmap(HashMap):
    def _bucket_getitem(self, index, key):
        bucket = self._data[index]
        if bucket is None:
            raise KeyError('Ne postoji element sa traženim ključem.')

        return bucket[key]

    def _bucket_setitem(self, bucket_index, key, value):
        bucket = self._data[bucket_index]
        if bucket is None:
            self._data[bucket_index] = Map()

        current_size = len(self._data[bucket_index])
        self._data[bucket_index][key] = value
        if len(self._data[bucket_index]) > current_size:
            self._size += 1

    def _bucket_delitem(self, bucket_index, key):
        bucket = self._data[bucket_index]
        if bucket is None:
            raise KeyError('Ne postoji element sa traženim ključem.')

        del bucket[key]
        self._size -= 1

    def items(self):
        for bucket in self._data:
            if bucket is not None:
                for key, value in bucket.items():
                    yield key, value

    def __iter__(self):
        for bucket in self._data:
            if bucket is not None:
                for key in bucket:
                    yield key
