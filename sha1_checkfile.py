import hashlib, time

fd = open("log.txt","w") #open file for outputlogs

# Open the file in binary mode
with open('Hello.txt', 'rb') as f:
    # Create a SHA-1 hash object
    sha1 = hashlib.sha256()
    # print("Initial hash value: ", sha1.hexdigest())
    # print("Initial hash value: ", sha1.hexdigest(), file=fd)   # save to text file
    
    chunk = 0
    counter = 0

    # Read the file in chunks and update the hash object
    while chunk != b'':
        counter+=1
        chunk = f.read(64)  #64 bytes chunks
        sha1.update(chunk)
        if chunk == b'': 
            f.close()
            break

        # print(f"Processing chunk {counter}: {sha1.hexdigest()} chunk: {chunk}")
        # print(f"Processing chunk {counter}: {sha1.hexdigest()} chunk: {chunk}", file=fd)    # Open a file for writing

        # print(f"Processing chunk {counter}: {' '.join([sha1.hexdigest()[i:i+8] for i in range(0, len(sha1.hexdigest()), 8)])} chunk: {chunk}")
        # print(f"Processing chunk {counter}: {' '.join([sha1.hexdigest()[i:i+8] for i in range(0, len(sha1.hexdigest()), 8)])} chunk: {chunk}", file=fd)    # Open a file for writing
        # time.sleep(.03)

# Get the hexadecimal representation of the digest
sha1_digest = sha1.hexdigest()

print(f"FINAL HASH: {sha1_digest}")
print(f"FINAL HASH: {sha1_digest}", file=fd)

f.close()
