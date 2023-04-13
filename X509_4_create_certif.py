from OpenSSL import crypto
import datetime

# create a new key pair
k = crypto.PKey()
k.generate_key(crypto.TYPE_RSA, 2048)

# create a self-signed certificate
cert = crypto.X509()
cert.get_subject().C = "US"
cert.get_subject().ST = "California"
cert.get_subject().L = "San Francisco"
cert.get_subject().O = "Example Company"
cert.get_subject().CN = "example.com"
cert.set_serial_number(1000)
cert.gmtime_adj_notBefore(0)
cert.gmtime_adj_notAfter(365*24*60*60)
cert.set_issuer(cert.get_subject())
cert.set_pubkey(k)
cert.sign(k, 'sha256')

# write the certificate to a file
with open('certificate.pem', 'wb') as f:
    f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
