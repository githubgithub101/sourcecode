import hashlib
def sha1_with_process(message):
    sha1 = hashlib.sha1()
    # Initial hash value
    print("Initial hash value: ", sha1.hexdigest())

    # Process
    sha1.update(message)
    return sha1.hexdigest()

# Example
message = b'HelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHello'

print(f"message lenght:{len(message)} bytes")
print(f"FINAL HASH: {sha1_with_process(message)}")





