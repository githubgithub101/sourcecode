import random
from math import gcd
from pyprimes import isprime

# # function to check if a number is prime or you can use modules to check if its a prime
# def is_prime(num):
#     if num == 2:
#         return True
#     if num < 2 or num % 2 == 0:
#         return False
#     for n in range(3, int(num**0.5)+2, 2):
#         if num % n == 0:
#             return False
#     return True

# function to generate random prime numbers
def generate_prime_number():
    while True:
        prime_candidate = random.randint(2**15, 2**16)
        # if is_prime(prime_candidate):
        if isprime(prime_candidate):
            return prime_candidate

# function to get GCD or simply you can use modules instead
# def gcd(a, h):
# 	temp = 0
# 	while(1):
# 		temp = a % h
# 		if (temp == 0):
# 			return h
# 		a = h
# 		h = temp

def gen_publickey_e():
    # Choose public key e
    e = random.randrange(1, totient)
    g = gcd(e, totient)
    print(f"gcd({e}, {totient}) = {g}")
    while g != 1:
        e = random.randrange(1, totient)
        g = gcd(e, totient)
        print(f"gcd({e}, {totient}) = {g}")
    print()
    return e

def gen_totient(): # totient or phi
    return (p-1)*(q-1)

def prod_of_pq():
    return p*q

p = generate_prime_number()
q = generate_prime_number()
n = prod_of_pq()
totient = gen_totient()
e = gen_publickey_e()
d = pow(e, -1, totient)  # Private key (d stands for decrypt) Calculate private key d or the modular inverse of e and phi

# Message to be encrypted
msg = 4894748
# msg = 5
print(f"Message data =\t{msg}")
print(f"p = \t\t{p}")
print(f"q = \t\t{q}")
print(f"n = p*q = \t{n}")
print(f"e = \t\t{e}")
print(f"d = \t\t{d}")
print(f"phi=(p-1)*(q-1) = {totient}")

print()
print(f"Encryption keys e: {e} n: {n}")
# Encryption c = (msg ^ e) % n
print("Encryption c = (msg ^ e) % n")
c = pow(int(msg), int(e), int(n))
print("Encrypted data = ", c)

# Decryption m = (c ^ d) % n
print(f"\nDecryption keys d: {d} n: {n}")
print("Decryption m = (c ^ d) % n")
m = pow(int(c), int(d), int(n))
print("Original Message = ", m)
