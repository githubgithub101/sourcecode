# from __future__ import print_function
# import struct
# import io

# try:
#     range = xrange
# except NameError:
#     pass


# def _left_rotate(n, b):
#     """Left rotate a 32-bit integer n by b bits."""
#     return ((n << b) | (n >> (32 - b))) & 0xffffffff


# def _process_chunk(chunk, h0, h1, h2, h3, h4):
#     """Process a chunk of data and return the new digest variables."""
#     assert len(chunk) == 64

#     w = [0] * 80

#     # Break chunk into sixteen 4-byte big-endian words w[i]
#     for i in range(16):
#         w[i] = struct.unpack(b'>I', chunk[i * 4:i * 4 + 4])[0]

#     # Extend the sixteen 4-byte words into eighty 4-byte words
#     for i in range(16, 80):
#         w[i] = _left_rotate(w[i - 3] ^ w[i - 8] ^ w[i - 14] ^ w[i - 16], 1)

#     # Initialize hash value for this chunk
#     a = h0
#     b = h1
#     c = h2
#     d = h3
#     e = h4

#     for i in range(80):
#         if 0 <= i <= 19:
#             # Use alternative 1 for f from FIPS PB 180-1 to avoid bitwise not
#             f = d ^ (b & (c ^ d))
#             k = 0x5A827999
#         elif 20 <= i <= 39:
#             f = b ^ c ^ d
#             k = 0x6ED9EBA1
#         elif 40 <= i <= 59:
#             f = (b & c) | (b & d) | (c & d)
#             k = 0x8F1BBCDC
#         elif 60 <= i <= 79:
#             f = b ^ c ^ d
#             k = 0xCA62C1D6

#         a, b, c, d, e = ((_left_rotate(a, 5) + f + e + k + w[i]) & 0xffffffff,
#                          a, _left_rotate(b, 30), c, d)

#     # Add this chunk's hash to result so far
#     h0 = (h0 + a) & 0xffffffff
#     h1 = (h1 + b) & 0xffffffff
#     h2 = (h2 + c) & 0xffffffff
#     h3 = (h3 + d) & 0xffffffff
#     h4 = (h4 + e) & 0xffffffff

#     return h0, h1, h2, h3, h4


# class Sha1Hash(object):
#     """A class that mimics that hashlib api and implements the SHA-1 algorithm."""

#     name = 'python-sha1'
#     digest_size = 20
#     block_size = 64

#     def __init__(self):
#         # Initial digest variables
#         self._h = (
#             0x67452301,
#             0xEFCDAB89,
#             0x98BADCFE,
#             0x10325476,
#             0xC3D2E1F0,
#         )

#         # bytes object with 0 <= len < 64 used to store the end of the message
#         # if the message length is not congruent to 64
#         self._unprocessed = b''
#         # Length in bytes of all data that has been processed so far
#         self._message_byte_length = 0

#     def update(self, arg):
#         """Update the current digest.

#         This may be called repeatedly, even after calling digest or hexdigest.

#         Arguments:
#             arg: bytes, bytearray, or BytesIO object to read from.
#         """
#         if isinstance(arg, (bytes, bytearray)):
#             arg = io.BytesIO(arg)

#         # Try to build a chunk out of the unprocessed data, if any
#         chunk = self._unprocessed + arg.read(64 - len(self._unprocessed))

#         # Read the rest of the data, 64 bytes at a time
#         while len(chunk) == 64:
#             self._h = _process_chunk(chunk, *self._h)
#             self._message_byte_length += 64
#             chunk = arg.read(64)

#         self._unprocessed = chunk
#         return self

#     def digest(self):
#         """Produce the final hash value (big-endian) as a bytes object"""
#         return b''.join(struct.pack(b'>I', h) for h in self._produce_digest())

#     def hexdigest(self):
#         """Produce the final hash value (big-endian) as a hex string"""
#         return '%08x%08x%08x%08x%08x' % self._produce_digest()

#     def _produce_digest(self):
#         """Return finalized digest variables for the data processed so far."""
#         # Pre-processing:
#         message = self._unprocessed
#         message_byte_length = self._message_byte_length + len(message)

#         # append the bit '1' to the message
#         message += b'\x80'

#         # append 0 <= k < 512 bits '0', so that the resulting message length (in bytes)
#         # is congruent to 56 (mod 64)
#         message += b'\x00' * ((56 - (message_byte_length + 1) % 64) % 64)

