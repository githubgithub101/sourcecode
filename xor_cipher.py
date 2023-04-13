def xor_cipher(text_binary, key_binary):
    # Initialize an empty result binary string
    result_binary = ""

    # Loop through each character in the text_binary string
    for i in range(len(text_binary)):
        # XOR each character in the text_binary string with the corresponding character in the key_binary string
        result_binary += str(int(text_binary[i]) ^ int(key_binary[i % len(key_binary)]))
        # print(i+1, "bit", int(text_binary[i]), "XOR", int(key_binary[i % len(key_binary)]), "=", int(text_binary[i]) ^ int(key_binary[i % len(key_binary)]))

    # Convert the result_binary string back to a string of characters
    result = ''.join(chr(int(result_binary[i:i+8], 2)) for i in range(0, len(result_binary), 8))
    print("Encrypted:",' '.join(result_binary[i:i+8] for i in range(0, len(result_binary), 8)))
    return result


# text = "HelLOW0rld"
# key = "p4s$5w0Rdd"

text = "pOwerd0pLe"
key = "WeHe$Ow"


# Convert the text and key to binary strings
print("text:", text)
print("key:", key)
text_binary = ''.join(format(ord(c), '08b') for c in text)
key_binary = ''.join(format(ord(c), '08b') for c in key)
print("text_binary:", ''.join(text_binary[i:i+8] for i in range(0, len(text_binary), 8)), "\nkey_binary:", ''.join(key_binary[i:i+8] for i in range(0, len(key_binary), 8)))

encrypted = xor_cipher(text_binary, key_binary)
print(encrypted)

encrypted = ''.join(format(ord(c), '08b') for c in encrypted)
decrypted = xor_cipher(encrypted, key_binary)
print(decrypted)


