import multiprocessing
import os
import time

def bins_to_bytes(bins):
    return bytearray(int(bins[i:i+8], 2) for i in range(0, len(bins), 8))

def char_to_bin(file):
    return ''.join(format(ord(chr(c)), '08b') for c in file)  #converts file to bin

def get_key_path():
    path = input('Enter path of file : ')           # take path of file as a input
    key = input('Enter Key for encryption of file : ')  # taking encryption key as input
    key = int(''.join([str(ord(i)) for i in key]))
    return path, key

def get_cpu_count():
    return multiprocessing.cpu_count()

def get_pool_size(num_of_workers):
    return multiprocessing.Pool(num_of_workers)

def openfile(path):
    fin = open(path, 'rb') # open file for reading purpose
    file = fin.read() # storing file data in variable "file"
    fin.close()
    file = bytearray(file) # converting file into byte array
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
        print(f"Processing by {num_of_workers} CPUs...")
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
            time.sleep(0.1)  # Simulate some work being done

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
        fin = open(path + postfix, 'wb') # opening file for writing purpose
        fin.write(file) # writing encrypted data in file
        fin.close()
    except Exception as e:
        print('Error caught : ', type(e).__name__)


def XOR_decryption(path, key):
    # try block to handle the exception
    try:
        file = openfile(path)
        file = bins_to_bytes(''.join(xor_worker(file, key)))

        fin = open(prefix + path[:-4], 'wb')
        fin.write(file)  # writing decryption data in file
        fin.close()
    except Exception:
        print('Error caught : ', Exception.__name__)


if __name__ == '__main__':
    global prefix
    global postfix
    postfix = ".enc"
    prefix = "decrypted_"
    while True:
        try:
            select =int(input("1 Encryption\n2 Decryption\n3 Exit\n"))
            if select == 1:
                path,key = get_key_path()
                start_time = time.time()
                XOR_encryption(path, key)
                end_time = time.time()
                elapsed_time = end_time - start_time
                print('Encryption Done...')
                print("Elapsed time: {:.2f} seconds".format(elapsed_time))
            elif select == 2:
                path,key = get_key_path()
                start_time = time.time()
                XOR_decryption(path, key)
                end_time = time.time()
                elapsed_time = end_time - start_time
                print('Decryption Done...')
                print("Elapsed time: {:.2f} seconds".format(elapsed_time))
            elif select == 3:
                break
            else:
                print("error selection")
        except ValueError:
            print("Just select between 1 2 and 3")
        finally:
             print("----------------")





# import time

# def progress_bar(total, progress):
#     """Displays a simple progress bar.
    
#     Args:
#         total (int): Total number of iterations.
#         progress (int): Current progress.
#     """
#     bar_length = 30  # Length of the progress bar
#     filled_length = int(bar_length * progress / total)
#     bar = '█' * filled_length + '-' * (bar_length - filled_length)
#     percent = (progress / total) * 100
#     print(f'Progress: |{bar}| {percent:.1f}% Complete', end='\r')

# # Example usage:
# total_iterations = 100
# for i in range(total_iterations + 1):
#     progress_bar(total_iterations, i)
#     time.sleep(0.1)  # Simulate some work being done







# import multiprocessing
# import time

# def bins_to_bytes(bins):
#     return bytearray(int(bins[i:i+8], 2) for i in range(0, len(bins), 8))

# def char_to_bin(file):
#     return ''.join(format(ord(chr(c)), '08b') for c in file)  #converts file to bin

# def get_key_path():
#     path = input('Enter path of file : ')           # take path of file as a input
#     key = input('Enter Key for encryption of file : ')  # taking encryption key as input
#     key = int(''.join([str(ord(i)) for i in key]))
#     return path, key

# def get_cpu_count():
#     return multiprocessing.cpu_count()

# def get_pool_size(num_of_workers):
#     return multiprocessing.Pool(num_of_workers)

# def openfile(path):
#     fin = open(path, 'rb') # open file for reading purpose
#     file = fin.read() # storing file data in variable "file"
#     fin.close()
#     file = bytearray(file) # converting file into byte array
#     return file

# def xor_cipher(text_binary, key_binary):
#     result_binary = ""                  # Initialize an empty result binary string
#     for i in range(len(text_binary)):   # Loop through each character in the text_binary string
#         # XOR each character in the text_binary string with the corresponding character in the key_binary string
#         result_binary += str(int(text_binary[i]) ^ int(key_binary[i % len(key_binary)]))
#     # Convert the result_binary string back to a string of characters
#     result_bin = ''.join(result_binary[i:i+8] for i in range(0, len(result_binary), 8))
#     return result_bin

# def xor_worker(file, key):
#         num_of_workers = get_cpu_count()  # number of CPU or workers
#         pool = get_pool_size(num_of_workers)
#         print(f"Processing by {num_of_workers} CPUs...")
#         file = char_to_bin(file)
#         key = bin(int(key))[2:]
#         bit_len = int(len(file))
#         div_by_workers = int(bit_len/num_of_workers)

#         # print(bit_len)
#         # print(div_by_workers)
        
#         bits_list = []
#         count = 0
#         for i in range(0, bit_len, div_by_workers):
#             bits_substring = file[count : i + div_by_workers]
#             count += div_by_workers
#             bits_list.append(bits_substring)
#             time.sleep(0.1)  # Simulate some work being done

#         inputs = [(bits_list[i], key) for i in range(len(bits_list))]
#         output = pool.starmap(xor_cipher, inputs)

#         pool.close()    # Close the Pool
#         pool.join()     # Wait for all processes to finish
#         return output

# def XOR_encryption(path, key):
#         # try block to handle exception
#     try:
#         file = openfile(path)
#         file = bins_to_bytes(''.join(xor_worker(file, key))) # Extract the results from the list of tuples

#         fin = open(path + postfix, 'wb') # opening file for writing purpose
#         fin.write(file) # writing encrypted data in file
#         fin.close()
#     except Exception as e:
#         print('Error caught : ', type(e).__name__)


# def XOR_decryption(path, key):
#     # try block to handle the exception
#     try:
#         file = openfile(path)
#         file = bins_to_bytes(''.join(xor_worker(file, key)))

#         fin = open(prefix + path[:-4], 'wb')
#         fin.write(file)  # writing decryption data in file
#         fin.close()
#     except Exception:
#         print('Error caught : ', Exception.__name__)


# if __name__ == '__main__':
#     global prefix
#     global postfix
#     postfix = ".enc"
#     prefix = "decrypted_"
#     while True:
#         try:
#             select =int(input("1 Encryption\n2 Decryption\n3 Exit\n"))
#             if select == 1:
#                 path,key = get_key_path()
#                 start_time = time.time()
#                 XOR_encryption(path, key)
#                 end_time = time.time()
#                 elapsed_time = end_time - start_time
#                 print('Encryption Done...')
#                 print("Elapsed time: {:.2f} seconds".format(elapsed_time))
#             elif select == 2:
#                 path,key = get_key_path()
#                 start_time = time.time()
#                 XOR_decryption(path, key)
#                 end_time = time.time()
#                 elapsed_time = end_time - start_time
#                 print('Decryption Done...')
#                 print("Elapsed time: {:.2f} seconds".format(elapsed_time))
#             elif select == 3:
#                 break
#             else:
#                 print("error selection")
#         except ValueError:
#             print("Just select between 1 2 and 3")
#         finally:
#              print("----------------")

