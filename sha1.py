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
    return x

def padding(message):
    # Pads the input message with zeros so that padded_data has 64 bytes or 512 bits
    padded_value=''
    message_bin = ''

    for char in message:
        # Convert message to hex value and to bin value
        binary_char = bin(char)[2:].zfill(8)
        padded_value += hex(int(binary_char, 2))[2:]
        message_bin  += binary_char + " "

    padded_80 = bytes.fromhex(hex(int("10000000",2))[2:])    # add 1 bit or total of 10000000 bits
    padded_80_bin = bin(*list(padded_80))[2:]
    message_bin += padded_80_bin


    padding = padded_80 + b"\x00" * (63 - (len(message) + 8) % 64)
    padded_value += str(padding.hex()) + str(struct.pack(">Q", 8 * len(message)).hex())

    #return padded_data
    return bytes.fromhex(padded_value.strip())

def sha1(message):
    # displays Padd calculation
    # Step 1: Append padding bits and length
    message = padding(message)

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

            temp = (rotate_left(a, 5) + f + e + k + w[j]) & 0xffffffff    # or % (1 << 32)  or  n mod 2^32

            e = d
            d = c
            c = rotate_left(b, 30)
            b = a
            a = temp
            
        # Step 6: Add the hash value of this block to the result
        a = (a + temp_a) & 0xffffffff    # or % (1 << 32)  or  n mod 2^32
        b = (b + temp_b) & 0xffffffff
        c = (c + temp_c) & 0xffffffff
        d = (d + temp_d) & 0xffffffff
        e = (e + temp_e) & 0xffffffff
    # Step 7: return Hash value
    return hex(a)[2:]+hex(b)[2:]+hex(c)[2:]+hex(d)[2:]+hex(e)[2:]
    
message = b'ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCD'  # 960 bits

print(sha1(message))


# In the padding rule for SHA-1, if the length of the message is already congruent or greater than 448 bits (mod 512 bits), 
# then Step 2 requires appending an additional 512 bits of padding. 
# This may seem counterintuitive, but it is necessary to ensure that the length of the padded message is a multiple of 512 bits.



