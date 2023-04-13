def get_key_path():
    # take path of file as a input
    path = input('Enter path of file : ')
	
    # taking encryption key as input
    key = input('Enter Key for encryption of file : ')
    key = int(''.join([str(ord(i)) for i in key]))
    return path, key


def xor_cipher(text_binary, key_binary):
    # Initialize an empty result binary string
    result_binary = ""

    # Loop through each character in the text_binary string
    for i in range(len(text_binary)):
        # XOR each character in the text_binary string with the corresponding character in the key_binary string
        result_binary += str(int(text_binary[i]) ^ int(key_binary[i % len(key_binary)]))
    # Convert the result_binary string back to a string of characters
    result_bin = ''.join(result_binary[i:i+8] for i in range(0, len(result_binary), 8))
    result_bytes = bytearray(int(result_bin[i:i+8], 2) for i in range(0, len(result_bin), 8))
    return result_bin, result_bytes


def XOR_encryption(path, key):
        # try block to handle exception
    try:
        # open file for reading purpose
        fin = open(path, 'rb')
        
        # storing file data in variable "file"
        file = fin.read()
        fin.close()
        
        # converting file into byte array to
        # perform encryption easily on numeric data
        file = bytearray(file)

        val1 = ''.join(format(ord(chr(c)), '08b') for c in file)
        val2 = bin(int(key))[2:]

        XOR_val = xor_cipher(val1, val2)
        
        # print(val1)
        # print(val2)
        print(XOR_val[0])

        file = XOR_val[1]

        # opening file for writing purpose
        fin = open(path + '.enc', 'wb')
        
        # writing encrypted data in file
        fin.write(file)
        fin.close()
        print('Encryption Done...')
        # Save encrypted file to file
    except Exception as e:
        print('Error caught : ', type(e).__name__)



def XOR_decryption(path, key):
    # try block to handle the exception
    try:
        # open file for reading purpose
        fin = open(path, 'rb')
        
        # storing file data in variable "file"
        file = fin.read()
        fin.close()
        
        # converting file into byte array to perform decryption easily on numeric data
        file = bytearray(file)

        val1 = ''.join(format(ord(chr(c)), '08b') for c in file)
        val2 = bin(int(key))[2:]
        XOR_val = xor_cipher(val1, val2)

        # print(val1)
        # print(val2)
        # print(XOR_val[0])

        file = XOR_val[1]

        fin = open('decrypted_' + path[:-4], 'wb')
        
        # writing decryption data in file
        fin.write(file)
        fin.close()
        print('Decryption Done...')
    except Exception:
        print('Error caught : ', Exception.__name__)


if __name__ == '__main__':
    while True:
        try:
            select =int(input("1 Encryption\n2 Decryption\n3 Exit\n"))
            if select == 1:
                path,key = get_key_path()
                XOR_encryption(path, key)
            elif select == 2:
                path,key = get_key_path()
                XOR_decryption(path, key)
            elif select == 3:
                break
            else:
                print("error selection")
        except ValueError:
            print("Just select between 1 2 and 3")
        finally:
             print("----------------")


