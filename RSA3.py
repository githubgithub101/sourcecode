# import rsa

# # generate public and private keys with
# # rsa.newkeys method,this method accepts
# # key length as its parameter
# # key length should be atleast 16
# publicKey, privateKey = rsa.newkeys(512)

# print(publicKey)
# print(privateKey)

# # this is the string that we will be encrypting
# message = "hello geeks"

# # rsa.encrypt method is used to encrypt
# # string with public key string should be
# # encode to byte string before encryption
# # with encode method
# encMessage = rsa.encrypt(message.encode(), publicKey)

# print("original string: ", message)
# print("encrypted string: ", encMessage)

# # the encrypted message can be decrypted
# # with ras.decrypt method and private key
# # decrypt method returns encoded byte string,
# # use decode method to convert it to string
# # public key cannot be used for decryption
# decMessage = rsa.decrypt(encMessage, privateKey).decode()

# print("decrypted string: ", decMessage)










# import rsa

# public_key, private_key = rsa.newkeys(512)

# def encrypt_text(plain_text):
#     plain_text = plain_text.encode('utf8')
#     encrypted_text = rsa.encrypt(plain_text, public_key)
#     return encrypted_text

# def decrypt_text(encrypted_text):
#     decrypted_text = rsa.decrypt(encrypted_text, private_key)
#     return decrypted_text.decode("utf-8")

# # testing
# plain_text = "Hello this is an important message"

# encrypted_text = encrypt_text(plain_text)
# print("Encrypted text is = %s" %(encrypted_text))

# decrypted_text = decrypt_text(encrypted_text)
# print("Decrypted text is = %s" %(decrypted_text))












# from math import gcd

# # defining a function to perform RSA approch
# def RSA(p: int, q: int, message: int):
#     # calculating n
#     n = p * q

#     # calculating totient, t
#     t = (p - 1) * (q - 1)

#     # selecting public key, e
#     for i in range(2, t):
#         if gcd(i, t) == 1:
#             e = i
#             break
    
#     # selecting private key, d
#     j = 0
#     while True:
#         if (j * e) % t == 1:
#             d = j
#             break
#         j += 1

#     # performing encryption
#     ct = (message ** e) % n
#     print(f"Encrypted message is {ct}")

#     # performing decryption
#     mes = (ct ** d) % n
#     print(f"Decrypted message is {mes}")

# # Testcase - 1
# RSA(p=1427, q=1429, message=5555)












import random
from math import gcd



# function to generate random prime numbers
def generate_prime_number():
    while True:
        prime_candidate = random.randint(2**15, 2**16)
        if is_prime(prime_candidate):
            return prime_candidate

# function to check if a number is prime
def is_prime(num):
    if num == 2:
        return True
    if num < 2 or num % 2 == 0:
        return False
    for n in range(3, int(num**0.5)+2, 2):
        if num % n == 0:
            return False
    return True


# def generate_keypair(p, q):
#     n = p * q
#     phi = (p - 1) * (q - 1)
#     e = random.randrange(1, phi)
#     g = gcd(e, phi)
#     while g != 1:
#         e = random.randrange(1, phi)
#         g = gcd(e, phi)
#     d = multiplicative_inverse(e, phi)
#     return ((e, n), (d, n))

def generate_keypair(p, q):
    # Generate two large prime numbers
    # Calculate n and totient
    n = p * q
    totient = (p - 1) * (q - 1)

    # Choose public key e
    e = random.randrange(1, totient)
    g = gcd(e, totient)
    while g != 1:
        e = random.randrange(1, totient)
        g = gcd(e, totient)

    # Calculate private key d
    d = pow(e, -1, totient)

    # Return public and private key pair
    return ((e, n), (d, n))


def multiplicative_inverse(e, phi):
    d = 0
    x1 = 0
    x2 = 1
    y1 = 1
    temp_phi = phi

    while e > 0:
        temp1 = temp_phi // e
        temp2 = temp_phi - temp1 * e
        temp_phi = e
        e = temp2

        x = x2 - temp1 * x1
        y = d - temp1 * y1

        x2 = x1
        x1 = x
        d = y1
        y1 = y

    if temp_phi == 1:
        return d + phi

def encrypt(pk, plaintext):
    key, n = pk
    cipher = [pow(ord(char), key, n) for char in plaintext]
    return cipher

def decrypt(pk, ciphertext):
    key, n = pk
    plain = [chr(pow(char, key, n)) for char in ciphertext]
    return ''.join(plain)

# Example usage:
if __name__ == '__main__':
    # p = 61
    # q = 53
    p = generate_prime_number()
    q = generate_prime_number()

    print(f"p: {p}")
    print(f"q: {q}")
    print(f"n = {p}*{q} = {p*q}")
    print(f"t = {p-1}*{q-1} = {(p-1)*(q-1)}")

    public, private = generate_keypair(p, q)

    print(f"e = {public[0]}")
    print(f"d = {private[0]}")

    print(f"Public key: e = {public[0]} | n = {public[1]}")
    print(f"Private key: d = {private[0]} ^ {-1} mod {p * q} = {private[0]} | n = {public[1]}")

    message = 'Hello Bob! How are you?'
    print(f"message: {message}")
    print(f"message: {[ord(char) for char in message]}")
    
    cipher = encrypt(public, message)
    print(f"Cipher text: {cipher}")
    plain = decrypt(private, cipher)
    print(f"Plain text: {plain}")

    print("\n\n")
    print(f"Char: {message[0]} = {ord(message[0])}")
    print(f"{ord(message[0])} ^ {public[0]} = {ord(message[0]) ^ public[0]}")

    cipher_T = pow(ord(message[0]), public[0], public[1])
    print(f"cipher_T: = {ord(message[0])} ^ {public[0]} mod {public[1]} = {cipher_T}")
    print("\t\t  Public_k(e)    Public_k(n)  cipher")
    print(f"decrypted: {cipher_T} ^ {private[0]} mod {p * q} = {pow(cipher_T, private[0], public[1])}")
    print("\t     cipher   private_k(d)     Public_k(n)")


    print(pow(ord(message[0]), public[0], public[1]))
    print(pow(cipher_T, private[0], public[1]))