#         # append length of message (before pre-processing), in bits, as 64-bit big-endian integer
#         message_bit_length = message_byte_length * 8
#         message += struct.pack(b'>Q', message_bit_length)

#         # Process the final chunk
#         # At this point, the length of the message is either 64 or 128 bytes.
#         h = _process_chunk(message[:64], *self._h)
#         if len(message) == 64:
#             return h
#         return _process_chunk(message[64:], *h)


# def sha1(data):
#     """SHA-1 Hashing Function

#     A custom SHA-1 hashing function implemented entirely in Python.

#     Arguments:
#         data: A bytes or BytesIO object containing the input message to hash.

#     Returns:
#         A hex SHA-1 digest of the input message.
#     """
#     return Sha1Hash().update(data).hexdigest()


# if __name__ == '__main__':
#     # Imports required for command line parsing. No need for these elsewhere
#     import argparse
#     import sys
#     import os

#     # # Parse the incoming arguments
#     # parser = argparse.ArgumentParser()
#     # parser.add_argument('input', nargs='*',
#     #                     help='input file or message to hash')
#     # args = parser.parse_args()

#     # data = None
#     # if len(args.input) == 0:
#     #     # No argument given, assume message comes from standard input
#     #     try:
#     #         # sys.stdin is opened in text mode, which can change line endings,
#     #         # leading to incorrect results. Detach fixes this issue, but it's
#     #         # new in Python 3.1
#     #         data = sys.stdin.detach()

#     #     except AttributeError:
#     #         # Linux ans OSX both use \n line endings, so only windows is a
#     #         # problem.
#     #         if sys.platform == "win32":
#     #             import msvcrt

#     #             msvcrt.setmode(sys.stdin.fileno(), os.O_BINARY)
#     #         data = sys.stdin

#     #     # Output to console
#     #     print('sha1-digest:', sha1(data))

#     # else:
#     #     # Loop through arguments list
#     #     for argument in args.input:
#     #         if (os.path.isfile(argument)):
#     #             # An argument is given and it's a valid file. Read it
#     #             data = open(argument, 'rb')
                
#     #             # Show the final digest
#     #             print('sha1-digest:', sha1(data))
#     #         else:
#     #             print("Error, could not find " + argument + " file." )




# SPDX-FileCopyrightText: 2013-2015 AJ Alt
# SPDX-FileCopyrightText: 2019 Brent Rubell for Adafruit Industries
#
# SPDX-License-Identifier: MIT






# import struct
# from io import BytesIO

# # SHA Block size and message digest sizes, in bytes.
# SHA_BLOCKSIZE = 64
# SHA_DIGESTSIZE = 20

# # initial hash value [FIPS 5.3.1]
# K0 = 0x5A827999
# K1 = 0x6ED9EBA1
# K2 = 0x8F1BBCDC
# K3 = 0xCA62C1D6


# def _getbuf(data):
#     """Converts data into ascii,
#     returns bytes of data.
#     :param str bytes bytearray data: Data to convert.

#     """
#     if isinstance(data, str):
#         return data.encode("ascii")
#     return bytes(data)


# def _left_rotate(n, b):
#     """Left rotate a 32-bit integer, n, by b bits.
#     :param int n: 32-bit integer
#     :param int b: Desired rotation amount, in bits.

#     """
#     return ((n << b) | (n >> (32 - b))) & 0xFFFFFFFF


# # pylint: disable=invalid-name, too-many-arguments
# def _hash_computation(chunk, h0, h1, h2, h3, h4):
#     """Processes 64-bit chunk of data and returns new digest variables.
#     Per FIPS [6.1.2]
#     :param bytes bytearray chunk: 64-bit bytearray
#     :param list h_tuple: List of hash values for the chunk

#     """
#     assert len(chunk) == 64, "Chunk size should be 64-bits"

#     w = [0] * 80

#     # Break chunk into sixteen 4-byte big-endian words w[i]
#     for i in range(16):
#         w[i] = struct.unpack(b">I", chunk[i * 4 : i * 4 + 4])[0]

#     # Extend the sixteen 4-byte words into eighty 4-byte words
#     for i in range(16, 80):
#         w[i] = _left_rotate(w[i - 3] ^ w[i - 8] ^ w[i - 14] ^ w[i - 16], 1)

#     # Init. hash values for chunk
#     a = h0
#     b = h1
#     c = h2
#     d = h3
#     e = h4

