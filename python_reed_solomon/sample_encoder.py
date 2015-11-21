#!/usr/bin/env python3.5

import sys
import binascii

from reed_solomon import ReedSolomon

headerSep = '|'

class SampleEncoder(object):
    DATA_SHARDS = 4
    PARITY_SHARDS = 2
    TOTAL_SHARDS = int(DATA_SHARDS + PARITY_SHARDS)

    BYTES_IN_INT = 4

    def MakeHeader(fname,n,k,size):
        return str.join(headerSep,
            ['FILE',fname,'n',n,'k',k,'size',size,'piece']
        ) + headerSep

    def main(self):
        total = len(sys.argv)
        if total == 2:
            f = open(sys.argv[1], 'rb')
            # with open(sys.argv[1], 'rb') as f:
            #    for piece in self.read_in_chunks(f):
            #        self.process_data(piece)

            f.seek(0, 2)
            fileSize = f.tell()
            size_as_bytes = int(fileSize).to_bytes(4, byteorder='big')
            #print("SIZE as bytes:")
            #print(binascii.hexlify(size_as_bytes))

            # Figure out how big each shard will be.  The total size stored
            # will be the file size (8 bytes) plus the file.
            storeSize = fileSize + SampleEncoder.BYTES_IN_INT
            shardSize = int(
                (storeSize + SampleEncoder.DATA_SHARDS - 1)
                / SampleEncoder.DATA_SHARDS
            )

            # Create a buffer holding the file size, followed by
            # the contents of the file.
            bufferSize = int(shardSize * SampleEncoder.DATA_SHARDS)
            allBytes = bytearray(bufferSize)

            # Insert size into the beginning of the bytearray
            allBytes[0:4] = size_as_bytes

            # Create a memory view of the byte array, needed to insert from
            # file with offset.
            allBytesView = memoryview(allBytes)

            # Start from the beginning of the file
            f.seek(0)
            # noinspection PyTypeChecker
            f.readinto(allBytesView[SampleEncoder.BYTES_IN_INT:])

            #print("DATA:")
            #print(binascii.hexlify(allBytes))

            # Make the buffers to hold the shards.
            shards = [
                bytearray(shardSize)
                      for x in range(SampleEncoder.TOTAL_SHARDS)
            ]

            # Fill in the data shards
            for i in range(SampleEncoder.DATA_SHARDS):
                shards[i] = allBytes[i*shardSize:(i*shardSize)+ shardSize]
                #print("SHARD "+str(i)+":")
                #print(binascii.hexlify(shards[i]))

            # Use Reed-Solomon to calculate the parity.
            rs = ReedSolomon(
                SampleEncoder.DATA_SHARDS,
                SampleEncoder.PARITY_SHARDS
            )


            f.close()
        else:
            print("Usage: python sample_encoder <fileName>")

    def read_in_chunks(self, file_object, chunk_size=131072):
        """
        Lazy function (generator) to read a file piece by piece.
        Default chunk size: 128k.
        """
        while True:
            data = file_object.read(chunk_size)
            if not data:
                break
            yield data

    def process_data(self, chunk):
        pass


if __name__ == "__main__":
    sampleEncoder = SampleEncoder()
    sampleEncoder.main()
