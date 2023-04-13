from OpenSSL import crypto
import datetime

# Generate a new 2048-bit RSA key pair
key = crypto.PKey()
key.generate_key(crypto.TYPE_RSA, 2048)

# Print the private key in PEM format
print(crypto.dump_privatekey(crypto.FILETYPE_PEM, key).decode())

# Generate a new self-signed certificate
cert = crypto.X509()
cert.get_subject().CN = "example.com"
cert.set_serial_number(1000)
cert.gmtime_adj_notBefore(0)
cert.gmtime_adj_notAfter(365*24*60*60)
cert.set_issuer(cert.get_subject())
cert.set_pubkey(key)
cert.sign(key, "sha256")

# Print the certificate in PEM format
print(crypto.dump_certificate(crypto.FILETYPE_PEM, cert).decode())
