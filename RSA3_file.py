import base64
import zlib
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

def generate_key():
    """Generate RSA key pair"""
    key = RSA.generate(4096)
    return key

def save_key(key, filename):
    """Save RSA key to file"""
    with open(filename, 'wb') as f:
        f.write(key.export_key('PEM'))

def load_key(filename):
    """Load RSA key from file"""
    with open(filename, 'rb') as f:
        key = f.read()
    return key

def encrypt_image(image_file, key):
    """Encrypt image using RSA encryption"""
    # Generate cipher
    cipher = RSA.importKey(key)
    cipher = PKCS1_OAEP.new(cipher)



    # Read image file
    with open(image_file, 'rb') as f:
        plaintext = f.read()
    

    plaintext = zlib.compress(plaintext)  #######


    # Encrypt image data
    # chunk_size = abs(get_chunk_size(key.size_in_bytes(), 33))
    # chunk_size = abs(get_chunk_size(512, 33))
    chunk_size = 470
    ciphertext = b''
    print(chunk_size)
    for i in range(0, len(plaintext), chunk_size):
        ciphertext += cipher.encrypt(plaintext[i:i+chunk_size])
    
    # Save encrypted image to file
    with open(image_file + '.enc', 'wb') as f:
        # f.write(ciphertext)
        f.write(base64.b64encode(ciphertext))
        

def decrypt_image(encrypted_file, key):
    """Decrypt image using RSA decryption"""
    # Generate cipher
    cipher = RSA.importKey(key)
    cipher = PKCS1_OAEP.new(cipher)


    # Read encrypted image file
    with open(encrypted_file, 'rb') as f:
        ciphertext = f.read()
    
    #Base 64 decode the data
    ciphertext = base64.b64decode(ciphertext)


    # Decrypt image data
    # chunk_size = key.size_in_bytes()
    chunk_size = 512
    plaintext = b''
    for i in range(0, len(ciphertext), chunk_size):
        plaintext += cipher.decrypt(ciphertext[i:i+chunk_size])

    # Save decrypted image to file
    with open('decrypted_' + encrypted_file[:-4], 'wb') as f:
        # f.write(plaintext)
        f.write(zlib.decompress(plaintext))
        

def get_chunk_size(key_size, padding_overhead):
    """Calculate chunk size"""
    key_size_bytes = (key_size + 7) // 8
    return key_size_bytes - padding_overhead

if __name__ == '__main__':
    # Generate RSA key pair
    key = generate_key()

    # Save RSA key to file
    save_key(key, 'private_key.pem')
    save_key(key.publickey(), 'public_key.pem')

    # Load RSA key from file
    private_key = load_key('private_key.pem')
    public_key = load_key('public_key.pem')

    # print(f"e: {key.e} \n\n")
    # print(f"t: {(key.p - 1) * (key.q - 1)} \n\n")
    # print(f"d: {key.d} \n\n")
    # print(f"n: {key.n} \n\n")
    # print(f"p: {key.p} \n\n")
    # print(f"q: {key.q} \n\n")

    # print(key.size_in_bytes())

    # Encrypt image file
    # encrypt_image('imageCopy.jpg', public_key)

    # Decrypt image file
    # decrypt_image('imageCopy.jpg.enc', private_key)












#ch9_generate_keys.py
# from Crypto.PublicKey import RSA
# from Crypto.Hash import SHA1
# from Crypto.Cipher import PKCS1_OAEP
# import zlib
# import base64


# #Generate a public/ private key pair using 4096 bits key length (512 bytes)
# new_key = RSA.generate(4096, e=65537)

# #The private key in PEM format
# private_key = new_key.exportKey("PEM")

# #The public key in PEM Format
# public_key = new_key.publickey().exportKey("PEM")

# print(private_key)
# fd = open("private_key.pem", "wb")
# fd.write(private_key)
# fd.close()

# print(public_key)
# fd = open("public_key.pem", "wb")
# fd.write(public_key)
# fd.close()


#ch9_encrypt_blob.py
# #Our Encryption Function
# def encrypt_blob(blob, public_key):
#     #Import the Public Key and use for encryption using PKCS1_OAEP
#     rsa_key = RSA.importKey(public_key)
#     rsa_key = PKCS1_OAEP.new(rsa_key,hashAlgo=SHA1)

#     #compress the data first
#     blob = zlib.compress(blob)

#     #In determining the chunk size, determine the private key length used in bytes
#     #and subtract 42 bytes (when using PKCS1_OAEP). The data will be in encrypted
#     #in chunks
#     chunk_size = 470
#     offset = 0
#     end_loop = False
#     encrypted =  b""
#     print(len(blob))
#     print(f"len blob {len(blob)}")
#     while not end_loop:
#         #The chunk
#         chunk = blob[offset:offset + chunk_size]

