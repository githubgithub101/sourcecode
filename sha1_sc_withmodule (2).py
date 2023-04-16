import hashlib, time

fd = open("log.txt","w") #open file for outputlogs

def sha1_with_process(message):
    sha1 = hashlib.sha1()

    # Initial hash value
    print("Initial hash value: ", sha1.hexdigest())

    # Process each chunk of 64 bytes
    for i in range(0, len(message), 64):
        sha1.update(message[i:i+64])
        print(f"Processing chunk {i//64+1}: {' '.join([sha1.hexdigest()[i:i+8] for i in range(0, len(sha1.hexdigest()), 8)])} chunk: {message[i:i+64]}")
        print(f"Processing chunk {i//64+1}: {' '.join([sha1.hexdigest()[i:i+8] for i in range(0, len(sha1.hexdigest()), 8)])} chunk: {message[i:i+64]}", file=fd)    # Open a file for writing
        time.sleep(.03)

    # Final hash value
    print("Final hash value: ", sha1.hexdigest())
    return sha1.hexdigest()


# Example
#message = b'Hello'
message = b'HelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHello'

print(len(message))
print(f"FINAL HASH: {sha1_with_process(message)}", file=fd)
fd.close()





