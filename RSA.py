


# from cryptography.hazmat.primitives.asymmetric import rsa, padding
# from cryptography.hazmat.primitives import serialization, hashes

# # Generate an RSA key pair
# private_key = rsa.generate_private_key(
#     public_exponent=65537,          # Choose a public exponent for the key pair
#     key_size=4096                   # Choose a key size for the key pair
# )

# public_key = private_key.public_key()       # Get the corresponding public key from the private key

# # Convert the keys to PEM format for storage
# private_key_pem = private_key.private_bytes(
#     encoding=serialization.Encoding.PEM,                # Choose the encoding format for the private key
#     format=serialization.PrivateFormat.PKCS8,           # Choose the format for the private key
#     encryption_algorithm=serialization.NoEncryption()   # Choose the encryption algorithm for the private key
# )

# print("private_key_pem:\n",private_key_pem,"\n\n")

# public_key_pem = public_key.public_bytes(
#     encoding=serialization.Encoding.PEM,                    # Choose the encoding format for the public key
#     format=serialization.PublicFormat.SubjectPublicKeyInfo  # Choose the format for the public key
# )

# print("public_key_pem:\n",public_key_pem,"\n\n")

# # Encrypt a message using the public key
# message = b'Hello world!'                              # Define the message to be encrypted
# encrypted_message = public_key.encrypt(
#     message,                                            # Choose the message to be encrypted
#     padding.OAEP(
#         mgf=padding.MGF1(algorithm=hashes.SHA256()),    # Choose the mask generation function for the padding scheme
#         algorithm=hashes.SHA256(),                      # Choose the hash algorithm for the padding scheme
#         label=None                                      # Choose the label for the padding scheme (can be None)
#     )
# )
# print('Encrypted message:\n', encrypted_message) # Print the encrypted message


# # Decrypt the message using the private key
# decrypted_message = private_key.decrypt(
#     encrypted_message,                                  # Choose the message to be decrypted
#     padding.OAEP(
#         mgf=padding.MGF1(algorithm=hashes.SHA256()),    # Choose the mask generation function for the padding scheme
#         algorithm=hashes.SHA256(),                      # Choose the hash algorithm for the padding scheme
#         label=None                                      # Choose the label for the padding scheme (can be None)
#     )
# )
# print('\nDecrypted message:', decrypted_message.decode())        # Print the decrypted message








from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Cipher import PKCS1_OAEP




with open('private_key.pem', 'rb') as f:
    private_key = RSA.import_key(f.read())

with open('public_key.pem', 'rb') as f:
    public_key = RSA.import_key(f.read())


# Choose a plaintext message to encrypt
plaintext = b'This is a secret message!'

# Encrypt the message using the RSA public key
cipher = PKCS1_OAEP.new(public_key, SHA256)
ciphertext = cipher.encrypt(plaintext)
print(f"RSA public key: {public_key.export_key().decode()}")

# Decrypt the ciphertext using the RSA private key
cipher = PKCS1_OAEP.new(private_key, SHA256)
decrypted_plaintext = cipher.decrypt(ciphertext)
print(f"RSA private key: {private_key.export_key().decode()}")

print(f"\nciphertext: {ciphertext.hex()}")
print(f"\ndecrypted_plaintext: {decrypted_plaintext.decode()}")

# Verify that the decrypted plaintext matches the original message
print(f"successfully decrypted? {decrypted_plaintext == plaintext}")  # Should print True
