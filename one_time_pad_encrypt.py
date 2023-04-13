def one_time_pad_encrypt(plaintext, key):
    # Convert the plaintext and key to binary strings
    plaintext_binary = ''.join(format(ord(c), '08b') for c in plaintext)
    key_binary = ''.join(format(ord(c), '08b') for c in key)

    # Initialize an empty result binary string
    result_binary = ""

    # Loop through each character in the plaintext_binary string
    for i in range(len(plaintext_binary)):
        # XOR each character in the plaintext_binary string with the corresponding character in the key_binary string
        result_binary += str(int(plaintext_binary[i]) ^ int(key_binary[i]))
        print(i+1, "bit", int(plaintext_binary[i]), "XOR", int(key_binary[i % len(key_binary)]), "=", int(plaintext_binary[i]) ^ int(key_binary[i % len(key_binary)]))
   
   # Convert the result_binary string back to a string of characters
    result = ''.join(chr(int(result_binary[i:i+8], 2)) for i in range(0, len(result_binary), 8))
    return result


def one_time_pad_decrypt(ciphertext, key):
    # Convert the ciphertext and key to binary strings
    ciphertext_binary = ''.join(format(ord(c), '08b') for c in ciphertext)
    key_binary = ''.join(format(ord(c), '08b') for c in key)

    # Initialize an empty result binary string
    result_binary = ""

    # Loop through each character in the ciphertext_binary string
    for i in range(len(ciphertext_binary)):
        # XOR each character in the ciphertext_binary string with the corresponding character in the key_binary string
        result_binary += str(int(ciphertext_binary[i]) ^ int(key_binary[i]))
        print(i+1, "bit", int(ciphertext_binary[i]), "XOR",int(key_binary[i % len(key_binary)]), "=", int(ciphertext_binary[i]) ^ int(key_binary[i % len(key_binary)]))
    # Convert the result_binary string back to a string of characters
    result = ''.join(chr(int(result_binary[i:i+8], 2)) for i in range(0, len(result_binary), 8))
    return result


plaintext = "hello world"
key = "hello hello1qeqwe"

ciphertext = one_time_pad_encrypt(plaintext, key)
print("Ciphertext:", ciphertext)

decrypted_plaintext = one_time_pad_decrypt(ciphertext, key)
print("Decrypted plaintext:", decrypted_plaintext)
