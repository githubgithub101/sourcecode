
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
