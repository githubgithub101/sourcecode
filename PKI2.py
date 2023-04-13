from Crypto.PublicKey import RSA

# Generate a new private/public key pair
key = RSA.generate(2048)
print(f"key: {key}")
print(f"first prime factor: {key.p}")  # Prints the first prime factor
print(f"\nsecond prime factor: {key.q}")  # Prints the second prime factor
print(f"\nkey product of two large prime numbers: {key.n}\n")  # key product of two large prime numbers used to generate the RSA key pair.

# Export the private key in PEM format
private_key = key.export_key()
print(private_key.decode())

with open('private_key.pem', 'wb') as f:
    f.write(private_key)

# Export the public key in PEM format
public_key = key.publickey().export_key()
with open('public_key.pem', 'wb') as f:
    f.write(public_key)
print("\n",public_key.decode())






# pip uninstall crypto
# pip uninstall pycryptodome
# pip install pycryptodome