#         #If the data chunk is less then the chunk size, then we need to add
#         #padding with " ". This indicates the we reached the end of the file
#         #so we end loop here
#         if len(chunk) % chunk_size != 0:
#             end_loop = True
#             chunk += b" " * (chunk_size - len(chunk))

#         #Append the encrypted chunk to the overall encrypted file
#         encrypted += rsa_key.encrypt(chunk)

#         #Increase the offset by chunk size
#         offset += chunk_size

#     #Base 64 encode the encrypted file
#     return base64.b64encode(encrypted)


# #ch9_decrypt_blob.py
# #Our Decryption Function
# def decrypt_blob(encrypted_blob, private_key):

#     #Import the Private Key and use for decryption using PKCS1_OAEP
#     rsakey = RSA.importKey(private_key)
#     rsakey = PKCS1_OAEP.new(rsakey, hashAlgo=SHA1)

#     #Base 64 decode the data
#     encrypted_blob = base64.b64decode(encrypted_blob)

#     #In determining the chunk size, determine the private key length used in bytes.
#     #The data will be in decrypted in chunks
#     print(f"len {len(private_key)}")

#     chunk_size = 512
#     offset = 0
#     decrypted = b""

#     #keep loop going as long as we have chunks to decrypt
#     while offset < len(encrypted_blob):
#         #The chunk
#         chunk = encrypted_blob[offset: offset + chunk_size]

#         #Append the decrypted chunk to the overall decrypted file
#         decrypted += rsakey.decrypt(chunk)

#         #Increase the offset by chunk size
#         offset += chunk_size
#     #return the decompressed decrypted data
#     return zlib.decompress(decrypted)


# #####################

# #Use the public key for encryption
# fd = open("public_key.pem", "rb")
# public_key = fd.read()
# fd.close()

# #Our candidate file to be encrypted
# fd = open("image.jpg", "rb")
# unencrypted_blob = fd.read()
# fd.close()
# print(f"unencrypted_blob {len(unencrypted_blob)}")
# encrypted_blob = encrypt_blob(unencrypted_blob, public_key)

# #Write the encrypted contents to a file
# fd = open("image.enc", "wb")
# fd.write(encrypted_blob)
# fd.close()


#####################


# #Use the private key for decryption
# fd = open("private_key.pem", "rb")
# private_key = fd.read()
# fd.close()

# #Our candidate file to be decrypted
# fd = open("image.enc", "rb")
# encrypted_blob = fd.read()
# fd.close()

# #Write the decrypted contents to a file
# fd = open("image.jpg", "wb")
# fd.write(decrypt_blob(encrypted_blob, private_key))
# fd.close()






















# from Crypto.Cipher import PKCS1_OAEP
# from Crypto.PublicKey import RSA

# # Generate a new RSA key pair
# key = RSA.generate(2048)

# # Save the public and private keys to files
# with open('public.pem', 'wb') as f:
#     f.write(key.publickey().export_key())

# with open('private.pem', 'wb') as f:
#     f.write(key.export_key())

# def encrypt_file(input_file_path, output_file_path, public_key_path):
#     # Load the public key from disk
#     with open(public_key_path, 'rb') as f:
#         public_key = RSA.import_key(f.read())

#     # Create a new RSA cipher using the public key
#     cipher = PKCS1_OAEP.new(public_key)

#     # Open the input and output files
#     with open(input_file_path, 'rb') as input_file, open(output_file_path, 'wb') as output_file:
#         # Encrypt the file in chunks and write the encrypted chunks to the output file
#         while True:
#             chunk = input_file.read(50)
#             if len(chunk) == 0:
#                 break
#             encrypted_chunk = cipher.encrypt(chunk)
#             output_file.write(encrypted_chunk)

# def decrypt_file(input_file_path, output_file_path, private_key_path):
#     # Load the private key from disk
#     with open(private_key_path, 'rb') as f:
#         private_key = RSA.import_key(f.read())

#     # Create a new RSA cipher using the private key
#     cipher = PKCS1_OAEP.new(private_key)

#     # Open the input and output files
#     with open(input_file_path, 'rb') as input_file, open(output_file_path, 'wb') as output_file:
#         # Decrypt the file in chunks and write the decrypted chunks to the output file
#         while True:
#             chunk = input_file.read(50)
#             if len(chunk) == 0:
#                 break
#             decrypted_chunk = cipher.decrypt(chunk)
#             output_file.write(decrypted_chunk)

# # Example usage
# input_file_path = 'sample.jpg'
# encrypted_file_path = 'sample.enc'
# decrypted_file_path = 'decrypted_sample.jpg'

# # Encrypt the input file using the public key
# public_key_path = 'public.pem'
# encrypt_file(input_file_path, encrypted_file_path, public_key_path)

