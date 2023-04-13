from OpenSSL import crypto

# Generate a new 2048-bit RSA key pair
key = crypto.PKey()
key.generate_key(crypto.TYPE_RSA, 2048)

# Print the private key in PEM format
print(crypto.dump_privatekey(crypto.FILETYPE_PEM, key).decode())

# Generate a new CSR
req = crypto.X509Req()
req.get_subject().CN = "example.com"
req.set_pubkey(key)
req.sign(key, "sha256")

# Print the CSR in PEM format
print(crypto.dump_certificate_request(crypto.FILETYPE_PEM, req).decode())
