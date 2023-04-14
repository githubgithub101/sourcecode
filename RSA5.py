# RSA Key Generation

from Crypto.PublicKey import RSA
keyPair = RSA.generate(2024)

pubKey = keyPair.publickey()
# print(f"Public key:  (n={hex(pubKey.n)}, e={hex(pubKey.e)})")
pubKeyPEM = pubKey.exportKey()
print(pubKeyPEM.decode('ascii'))

# print(f"Private key: (n={hex(pubKey.n)}, d={hex(keyPair.d)})")
privKeyPEM = keyPair.exportKey()
print(privKeyPEM.decode('ascii'))


# RSA Encryption
from Crypto.Cipher import PKCS1_OAEP
import binascii

msg = b'A message for encryption'
encryptor = PKCS1_OAEP.new(pubKey)
encrypted = encryptor.encrypt(msg)
print("Encrypted:", binascii.hexlify(encrypted))
print("Encrypted:", encrypted)


# RSA Decryption
from Crypto.Cipher import PKCS1_OAEP
decryptor = PKCS1_OAEP.new(keyPair)
decrypted = decryptor.decrypt(encrypted)
print('Decrypted:', decrypted)