#     for i in range(80):
#         if 0 <= i <= 19:
#             # Use alternative 1 for f from FIPS PB 180-1 to avoid bitwise not
#             f = d ^ (b & (c ^ d))
#             k = K0
#         elif 20 <= i <= 39:
#             f = b ^ c ^ d
#             k = K1
#         elif 40 <= i <= 59:
#             f = (b & c) | (b & d) | (c & d)
#             k = K2
#         elif 60 <= i <= 79:
#             f = b ^ c ^ d
#             k = K3

#         a, b, c, d, e = (
#             (_left_rotate(a, 5) + f + e + k + w[i]) & 0xFFFFFFFF,
#             a,
#             _left_rotate(b, 30),
#             c,
#             d,
#         )

#     # Add to chunk's hash result so far
#     h0 = (h0 + a) & 0xFFFFFFFF
#     h1 = (h1 + b) & 0xFFFFFFFF
#     h2 = (h2 + c) & 0xFFFFFFFF
#     h3 = (h3 + d) & 0xFFFFFFFF
#     h4 = (h4 + e) & 0xFFFFFFFF

#     return h0, h1, h2, h3, h4


# # pylint: disable=too-few-public-methods, invalid-name
# class sha1:
#     """SHA-1 Hash Object"""

#     digest_size = SHA_DIGESTSIZE
#     block_size = SHA_BLOCKSIZE
#     name = "sha1"

#     def __init__(self, data=None):
#         """Construct a SHA-1 hash object.
#         :param bytes data: Optional data to process

#         """
#         # Initial Digest Variables
#         self._h = (0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476, 0xC3D2E1F0)

#         # bytes object with 0 <= len < 64 used to store the end of the message
#         # if the message length is not congruent to 64
#         self._unprocessed = b""

#         # Length in bytes of all data that has been processed so far
#         self._msg_byte_len = 0

#         if data:
#             self.update(data)

#     def _create_digest(self):
#         """Returns finalized digest variables for the data processed so far."""
#         # pre-processing
#         message = self._unprocessed
#         message_len = self._msg_byte_len + len(message)

#         # add trailing '1' bit (+ 0's padding) to string [FIPS 5.1.1]
#         message += b"\x80"

#         # append 0 <= k < 512 bits '0', so that the resulting message length (in bytes)
#         # is congruent to 56 (mod 64)
#         message += b"\x00" * ((56 - (message_len + 1) % 64) % 64)

#         # append ml, the original message length, as a 64-bit big-endian integer.
#         message_bit_length = message_len * 8
#         message += struct.pack(b">Q", message_bit_length)

#         # Process the final chunk
#         h = _hash_computation(message[:64], *self._h)
#         if len(message) == 64:
#             return h
#         return _hash_computation(message[64:], *h)

#     def update(self, data):
#         """Updates the hash object with bytes-like object, data.
#         :param bytes data: bytearray or bytes object

#         """
#         # if we get a string, convert to a bytearray objects
#         data = _getbuf(data)

#         # Use BytesIO for stream-like reading
#         if isinstance(data, (bytes, bytearray)):
#             data = BytesIO(data)

#         # Try to build a chunk out of the unprocessed data, if any
#         chunk = self._unprocessed + data.read(64 - len(self._unprocessed))

#         while len(chunk) == 64:
#             self._h = _hash_computation(chunk, *self._h)
#             # increase the length of the message by 64 bytes
#             self._msg_byte_len += 64
#             # read the next 64 bytes
#             chunk = data.read(64)

#         self._unprocessed = chunk
#         return self

#     def digest(self):
#         """Returns the digest of the data passed to the update()
#         method so far.

#         """
#         return b"".join(struct.pack(b">I", h) for h in self._create_digest())

#     def hexdigest(self):
#         """Like digest() except the digest is returned as a string object of
#         double length, containing only hexadecimal digits.

#         """
#         return "".join(["%.2x" % i for i in self.digest()])



# byte_string = b"Hello"

# # Create a SHA-1 message
# print("--SHA1--")
# m = sha1()
# # Update the hash object with byte_string
# m.update(byte_string)
# # Obtain the digest, digest size, and block size
# print("Msg Digest: {}\nMsg Digest Size: {}\nMsg Block Size: {}".format(
#         m.hexdigest(), m.digest_size, m.block_size
#     )
# )









# import hashlib
# print(hashlib.sha1(b"HelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHello").hexdigest())








# import struct
# from io import BytesIO

# # SHA Block size and message digest sizes, in bytes.
# SHA_BLOCKSIZE = 64
# SHA_DIGESTSIZE = 20

