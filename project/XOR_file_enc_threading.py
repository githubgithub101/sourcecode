import multiprocessing

def bins_to_bytes(bins):
    return bytearray(int(bins[i:i+8], 2) for i in range(0, len(bins), 8))

def char_to_bin(file):
    return ''.join(format(ord(chr(c)), '08b') for c in file)  #converts file to bin

def get_cpu_count():
    return multiprocessing.cpu_count()

def get_pool_size(num_of_workers):
    return multiprocessing.Pool(num_of_workers)

def openfile(path):
    file = bytearray(path) # converting file into byte array
    return file

def xor_cipher(text_binary, key_binary):
    result_binary = ""                  # Initialize an empty result binary string
    for i in range(len(text_binary)):   # Loop through each character in the text_binary string
        # XOR each character in the text_binary string with the corresponding character in the key_binary string
        result_binary += str(int(text_binary[i]) ^ int(key_binary[i % len(key_binary)]))
    # Convert the result_binary string back to a string of characters
    result_bin = ''.join(result_binary[i:i+8] for i in range(0, len(result_binary), 8))
    return result_bin

def xor_worker(file, key):
        num_of_workers = get_cpu_count()  # number of CPU or workers
        pool = get_pool_size(num_of_workers)
        # print(f"Processing by {num_of_workers} CPUs...")
        file = char_to_bin(file)
        key = bin(int(key))[2:]
        bit_len = int(len(file))
        div_by_workers = int(bit_len/num_of_workers)

        # print(bit_len)
        # print(div_by_workers)
        
        bits_list = []
        count = 0
        for i in range(0, bit_len, div_by_workers):
            bits_substring = file[count : i + div_by_workers]
            count += div_by_workers
            bits_list.append(bits_substring)

        inputs = [(bits_list[i], key) for i in range(len(bits_list))]
        output = pool.starmap(xor_cipher, inputs)
        

        pool.close()    # Close the Pool
        pool.join()     # Wait for all processes to finish
        return output

def XOR_encryption(path, key):
        # try block to handle exception
    try:
        file = openfile(path)
        file = bins_to_bytes(''.join(xor_worker(file, key))) # Extract the results from the list of tuples
        return file
    except Exception as e:
        print('Error caught : ', type(e).__name__)


def XOR_decryption(path, key):
    # try block to handle the exception
    try:
        file = openfile(path)
        file = bins_to_bytes(''.join(xor_worker(file, key)))
        return file
    except Exception:
        print('Error caught : ', Exception.__name__)