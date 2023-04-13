# Import required modules
import binascii, hashlib, sys

stdoutOrigin=sys.stdout 
sys.stdout = open("hmac_sc_withmodule_OUTPUT.txt", "w")

def H_MAC(secret_key, message):
    # Define the inner and outer pads for the key
    ipad = b'\x36' * 64
    opad = b'\x5c' * 64

    # If the key is longer than 64 bytes, hash it using SHA-1 to generate a new 64-byte key.
    if len(secret_key) > 64:
        secret_key = hashlib.sha1(secret_key).digest()
        print(f"secret_key > 64! New key: {binascii.hexlify(secret_key).decode()}")

    # Pad the key with zeros to 64 bytes (512 bits) and define the inner and outer padding values
    padded_secret_key = secret_key + b"\x00"*(64-len(secret_key))

    #print inputs
    print(f"message: \t\t{message}\n\t\t\t\t{''.join('{:08b}'.format(byte) for byte in message)}")
    print(f"\t\t\t\t{binascii.hexlify(message).decode()}")
    print(f"secret_key: \t{secret_key}\n\t\t\t\t{''.join('{:08b}'.format(byte) for byte in secret_key)}")
    print(f"padded_s_key: \t{padded_secret_key}\n\t\t\t\t{''.join('{:08b}'.format(byte) for byte in padded_secret_key)}")
    print(f"\t\t\t\t{binascii.hexlify(padded_secret_key).decode()}")
    print(f"ipad: \t\t\t{ipad}\n\t\t\t\t{''.join('{:08b}'.format(byte) for byte in ipad)}")
    print(f"opad: \t\t\t{opad}\n\t\t\t\t{''.join('{:08b}'.format(byte) for byte in opad)}\n")

    # Perform the inner and outer padding operations by XORing the key with the ipad and opad values.
    XOR_padded_secret_key_ipad = bytes([padded_secret_key[i] ^ ipad[i] for i in range(64)])
    print(f"p_skey binary: \t{''.join('{:08b}'.format(byte) for byte in padded_secret_key)}")
    print(f"ipad binary: \t{''.join('{:08b}'.format(byte) for byte in ipad)}")
    print(f"XOR_psk_ipad: \t{''.join('{:08b}'.format(byte) for byte in XOR_padded_secret_key_ipad)}")
    print(f"XOR_psk_ipad: \t{XOR_padded_secret_key_ipad}")
    print(f"XOR_psk_ipad: \t{binascii.hexlify(XOR_padded_secret_key_ipad).decode()}\n")
    
    XOR_padded_secret_key_opad = bytes([padded_secret_key[i] ^ opad[i] for i in range(64)])
    print(f"p_skey binary: \t{''.join('{:08b}'.format(byte) for byte in padded_secret_key)}")
    print(f"opad binary: \t{''.join('{:08b}'.format(byte) for byte in opad)}")
    print(f"XOR_psk_opad: \t{''.join('{:08b}'.format(byte) for byte in XOR_padded_secret_key_opad)}")
    print(f"XOR_psk_opad: \t{XOR_padded_secret_key_opad}")
    print(f"XOR_psk_opad: \t{binascii.hexlify(XOR_padded_secret_key_opad).decode()}\n")
    
    
    # Combine the padded key with the hash of the padded key and message, then hash the result using SHA-1.
    XOR_padded_secret_key_ipad_plus_message = XOR_padded_secret_key_ipad + message
    print(f"XOR_psk_ipad: \t{''.join('{:08b}'.format(byte) for byte in XOR_padded_secret_key_ipad)}")
    print(f"\t+message:   {''.join('{:08b}'.format(byte) for byte in message)}")
    print(f"\t\t   =:   {''.join('{:08b}'.format(byte) for byte in XOR_padded_secret_key_ipad_plus_message)}")
    print(f"\t\t   =:   {XOR_padded_secret_key_ipad_plus_message}")
    print(f"\t\t   =:   {binascii.hexlify(XOR_padded_secret_key_ipad_plus_message).decode()}\n")

    # Combine the padded key with the hash of the padded key and message, then hash the result using SHA-1.
    tag = hashlib.sha1(XOR_padded_secret_key_opad + hashlib.sha1(XOR_padded_secret_key_ipad_plus_message).digest()).digest()
    print(f"\nMAC = sha1(XOR_padded_secret_key_opad + sha1(XOR_padded_secret_key_ipad_plus_message))")
    print(f"MAC = sha1(XOR_padded_secret_key_opad + {hashlib.sha1(XOR_padded_secret_key_ipad_plus_message).digest()})")
    print(f"MAC = sha1(XOR_padded_secret_key_opad + {binascii.hexlify(hashlib.sha1(XOR_padded_secret_key_ipad_plus_message).digest()).decode()})")
    print(f"MAC = sha1({XOR_padded_secret_key_opad+hashlib.sha1(XOR_padded_secret_key_ipad_plus_message).digest()})")
    print(f"MAC = {' '.join('{:08b}'.format(byte) for byte in tag)}")
    print(f"MAC =  {tag}")

    # Convert the resulting HMAC value to a hex-encoded string and print it.
    tag = binascii.hexlify(tag).decode()
    print(f"HMAC value: {tag}\n\n")
    return tag

# Define the key and message to be authenticated
#alice sender
shared_secret = b'passwordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpassword'
alice_message = b'PLS deposit 1,000,000.00 pesos to this bank account: 1232322356 A.S.A.P'
alice_HMAC = H_MAC(shared_secret,alice_message)

# Alice sends the message and the HMAC tag to Bob
print(f"Alice sends message: {alice_message}")
print(f"Alice sends HMAC tag: {alice_HMAC}\n")

# Bob receives the message and HMAC tag from Alice
print("Bob receives the message and HMAC tag from Alice\n")
received_message = b'PLS deposit 1,000,000.00 pesos to this bank account: 1232322356 A.S.A.P'
bob_hmac_digest = H_MAC(shared_secret,received_message)

# Bob computes the HMAC of the received message using the shared secret key and SHA-1 hash function
print(f"Alice HMAC(TAG) : {alice_HMAC}")
print(f"Bob HMAC(TAG)   : {bob_hmac_digest}")
if alice_HMAC == bob_hmac_digest:
    # HMACs match, message is authentic
    print("Bob received authentic message from Alice!")
else:
    # HMACs don't match, message may be tampered with
    print("Bob received message, but it may have been tampered with!")

             
# Import the required libraries - hashlib and binascii.
# Define the HMAC function which takes in two arguments, key and message.
# Define the inner and outer pads for the key as ipad and opad respectively, both of length 64 bytes.
# Check if the length of the key is greater than 64 bytes, if so, hash the key using SHA-1 to generate a new 64-byte key.
# Pad the key with zeros to create a 64-byte key.
# Perform the inner and outer padding operations by XORing the key with the ipad and opad values.
# Combine the padded key with the message and hash the result using SHA-1.
# Combine the padded key with the hash of the padded key and message, then hash the result using SHA-1.
# Convert the resulting HMAC value to a hex-encoded string and print it.
# Return the HMAC value.