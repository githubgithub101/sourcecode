# Import required modules
import binascii, hashlib, sys

stdoutOrigin=sys.stdout 
sys.stdout = open("hmac_sc_withmodule_OUTPUT.txt", "w")

count = 0  # for display puposes only
# Define the XOR function to perform bitwise XOR operation
def XOR(raw1, raw2):
    global count
    if count == 0:
        print("padded_secret_key XOR opad")
    else:
        print("padded_secret_key XOR ipad")
    print(f"raw1 binary: \t\t{''.join('{:08b}'.format(byte) for byte in raw1)}")
    print(f"raw2 binary: \t\t{''.join('{:08b}'.format(byte) for byte in raw2)}")

    # Convert the raw data strings to binary using hex encoding, then perform a bitwise XOR operation on them.
    # Convert the resulting binary value to a string representation of binary using the 'bin()' function.
    value = bin(int(binascii.hexlify(raw1), 16) ^ int(binascii.hexlify(raw2), 16))

    # Convert the binary string representation to an integer using the 'int()' function with base 2.
    value = int(value, 2)

    # If the resulting integer has an odd number of digits when converted to a string, pad it with a leading zero and convert it to binary data using the 'binascii.unhexlify()' function.
    # This is done because the binary data should have an even number of digits, since each hex digit corresponds to 4 binary digits.
    if len(str(value)) % 2 == 1:
        value = binascii.unhexlify('0%x' % value)
    else:
        # Otherwise, convert the resulting integer to binary data without padding.
        value = binascii.unhexlify('%x' % value)

    print(f"XOR value:   \t\t{''.join('{:08b}'.format(byte) for byte in value)}")
    print(f"value: \t\t\t\t{value}\n")

    count +=1
    return value

def H_MAC(secret_key, message):
    # Define the inner and outer pads for the key
    ipad = b'\x36' * 64
    opad = b'\x5c' * 64

    # If the key is longer than 64 bytes, hash it using SHA-1 to generate a new 64-byte key.
    if len(secret_key) > 64:
        secret_key = hashlib.sha1(secret_key).digest()

    # Pad the key with zeros to 64 bytes (512 bits) and define the inner and outer padding values
    padded_secret_key = secret_key + b"\x00"*(64-len(secret_key))

    
    print(f"message: \t\t{message}\n\t\t\t\t{''.join('{:08b}'.format(byte) for byte in message)}")
    print(f"secret_key: \t{secret_key}\n\t\t\t\t{''.join('{:08b}'.format(byte) for byte in secret_key)}")
    print(f"padded_s_key: \t{padded_secret_key}\n\t\t\t\t{''.join('{:08b}'.format(byte) for byte in padded_secret_key)}")
    print(f"ipad: \t\t\t{ipad}\n\t\t\t\t{''.join('{:08b}'.format(byte) for byte in ipad)}")
    print(f"opad: \t\t\t{opad}\n\t\t\t\t{''.join('{:08b}'.format(byte) for byte in opad)}\n")

    # Calculate the HMAC tag using the SHA-1 hash function
    XOR_padded_secret_key_opad = bytes([padded_secret_key[i] ^ opad[i] for i in range(64)])
    XOR_padded_secret_key_ipad = bytes([padded_secret_key[i] ^ ipad[i] for i in range(64)])
    XOR_padded_secret_key_ipad_plus_message = XOR_padded_secret_key_ipad + message

    print(f"\t\t     XOR_padded_secret_key_ipad: {''.join('{:08b}'.format(byte) for byte in XOR_padded_secret_key_ipad)}")
    print(f"\t\t\t\t\t\t      + message: {''.join('{:08b}'.format(byte) for byte in message)}")
    print(f"XOR_padded_secret_key_ipad_plus_message: {''.join('{:08b}'.format(byte) for byte in XOR_padded_secret_key_ipad_plus_message)}")
    print(f"XOR_padded_secret_key_ipad_plus_message: {XOR_padded_secret_key_ipad_plus_message}")

    tag = hashlib.sha1(XOR_padded_secret_key_opad + hashlib.sha1(XOR_padded_secret_key_ipad_plus_message).digest()).digest()
    print(f"\nMAC = sha1(XOR_padded_secret_key_opad + sha1(XOR_padded_secret_key_ipad_plus_message))")
    print(f"MAC = sha1(XOR_padded_secret_key_opad + {hashlib.sha1(XOR_padded_secret_key_ipad_plus_message).digest()})")
    print(f"MAC = sha1({XOR_padded_secret_key_opad+hashlib.sha1(XOR_padded_secret_key_ipad_plus_message).digest()})")
    print(f"MAC =  {tag}")
    tag = binascii.hexlify(tag).decode()
    print(f"HMAC value: {tag}\n\n")
    return tag

