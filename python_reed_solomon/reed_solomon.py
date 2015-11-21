import numpy as np

#np.set_printoptions(formatter={'int':hex})

class ReedSolomon(object):

    def __init__(self, data_shard_count, parity_shard_count):
        self.data_shard_count = data_shard_count
        self.parity_shard_count = parity_shard_count
        if self.data_shard_count + self.parity_shard_count > 256:
            raise ValueError("Too many shards - max is 256")

        self.total_shard_count = int(data_shard_count + parity_shard_count)
        self.matrix = self.build_matrix(
            data_shard_count,
            self.total_shard_count
        )

    def build_matrix(self, data_shard_count, total_shard_count):
        # Start with a Vandermonde matrix.  This matrix would work,
        # in theory, but doesn't have the property that the data
        # shards are unchanged after encoding.
        rows = np.array([x for x in range(total_shard_count)])
        matrix = np.vander(rows,data_shard_count, increasing=True)
        top_matrix = matrix[0:data_shard_count]
        print(top_matrix)
        inv_matrix = np.linalg.inv(top_matrix)
        print(inv_matrix)

        # Multiple by the inverse of the top square of the matrix.
        # This will make the top square be the identity matrix, but
        # preserve the property that any square subset of rows is invertible.
        return []
