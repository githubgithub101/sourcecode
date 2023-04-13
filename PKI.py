from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes

# Load the public key from a file
with open('public_key.pem', 'rb') as f:
    file = f.read()
    public_key = serialization.load_pem_public_key(file)
    print(f"public_key\n\n {file.decode()}")

# Load the private key from a file
with open('private_key.pem', 'rb') as f:
    file = f.read()
    private_key = serialization.load_pem_private_key(file, password=None)
    print(f"private_key\n\n {file.decode()}")
    

# Encrypt data using the public key
data = b'This is some data to be encrypted'
ciphertext = public_key.encrypt(data, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
print(f"\nciphertext: {ciphertext}")


# Decrypt the ciphertext using the private key
plaintext = private_key.decrypt(ciphertext, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))

print(f"\nplaintext: {plaintext}")





