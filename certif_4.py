from OpenSSL import crypto

# Load the root CA certificate
with open("root_ca.pem", "rb") as f:
    root_ca_data = f.read()
root_ca = crypto.load_certificate(crypto.FILETYPE_PEM, root_ca_data)

# Load the intermediate CA certificate
with open("intermediate_ca.pem", "rb") as f:
    intermediate_ca_data = f.read()
intermediate_ca = crypto.load_certificate(crypto.FILETYPE_PEM, intermediate_ca_data)

# Load the end-entity certificate
with open("end_entity.pem", "rb") as f:
    end_entity_data = f.read()
end_entity = crypto.load_certificate(crypto.FILETYPE_PEM, end_entity_data)

# Verify the certificate chain
store = crypto.X509Store()
store.add_cert(root_ca)
store.add_cert(intermediate_ca)
store_ctx = crypto.X509StoreContext(store, end_entity)
store_ctx.verify_certificate()
