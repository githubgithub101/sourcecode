import struct
import sys 

stdoutOrigin=sys.stdout 
sys.stdout = open("log_YOURLASTNAME.txt", "w")

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
    print()

    padded_value=''
    message_bin = ''

    for char in message:
        # Convert message to hex value and to bin value
        binary_char = bin(char)[2:].zfill(8)
        padded_value += hex(int(binary_char, 2))[2:]
        message_bin  += binary_char + " "
    
    print("char to hex ",message.decode(),"\n\t\t\t",' '.join([padded_value[i:i+2] for i in range(0, len(padded_value), 2)]))

    padded_80 = bytes.fromhex(hex(int("10000000",2))[2:])    # add 1 bit or total of 10000000 bits
    padded_80_bin = bin(*list(padded_80))[2:]

    print("message_bin:\t\t\t",message_bin)
    message_bin += padded_80_bin
    print("message_bin + 1 bit:\t",message_bin)


    #original
    padding = padded_80 + b"\x00" * (63 - (len(message) + 8) % 64)

    padded_len = int(((len(padded_value)+len(str(padding.hex())))/2)*8)
    print("char_hex",padded_len,"bits:\t\t",padded_value,str(padded_80.hex()) , str(b"\x00".hex()) * (63 - (len(message) + 8) % 64))
    padded_data = message + padding + struct.pack(">Q", 8 * len(message))
    padded_value += str(padding.hex()) + str(struct.pack(">Q", 8 * len(message)).hex())
    print(len(message)*8,"+", 512 - len(message)*8 % 512, ":",(len(message)*8)+512 - len(message)*8 % 512,"\t",padded_value)
    # print(bytes.fromhex(char_hex))

    # hex_data = bytes.fromhex(char_hex)
    # Loop through the hex data, printing each DWORD on a separate line
    for i in range(0, len(padded_value), 8):
        dword = padded_value[i:i+8]
        print(dword, end=' ')
        if (i + 8) % 32 == 0:
            print()

    #return padded_data
    return bytes.fromhex(padded_value.strip())


def sha1(message):
    # displays Padd calculation
    ml = len(message)*8
    print("Message length before padding:",ml,"bits")
    print(f"{ml} mod {512} = {ml % 512}")
    print(f"{ml} padded with 512-{ml % 512} = {512 - ml % 512} bits or {int((512 - ml % 512)/8)} byte = {ml + (512 - ml % 512)} total bits")
    if ml % 512 >= 448:
        print(f"Since {ml % 512} >= to 448 bit so, plus 512 bits or {int(512/8)} byte padding")
    # Step 1: Append padding bits and length
    message = padding(message)
    print("Message length after padding:",len(message)*8)   #512 bits
    print("Message:",message)   #512 bits  padded
    print()

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

        print(f"Message chunk {i//64}: {message[i:i+64]}")
        # Step 4: Initialize hash value for this block
        temp_a = a
        temp_b = b
        temp_c = c
        temp_d = d
        temp_e = e

        # Step 5: Main loop
        for j in range(80):
            # print(f"Iteration {int((i+64)/64)-1} : {j}:")
            # print(f"a = {a} = {hex(a)[2:]}",bin(a).replace("0b", ""))
            # print(f"b = {b} = {hex(b)[2:]}",bin(b).replace("0b", ""))
            # print(f"c = {c} = {hex(c)[2:]}",bin(c).replace("0b", ""))
            # print(f"d = {d} = {hex(d)[2:]}",bin(d).replace("0b", ""))
            # print(f"e = {e} = {hex(e)[2:]}",bin(e).replace("0b", ""))
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


            # print(f"Iteration {int((i+64)/64)-1} : {j}:")
            # print(f"a = {a} = {hex(a)[2:]}",bin(a).replace("0b", ""))
            # print(f"b = {b} = {hex(b)[2:]}",bin(b).replace("0b", ""))
            # print(f"c = {c} = {hex(c)[2:]}",bin(c).replace("0b", ""))
            # print(f"d = {d} = {hex(d)[2:]}",bin(d).replace("0b", ""))
            # print(f"e = {e} = {hex(e)[2:]}",bin(e).replace("0b", ""))
            # print(f"f = {f} = {hex(f)[2:]}",bin(f).replace("0b", ""))
            # print(f"k = {k} = {hex(k)[2:]}",bin(k).replace("0b", ""))
            # print(f"w = {w[j]} = {hex(w[j])[2:]}",bin(w[j]).replace("0b", ""))
            # print(f"temp = {temp} = {hex(temp)[2:]}",bin(temp).replace("0b", ""))
            # print('{:08x}{:08x}{:08x}{:08x}{:08x}'.format(a, b, c, d, e))
            # print()



            print(f"Chunk {int((i+64)/64)-1} : Iteration {j}:")
            print(f"a = {hex(a)[2:]}")
            print(f"b = {hex(b)[2:]}")
            print(f"c = {hex(c)[2:]}")
            print(f"d = {hex(d)[2:]}")
            print(f"e = {hex(e)[2:]}")
            print(f"Hash value: {hex(a)[2:]+hex(b)[2:]+hex(c)[2:]+hex(d)[2:]+hex(e)[2:]}")
            print()


            e = d
            d = c
            c = rotate_left(b, 30)
            b = a
            a = temp
            # print(a, b, c, d, e)
            

        # Step 6: Add the hash value of this block to the result
        print(f"Processed message in 512-bit chunk {int((i+64)/64)-1}")
        print(f"{hex(temp_a)[2:]} + {hex(a)[2:]} = {hex((a + temp_a) & 0xffffffff)[2:]}")
        print(f"{hex(temp_b)[2:]} + {hex(b)[2:]} = {hex((b + temp_b) & 0xffffffff)[2:]}")
        print(f"{hex(temp_c)[2:]} + {hex(c)[2:]} = {hex((c + temp_c) & 0xffffffff)[2:]}")
        print(f"{hex(temp_d)[2:]} + {hex(d)[2:]} = {hex((d + temp_d) & 0xffffffff)[2:]}")
        print(f"{hex(temp_e)[2:]} + {hex(e)[2:]} = {hex((e + temp_e) & 0xffffffff)[2:]}")

        a = (a + temp_a) & 0xffffffff    # or % (1 << 32)  or  n mod 2^32
        b = (b + temp_b) & 0xffffffff
        c = (c + temp_c) & 0xffffffff
        d = (d + temp_d) & 0xffffffff
        e = (e + temp_e) & 0xffffffff

        print("Hash value:",hex(a)[2:]+hex(b)[2:]+hex(c)[2:]+hex(d)[2:]+hex(e)[2:])
        print()

    return hex(a)[2:]+hex(b)[2:]+hex(c)[2:]+hex(d)[2:]+hex(e)[2:]
    
# # file hashing
# with open('v7.Class-Plotting.xlsx', 'rb') as f:
#     chunk = 0
#     while chunk != b'':
#         chunk = f.read()  #64 bytes chunks
#         #sha1.update(chunk)
#         if chunk == b'': 
#             f.close()
#             break
#         print(f"FINAL HASH: {sha1(chunk)}")


#text hashing
# print("\n\ntext hashing")
message = b'ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCD'  # 960 bits
#message = b'ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ'  # 960 bits

print(f"FINAL HASH: {sha1(message)}\n\n")



# In the padding rule for SHA-1, if the length of the message is already congruent or greater than 448 bits (mod 512 bits), 
# then Step 2 requires appending an additional 512 bits of padding. 
# This may seem counterintuitive, but it is necessary to ensure that the length of the padded message is a multiple of 512 bits.



