from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Cipher import PKCS1_OAEP



def openfile(path):
    fin = open(path, 'rb') # open file for reading purpose
    file = fin.read() # storing file data in variable "file"
    fin.close()
    file = bytearray(file) # converting file into byte array
    return file

if __name__ == '__main__':
    with open('private_key.pem', 'rb') as f:
        private_key = RSA.import_key(f.read())

    with open('public_key.pem', 'rb') as f:
        public_key = RSA.import_key(f.read())

    # Choose a plaintext message to encrypt

    plaintext = openfile("image1.jpg")
    print(plaintext)
    # plaintext = b'This is a secret message!'

    # Encrypt the message using the RSA public key
    cipher = PKCS1_OAEP.new(public_key, SHA256)
    ciphertext = cipher.encrypt(plaintext)
    print(f"RSA public key: {public_key.export_key().decode()}")

    # Decrypt the ciphertext using the RSA private key
    cipher = PKCS1_OAEP.new(private_key, SHA256)
    decrypted_plaintext = cipher.decrypt(ciphertext)
    print(f"RSA private key: {private_key.export_key().decode()}")

    fin = open("image1.jpg.Renc", 'wb') # opening file for writing purpose
    fin.write(ciphertext) # writing encrypted data in file
    fin.close()

    print(f"\nciphertext: {ciphertext.hex()}")

    file = openfile("image1.jpg.Renc")
    print(f"\ndecrypted_plaintext: {decrypted_plaintext.decode()}")

    fin = open("DECE_RSA_image1.jpg", 'wb')
    fin.write(decrypted_plaintext)  # writing decryption data in file
    fin.close()

    # Verify that the decrypted plaintext matches the original message
    print(f"successfully decrypted? {decrypted_plaintext == plaintext}")  # Should print True
