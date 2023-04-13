import struct
import sys 

stdoutOrigin=sys.stdout 
# if error due to file not found use proper directory format example: open("D:/Documents/log_YOURLASTNAME.txt", "w")
sys.stdout = open("log_YOURLASTNAME.txt", "w")

# Define constants used in the SHA-1 algorithm
H0 = 0x67452301
H1 = 0xEFCDAB89
H2 = 0x98BADCFE
H3 = 0x10325476
H4 = 0xC3D2E1F0

def rotate_left(n, b):
    x = ((n << b) | (n >> (32 - b))) & 0xffffffff
    return x

#Pads the input message with zeros so that padded_data has 64 bytes or 512 bits
def padding(message):
    padding = b"\x80" + b"\x00" * (63 - (len(message) + 8) % 64)
    padded_data = message + padding + struct.pack(">Q", 8 * len(message))
    return padded_data

# Define the SHA-1 functions
def sha1(message):
    # displays Padd calculation
    # 1. define ml as length of the message multiplied by 8 bits.
    ml = len(message)*8
    # 2. print value of ml
    print(f"Message length: {ml} ")
    # 3. print(f"{__} mod {512} = {__ % __}")
    # 4. print(f"{__} padded with 512-{__ % 512} = {512 - __ % 512} bits or {int((512 - __ % 512)/__)} bytes = {__ + (512 - __ % 512)}")

    # 5. if __ % 512 >= __:
        # 6. print(f"Since {__ % 512} >= to 448 bit so, plus 512 bits or {int(512/__)} bytes padding")
    
    # Step 1: Append padding bits and length
    message = padding(message)
    # 6. print("Message len after padding:",___)  
    # 7. print("Message:",__)   #512 bits  padded

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

        # 8. print(f"Message chunk {__}: {message[__}")

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

            # 9.
            # print(f"Chunk {__} : Iteration {__}:")
            # print(f"a = {__}")  #you can use hex() fuction and [2:]
            # print(f"b = {__}")
            # print(f"c = {__}")
            # print(f"d = {__}")
            # print(f"e = {__}")
            # print(f"Hash value: {__}")

            e = d
            d = c
            c = rotate_left(b, 30)
            b = a
            a = temp

        # Step 6: Add the hash value of this block to the result
        # print(f"Processed message in 512-bit chunk {int((i+64)/64)-1}")
        
        # 10. Follow the proper output
        # print(f"{temp_a} + {a} = {(a + temp_a) & 0xffffffff}")  #you can use hex() fuction and [2:]
        # print(f"{temp_b} + {b} = {(b + temp_b) & 0xffffffff}")
        # print(f"{temp_c} + {c} = {(c + temp_c) & 0xffffffff}")
        # print(f"{temp_d} + {d} = {(d + temp_d) & 0xffffffff}")
        # print(f"{temp_e} + {e} = {(e + temp_e) & 0xffffffff}")

        a = (a + temp_a) & 0xffffffff    # or % (1 << 32)  or  n mod 2^32
        b = (b + temp_b) & 0xffffffff
        c = (c + temp_c) & 0xffffffff
        d = (d + temp_d) & 0xffffffff
        e = (e + temp_e) & 0xffffffff

        # 11. print("Hash value:",__)

    return a,b,c,d,e   # 12. convert it to final hash.
    

message = b'ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ'  # 960 bits
print("FINAL HASH:",sha1(message))


# In the padding rule for SHA-1, if the length of the message is already congruent or greater than 448 bits (mod 512 bits), 
# then Step 2 requires appending an additional 512 bits of padding. 
# This may seem counterintuitive, but it is necessary to ensure that the length of the padded message is a multiple of 512 bits.


