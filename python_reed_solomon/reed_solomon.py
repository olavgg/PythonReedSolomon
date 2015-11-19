import numpy as np


class ReedSolomon(object):

    def __init__(self, data_shard_count, parity_shard_count):
        self.data_shard_count = data_shard_count
        self.parity_shard_count = parity_shard_count
        if self.data_shard_count + self.parity_shard_count > 256:
            raise ValueError("Too many shards - max is 256")

        self.matrix = self.build_matrix()

    def build_matrix(self):
        rows = np.array([1,2,4])
        matrix = np.vander(rows,2)
        return []