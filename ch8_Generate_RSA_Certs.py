#ch8_Generate_RSA_Certs.py
from Crypto.PublicKey import RSA

# Generate a new RSA key pair with 4096 bits (512 bytes) and public exponent 65537
new_key = RSA.generate(4096, e=65537)

# Export the private key in PEM format
private_key = new_key.exportKey("PEM")

# Export the public key in PEM format
public_key = new_key.publickey().exportKey("PEM")

# Print the private key and write it to a file named private_key.pem
print(private_key)
with open("private_key.pem", "wb") as f:
    f.write(private_key)

# Print the public key and write it to a file named public_key.pem
print(public_key)
with open("public_key.pem", "wb") as f:
    f.write(public_key)
