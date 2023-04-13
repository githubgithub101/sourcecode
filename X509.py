from OpenSSL import crypto

# Load the certificate from a file
with open('certificate.pem', 'rb') as f:
    cert_data = f.read()
cert = crypto.load_certificate(crypto.FILETYPE_PEM, cert_data)

# Get the certificate subject and issuer names
subject = cert.get_subject()
issuer = cert.get_issuer()

# Verify the certificate against a trusted root certificate
trusted_cert_data = b'-----BEGIN CERTIFICATE-----\n...\n-----END CERTIFICATE-----\n'
trusted_cert = crypto.load_certificate(crypto.FILETYPE_PEM, trusted_cert_data)
store = crypto.X509Store()
store.add_cert(trusted_cert)
store_ctx = crypto.X509StoreContext(store, cert)
store_ctx.verify_certificate()