# # Decrypt the encrypted file using the private key
# private_key_path = 'private.pem'
# decrypt_file(encrypted_file_path, decrypted_file_path, private_key_path)























# import binascii
# from Crypto.PublicKey import RSA
# from Crypto.Cipher import PKCS1_OAEP
# import os

# def encrypt_file(file_path, public_key_path):
#     chunk_size = 50
#     encrypted_chunks = []

#     with open(file_path, 'rb') as f:
#         data = f.read()
#     # print(binascii.hexlify(data))
#     with open(public_key_path, 'rb') as f:
#         public_key = RSA.import_key(f.read())
    
#     cipher = PKCS1_OAEP.new(public_key)
    
#     for i in range(0, len(data), chunk_size):
#         chunk = data[i:i+chunk_size]
#         encrypted_chunk = cipher.encrypt(chunk)
#         encrypted_chunks.append(encrypted_chunk)

#     # encrypted_data = cipher.encrypt(data)
#     ciphertext = b''.join(encrypted_chunks)
#     with open(file_path + '.enc', 'wb') as f:
#         f.write(ciphertext)

# def decrypt_file(file_path, private_key_path):
#     chunk_size = 50
#     derypted_chunks = []

#     with open(file_path, 'rb') as f:
#         data = f.read()

#     with open(private_key_path, 'rb') as f:
#         private_key = RSA.import_key(f.read())

#     cipher = PKCS1_OAEP.new(private_key)

#     for i in range(0, len(data), chunk_size):
#         chunk = data[i:i+chunk_size]
#         derypted_chunk = cipher.decrypt(chunk)
#         derypted_chunks.append(derypted_chunk)

#     # decrypted_data = cipher.decrypt(data)
#     decrypted_data = b''.join(derypted_chunks)

#     with open(os.path.splitext(file_path)[0], 'wb') as f:
#         f.write(decrypted_data)

# public_key_path = 'public.pem'
# private_key_path = 'private.pem'
# file_path = 'sample.jpg'

# # Generate keys if they don't exist
# if not os.path.isfile(public_key_path) or not os.path.isfile(private_key_path):
#     key = RSA.generate(3072)
#     private_key = key.export_key()
#     public_key = key.publickey().export_key()

#     with open(private_key_path, 'wb') as f:
#         f.write(private_key)

#     with open(public_key_path, 'wb') as f:
#         f.write(public_key)

# # encrypt_file(file_path, public_key_path)
# decrypt_file(file_path + '.enc', private_key_path)














# from Crypto.PublicKey import RSA
# from Crypto.Cipher import PKCS1_OAEP
# import os

# def generate_key_pair():
#     """
#     Generates a new RSA key pair and saves it to disk.
#     """
#     key = RSA.generate(2048)
#     private_key = key.export_key()
#     with open('private.pem', 'wb') as f:
#         f.write(private_key)

#     public_key = key.publickey().export_key()
#     with open('public.pem', 'wb') as f:
#         f.write(public_key)

# def encrypt_file(input_file, output_file, public_key_path):
#     """
#     Encrypts a file using RSA encryption.
#     """
#     with open(public_key_path, 'rb') as f:
#         public_key = RSA.import_key(f.read())

#     cipher = PKCS1_OAEP.new(public_key)

#     # Read the input file in chunks to conserve memory
#     chunk_size = 256
#     with open(input_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
#         while True:
#             chunk = f_in.read(chunk_size)
#             if len(chunk) == 0:
#                 break
#             encrypted_chunk = cipher.encrypt(chunk)
#             f_out.write(encrypted_chunk)

#     print(f'Encrypted file saved to {output_file}')

# def decrypt_file(input_file, output_file, private_key_path):
#     """
#     Decrypts a file using RSA decryption.
#     """
#     with open(private_key_path, 'rb') as f:
#         private_key = RSA.import_key(f.read())

#     cipher = PKCS1_OAEP.new(private_key)

#     # Read the input file in chunks to conserve memory
#     chunk_size = 256
#     with open(input_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
#         while True:
#             chunk = f_in.read(chunk_size)
#             if len(chunk) == 0:
#                 break
#             decrypted_chunk = cipher.decrypt(chunk)
#             f_out.write(decrypted_chunk)

#     print(f'Decrypted file saved to {output_file}')

# # Example usage
# input_file = 'sample.jpg'
# encrypted_file = 'sample.enc'
# decrypted_file = 'decrypted_filesample.jpg'
# public_key_path = 'public.pem'
# private_key_path = 'private.pem'

# # Generate key pair if it doesn't exist
# if not os.path.exists(public_key_path) or not os.path.exists(private_key_path):
#     generate_key_pair()

# # Encrypt the input file
# encrypt_file(input_file, encrypted_file, public_key_path)

# # Decrypt the encrypted file
# decrypt_file(encrypted_file, decrypted_file, private_key_path)