# # initial hash value [FIPS 5.3.1]
# K0 = 0x5A827999
# K1 = 0x6ED9EBA1
# K2 = 0x8F1BBCDC
# K3 = 0xCA62C1D6


# def _getbuf(data):
#     """Converts data into ascii,
#     returns bytes of data.
#     :param str bytes bytearray data: Data to convert.

#     """
#     if isinstance(data, str):
#         return data.encode("ascii")
#     return bytes(data)


# def _left_rotate(n, b):
#     """Left rotate a 32-bit integer, n, by b bits.
#     :param int n: 32-bit integer
#     :param int b: Desired rotation amount, in bits.

#     """
#     return ((n << b) | (n >> (32 - b))) & 0xFFFFFFFF


# # pylint: disable=invalid-name, too-many-arguments
# def _hash_computation(chunk, h0, h1, h2, h3, h4):
#     """Processes 64-bit chunk of data and returns new digest variables.
#     Per FIPS [6.1.2]
#     :param bytes bytearray chunk: 64-bit bytearray
#     :param list h_tuple: List of hash values for the chunk

#     """
#     assert len(chunk) == 64, "Chunk size should be 64-bits"

#     w = [0] * 80

#     # Break chunk into sixteen 4-byte big-endian words w[i]
#     for i in range(16):
#         w[i] = struct.unpack(b">I", chunk[i * 4 : i * 4 + 4])[0]

#     # Extend the sixteen 4-byte words into eighty 4-byte words
#     for i in range(16, 80):
#         w[i] = _left_rotate(w[i - 3] ^ w[i - 8] ^ w[i - 14] ^ w[i - 16], 1)

#     # Init. hash values for chunk
#     a = h0
#     b = h1
#     c = h2
#     d = h3
#     e = h4

#     for i in range(80):
#         if 0 <= i <= 19:
#             # Use alternative 1 for f from FIPS PB 180-1 to avoid bitwise not
#             f = d ^ (b & (c ^ d))
#             k = K0
#         elif 20 <= i <= 39:
#             f = b ^ c ^ d
#             k = K1
#         elif 40 <= i <= 59:
#             f = (b & c) | (b & d) | (c & d)
#             k = K2
#         elif 60 <= i <= 79:
#             f = b ^ c ^ d
#             k = K3

#         a, b, c, d, e = (
#             (_left_rotate(a, 5) + f + e + k + w[i]) & 0xFFFFFFFF,
#             a,
#             _left_rotate(b, 30),
#             c,
#             d,
#         )
#         # print("a {} b {} c {} d {} e {} ".format(a, b, c, d, e))

#     # Add to chunk's hash result so far
#     h0 = (h0 + a) & 0xFFFFFFFF
#     h1 = (h1 + b) & 0xFFFFFFFF
#     h2 = (h2 + c) & 0xFFFFFFFF
#     h3 = (h3 + d) & 0xFFFFFFFF
#     h4 = (h4 + e) & 0xFFFFFFFF

#     #print("h0 {} h1 {} h2 {} h3 {} h4 {} ".format(h0, h1, h2, h3, h4))
#     return h0, h1, h2, h3, h4


# # pylint: disable=too-few-public-methods, invalid-name
# class sha1:
#     """SHA-1 Hash Object"""

#     digest_size = SHA_DIGESTSIZE
#     block_size = SHA_BLOCKSIZE
#     name = "sha1"

#     def __init__(self, data=None):
#         """Construct a SHA-1 hash object.
#         :param bytes data: Optional data to process

#         """
#         # Initial Digest Variables
#         self._h = (0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476, 0xC3D2E1F0)

#         # bytes object with 0 <= len < 64 used to store the end of the message
#         # if the message length is not congruent to 64
#         self._unprocessed = b""

#         # Length in bytes of all data that has been processed so far
#         self._msg_byte_len = 0

#         if data:
#             self.update(data)

#     def _create_digest(self):
#         """Returns finalized digest variables for the data processed so far."""
#         # pre-processing
#         message = self._unprocessed
#         message_len = self._msg_byte_len + len(message)

#         # add trailing '1' bit (+ 0's padding) to string [FIPS 5.1.1]
#         message += b"\x80"

#         # append 0 <= k < 512 bits '0', so that the resulting message length (in bytes)
#         # is congruent to 56 (mod 64)
#         message += b"\x00" * ((56 - (message_len + 1) % 64) % 64)

#         # append ml, the original message length, as a 64-bit big-endian integer.
#         message_bit_length = message_len * 8
#         message += struct.pack(b">Q", message_bit_length)

