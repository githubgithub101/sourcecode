import random

def caesar_cipher_random(plaintext, key_length, mode):
    ciphertext = ""
    for char in plaintext:
        shift = random.randint(0, key_length)
        if mode == "encrypt":
            shifted_char = chr((ord(char) + shift - 65) % 26 + 65)
        elif mode == "decrypt":
            shifted_char = chr((ord(char) - shift - 65) % 26 + 65)
        ciphertext += shifted_char
    return ciphertext

plaintext = "ALLAN"
key_length = 1

ciphertext = caesar_cipher_random(plaintext, key_length, "encrypt")
print("Encrypted message:", ciphertext)

decrypted_message = caesar_cipher_random(ciphertext, key_length, "decrypt")
print("Decrypted message:", decrypted_message)
