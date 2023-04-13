from cryptography import x509
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

# Load the certificate from a file
with open('certificate.pem', 'rb') as f:
    cert_data = f.read()
cert = x509.load_pem_x509_certificate(cert_data)

# Get the certificate subject and issuer names
subject = cert.subject.get_attributes_for_oid(x509.NameOID.COMMON_NAME)[0].value
issuer = cert.issuer.get_attributes_for_oid(x509.NameOID.COMMON_NAME)[0].value

# Verify the certificate against a trusted root certificate
trusted_cert_data = b'-----BEGIN CERTIFICATE-----\n...\n-----END CERTIFICATE-----\n'
trusted_cert = x509.load_pem_x509_certificate(trusted_cert_data)
cert.public_key().verify(trusted_cert.signature, cert.tbs_certificate_bytes, cert.signature_algorithm)