#         # Process the final chunk
#         h = _hash_computation(message[:64], *self._h)
#         if len(message) == 64:
#             return h
#         return _hash_computation(message[64:], *h)

#     def update(self, data):
#         """Updates the hash object with bytes-like object, data.
#         :param bytes data: bytearray or bytes object

#         """
#         # if we get a string, convert to a bytearray objects
#         data = _getbuf(data)

#         # Use BytesIO for stream-like reading
#         if isinstance(data, (bytes, bytearray)):
#             data = BytesIO(data)

#         # Try to build a chunk out of the unprocessed data, if any
#         chunk = self._unprocessed + data.read(64 - len(self._unprocessed))
#         count = 0                                                 #for remove
#         while len(chunk) == 64:
#             self._h = _hash_computation(chunk, *self._h)
#             print(count+1,*self._h)                                    #for remove
#             # increase the length of the message by 64 bytes
#             self._msg_byte_len += 64
#             # read the next 64 bytes
#             chunk = data.read(64)
#             count+=1                                                         #for remove

#         self._unprocessed = chunk
#         return self

#     def digest(self):
#         """Returns the digest of the data passed to the update()
#         method so far.

#         """
#         # digest = self._create_digest()
#         # #print("digest",list(digest))
#         # for h in digest:
#         #     packed_h = struct.pack(b">I", h)
#         #     #print(int("".join(map(str, list(packed_h)))))
#         # #print(b"".join(struct.pack(b">I", h) for h in self._create_digest()))
#         return b"".join(struct.pack(b">I", h) for h in self._create_digest())

#     def hexdigest(self):
#         """Like digest() except the digest is returned as a string object of
#         double length, containing only hexadecimal digits.

#         """
#         string_repr = " ".join(["%.2x" % i for i in self.digest()])
#         print(*self._create_digest())
#         print(self.digest())
#         print(string_repr)
#         print(*list(self.digest()))
#         return "".join(["%.2x" % i for i in self.digest()])



# byte_string = b"HelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHello"

# # Create a SHA-1 message
# print("--SHA1--")
# m = sha1()
# # Update the hash object with byte_string
# m.update(byte_string)
# # Obtain the digest, digest size, and block size
# print("Msg Digest: {}\nMsg Digest Size: {}\nMsg Block Size: {}".format(m.hexdigest(), m.digest_size, m.block_size))














# import hashlib

# def sha1_with_process(message):
#     sha1 = hashlib.sha1()

#     # Initial hash value
#     print("Initial hash value: ", sha1.hexdigest())

#     # Process each chunk of 64 bytes
#     for i in range(0, len(message), 64):
#         sha1.update(message[i:i+64])
#         print("Processing chunk", i//64+1, ":", sha1.hexdigest())

#     # Final hash value
#     print("Final hash value: ", sha1.hexdigest())

#     return sha1.hexdigest()

# # Example usage
# message = b'HelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHello'
# sha1_with_process(message)

#certutil -hashfile "test.txt" sha1




import struct

# Define constants used in the SHA-1 algorithm
H0 = 0x67452301
H1 = 0xEFCDAB89
H2 = 0x98BADCFE
H3 = 0x10325476
H4 = 0xC3D2E1F0

# Define the SHA-1 functions
def rotate_left(n, b):
    x = ((n << b) | (n >> (32 - b))) & 0xffffffff
    #print(x)
    return x

