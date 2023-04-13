import hmac

# Define the message and the secret key as byte strings
message = b"some message"
secret_key = b"secret_key"

# Generate the HMAC using SHA1 as the hash function
hmac_value = hmac.new(secret_key, message, digestmod="SHA1").hexdigest()

# Print the HMAC value
print(f"Messafe MAC value using SHA1 as hashing function: {hmac_value}")


# In this code, we import the hmac module to use its new function to generate an HMAC.
# We define the message and secret_key as byte strings using the b prefix. The b prefix indicates that the following string should be treated as a byte string instead of a regular string.
# We generate the HMAC by calling hmac.new with the secret_key, message, and the digestmod parameter set to "SHA1", which specifies that we want to use the SHA-1 hash function. The hexdigest method is then called on the resulting HMAC object to return the hexadecimal representation of the HMAC.
# Finally, we print the HMAC value using the print function.