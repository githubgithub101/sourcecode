from Crypto.PublicKey import RSA

# Generate an RSA key pair
key = RSA.generate(2024)
print(f"key: {key}")
print(f"first prime factor: {key.p}")  # Prints the first prime factor
print(f"\nsecond prime factor: {key.q}")  # Prints the second prime factor
print(f"\nkey product of two large prime numbers: {key.n}\n")  # key product of two large prime numbers used to generate the RSA key pair.


with open('private_key.pem', 'wb') as f:
    f.write(key.export_key('PEM'))

with open('public_key.pem', 'wb') as f:
    f.write(key.publickey().export_key('PEM'))