# # Define a function that takes a shared secret and a message as inputs
# def checkif64(shared_secret, message):
#     # If the length of the shared secret is greater than 64 bytes, hash it using SHA-1 to generate a new 64-byte key.
#     if len(shared_secret) > 64:
#         shared_secret = binascii.hexlify(hashlib.sha1(shared_secret).digest()).decode()
#         # Print a message indicating that the key has been updated.
#         print(f"Key > 64 bytes! New key is:{shared_secret}")
#         # Calculate the HMAC value using the new 64-byte key and the message.
#         HMAC_value = H_MAC(bytes(shared_secret.encode()), message)
#     else:
#         # Otherwise, calculate the HMAC value using the original shared secret and the message.
#         HMAC_value = H_MAC(shared_secret, message)
#     # Return the HMAC value.
#     return HMAC_value


# Define the key and message to be authenticated
#alice sender
shared_secret = b'abcdefghijklmnopqrstuvqxyzabcdefghijklmnopqrstuvqxyzabcdefghijkld'
alice_message = b'PLS send 1,000,0000 pesos to this bank account: 1232322356 A.S.A.P'
alice_HMAC = H_MAC(shared_secret,alice_message)

# Alice sends the message and the HMAC digest to Bob
print(f"Alice sends message: {alice_message}")
print(f"Alice sends HMAC digest: {alice_HMAC}")

# Bob receives the message and HMAC digest from Alice
received_message = b'PLS send 1,000,0000 pesos to this bank account: 1023224342 A.S.A.P'
bob_hmac_digest = H_MAC(shared_secret,received_message)

# Bob computes the HMAC of the received message using the shared secret key and SHA-256 hash function
print(f"Alice HMAC : {alice_HMAC}")
print(f"Bob HMAC   : {bob_hmac_digest}")
if alice_HMAC == bob_hmac_digest:
    # HMACs match, message is authentic
    print("Bob received authentic message from Alice!")
else:
    # HMACs don't match, message may be tampered with
    print("Bob received message, but it may have been tampered with!")

             

# In this code, we import the binascii and hashlib modules. The binascii module is used for conversion between binary and ASCII formats, and the hashlib module provides a secure way to generate different types of hash functions.
# We define the secret_key and message variables as byte strings, which are the inputs to the HMAC algorithm.
# We pad the secret_key key with zeros to make it a 64-byte (512-bit) string and define two padding values, ipad and opad. These values are used in the HMAC algorithm to create two different hash functions.
# We define the XOR function to perform a bitwise XOR operation between two byte strings. The XOR function takes two byte strings as inputs, converts them to integers, performs the XOR operation, and then returns the resulting byte string.
# We calculate the HMAC tag using the SHA-1 hash function by first applying the outer padding (opad) to the padded key (padded_secret_key) using the XOR function. We then apply the inner padding (ipad) to the padded key (padded_secret_key) and concatenate the result with the message (message). We apply the SHA-1 hash function to this concatenated string, and then concatenate the resulting hash with the result of the previous step. We then apply the SHA-1 hash function to this final concatenated string to produce the HMAC tag.
# Finally, we print the tag as a hex-encoded string using the binascii.hexlify function.
