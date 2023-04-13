from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256

# Define the message to be encrypted
message = b'Hello world!'

# Import the public key from a file
with open('public_key.pem', 'rb') as f:
    key_data = f.read()
key = RSA.import_key(key_data)
print("key:", key)

# Create a new PKCS1_OAEP cipher object with the public key
cipher = PKCS1_OAEP.new(key, SHA256)   #cipher = PKCS1_OAEP.new(key, SHA1)
print("cipher:", cipher)

# Encrypt the message using the cipher object
ciphertext = cipher.encrypt(message)
print("ciphertext:", ciphertext,"\n")

# Import the private key from a file
with open('private_key.pem', 'rb') as f:
    key_data = f.read()
key = RSA.import_key(key_data)
print("key:", key)

# Create a new PKCS1_OAEP cipher object with the private key
cipher = PKCS1_OAEP.new(key, SHA256)
print("cipher:", cipher)

# Decrypt the ciphertext using the cipher object
plaintext = cipher.decrypt(ciphertext)
print("plaintext:", plaintext)


