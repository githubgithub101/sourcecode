# Encryption function
def encrypt_caesar(plaintext, key):
    # Initialize an empty string for the ciphertext
    ciphertext = ""
    # Iterate through each character in the plaintext
    for char in plaintext:
        # Check if the character is a letter
        if char.isalpha():
            # Shift the ASCII value of the letter by the key value
            shifted = ord(char) + key
            # Check if the shifted value is outside the range of uppercase or lowercase letters
            if char.isupper():
                if shifted > ord('Z'):
                    shifted -= 26
                elif shifted < ord('A'):
                    shifted += 26
            else:
                if shifted > ord('z'):
                    shifted -= 26
                elif shifted < ord('a'):
                    shifted += 26
            # Add the shifted letter to the ciphertext
            ciphertext += chr(shifted)
        else:
            # Add non-letter characters to the ciphertext without modification
            ciphertext += char
    # Return the encrypted message
    return ciphertext

# Decryption function


def decrypt_caesar(ciphertext, key):
    # Call the encryption function with the negative key value
    return encrypt_caesar(ciphertext, -key)


str = "APPLIED CRYPTOGRAPHY"
shift = 19
enc = encrypt_caesar(str, shift)

print("encrypted:", enc)

print("decrypted:", decrypt_caesar(enc, 19))

# for shift in range(-25, 26):
#     print("Key:", shift, decrypt_caesar(enc, shift))
