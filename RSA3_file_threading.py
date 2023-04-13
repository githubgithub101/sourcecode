import base64
from multiprocessing import pool
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
    print(f"len(plaintext) {len(plaintext)}")
    print(f"chunk_size {chunk_size}")

    iterr = []
    # for x in range(0, (len(plaintext)/chunk_size)/12, 12):
    for i in range(0, len(plaintext), chunk_size):
        val = plaintext[i:i+chunk_size]
        iterr.append(val)
        # ciphertext += cipher.encrypt(plaintext[i:i+chunk_size])


    inputs = [(iterr[i], key) for i in range(len(iterr))]
    output = pool.starmap(cipher.encrypt, inputs)

    pool.close()    # Close the Pool
    pool.join()     # Wait for all processes to finish

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
    # key = generate_key()

    # # Save RSA key to file
    # save_key(key, 'private_key.pem')
    # save_key(key.publickey(), 'public_key.pem')

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
    encrypt_image('image1.jpg', public_key)

    # # Decrypt image file
    # decrypt_image('image1.jpg.enc', private_key)