def sha1(message):
    # Step 1: Append padding bits and length
    ml = len(message)
    message += b'\x80'  #x80 is a hexadecimal escape sequence
    message += b'\x00' * ((56 - (ml + 1) % 64) % 64)  #(add 0s in decimal)
    message += struct.pack('>Q', ml * 8)
    print(len(message)*8)   #512 bits
    print(message)   #512 bits

    # Step 2: Initialize variables
    a = H0
    b = H1
    c = H2
    d = H3
    e = H4

    # Step 3: Process message in 512-bit blocks
    for i in range(0, len(message), 64):
        w = [0] * 80
        for j in range(16):
            w[j] = struct.unpack('>I', message[i + j * 4:i + j * 4 + 4])[0]
        for j in range(16, 80):
            w[j] = rotate_left(w[j-3] ^ w[j-8] ^ w[j-14] ^ w[j-16], 1)

        # Step 4: Initialize hash value for this block
        temp_a = a
        temp_b = b
        temp_c = c
        temp_d = d
        temp_e = e

        # Step 5: Main loop
        for j in range(80):
            if j < 20:
                f = (b & c) | ((~b) & d)
                k = 0x5A827999
            elif j < 40:
                f = b ^ c ^ d
                k = 0x6ED9EBA1
            elif j < 60:
                f = (b & c) | (b & d) | (c & d)
                k = 0x8F1BBCDC
            else:
                f = b ^ c ^ d
                k = 0xCA62C1D6

            temp = (rotate_left(a, 5) + f + e + k + w[j]) & 0xffffffff

            # print(f"Iteration {j}:")
            # print(f"a = {hex(a)}")
            # print(f"b = {hex(b)}")
            # print(f"c = {hex(c)}")
            # print(f"d = {hex(d)}")
            # print(f"e = {hex(e)}")
            # print(f"f = {hex(f)}")
            # print(f"k = {hex(k)}")
            # print(f"w[{j}] = {hex(w[j])}")
            # print(f"temp = {hex(temp)}")
            # print()




            e = d
            d = c
            c = rotate_left(b, 30)
            b = a
            a = temp
            # print(a, b, c, d, e)
            

            
            print(f"Iteration {j}:")
            print(f"a = {a} = "'{:08x}'.format(a),bin(a).replace("0b", ""))
            print(f"b = {b} = "'{:08x}'.format(b),bin(b).replace("0b", ""))
            print(f"c = {c} = "'{:08x}'.format(c),bin(c).replace("0b", ""))
            print(f"d = {d} = "'{:08x}'.format(d),bin(d).replace("0b", ""))
            print(f"e = {e} = "'{:08x}'.format(e),bin(e).replace("0b", ""))
            print(f"f = {f} = "'{:08x}'.format(f),bin(f).replace("0b", ""))
            print(f"k = {k} = "'{:08x}'.format(k),bin(k).replace("0b", ""))
            print(f"w = {w[j]} = "'{:08x}'.format(w[j]),bin(w[j]).replace("0b", ""))
            print(f"temp = {temp} = "'{:08x}'.format(temp),bin(temp).replace("0b", ""))
            print('{:08x}{:08x}{:08x}{:08x}{:08x}'.format(a, b, c, d, e))
            print()



        # Step 6: Add the hash value of this block to the result
        print(f"Process message in 512-bit blocks Iteration {i}:")
        print(f"({a} + {temp_a}) mod 2^32 = {(a + temp_a) & 0xffffffff}")
        print(f"({b} + {temp_b}) mod 2^32 = {(b + temp_b) & 0xffffffff}")
        print(f"({c} + {temp_c}) mod 2^32 = {(c + temp_c) & 0xffffffff}")
        print(f"({d} + {temp_d}) mod 2^32 = {(d + temp_d) & 0xffffffff}")
        print(f"({e} + {temp_e}) mod 2^32 = {(e + temp_e) & 0xffffffff}")

        a = (a + temp_a) & 0xffffffff    # or % (1 << 32)  or  n mod 2^32
        b = (b + temp_b) & 0xffffffff
        c = (c + temp_c) & 0xffffffff
        d = (d + temp_d) & 0xffffffff
        e = (e + temp_e) & 0xffffffff

        # print(f"Process message in 512-bit blocks Iteration {i}:")
        # print(f"a = {a} = {hex(a)} "'{:08x}'.format(a),bin(a).replace("0b", ""))
        # print(f"b = {b} = {hex(b)} "'{:08x}'.format(b),bin(b).replace("0b", ""))
        # print(f"c = {c} = {hex(c)} "'{:08x}'.format(c),bin(c).replace("0b", ""))
        # print(f"d = {d} = {hex(d)} "'{:08x}'.format(d),bin(d).replace("0b", ""))
        # print(f"e = {e} = {hex(e)} "'{:08x}'.format(e),bin(e).replace("0b", ""))
        print()
        print()

        

    # Step 7: Produce the final hash value (big-endian)
    print('{:08x}{:08x}{:08x}{:08x}{:08x}'.format(a, b, c, d, e))

    return '{:08x}{:08x}{:08x}{:08x}{:08x}'.format(a, b, c, d, e)


message = b'HelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHello'
# message = b"The quick brown fox jumps over the lazy dog.The quick brown fox jumps over the lazy dog.The quick brown fox jumps over the lazy dog.The quick brown fox jumps over the lazy dog.The quick brown fox jumps over the lazy dog.The quick brown fox jumps over the lazy dog.The quick brown fox jumps over the lazy dog.The quick brown fox jumps over the lazy dog.The quick brown fox jumps over the lazy dog.The quick brown fox jumps over the lazy dog."
print(sha1(message))