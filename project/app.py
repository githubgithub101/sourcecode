from io import BytesIO
import streamlit as st
from XOR_file_enc_threading import XOR_encryption, XOR_decryption

# import warnings
# warnings.filterwarnings("ignore")

# streamlit run app.py 2>NUL


st.title('XOR Cipher')
st.header('FILE ENCRYPTION USING XOR CIPHER')
st.write("""
File encryption using the XOR cipher is a method of securing the contents of a file by applying a simple encryption algorithm known as the XOR (exclusive OR) cipher. The XOR cipher is a symmetric encryption algorithm that operates on binary data, where each byte (or bit) in the file is bitwise XORed with a key, typically a sequence of bytes (or bits).
The XOR operation works by comparing the corresponding bits of two operands (in this case, the file data and the encryption key), and producing an output bit that is set to 1 if the two input bits are different (i.e., one is 0 and the other is 1), and 0 if the input bits are the same (i.e., both 0 or both 1). This operation is performed on each byte (or bit) of the file data, using the corresponding byte (or bit) of the encryption key, which is repeated cyclically to match the length of the file.
To encrypt a file using XOR cipher, each byte in the file is bitwise XORed with a corresponding byte from the encryption key. This process is reversible, meaning that the original file can be decrypted by applying the same XOR operation using the same encryption key. However, the security of the XOR cipher is relatively weak, as it is susceptible to various attacks, such as frequency analysis and known-plaintext attacks, and is not recommended for strong encryption requirements.
""")
st.write('---')
 
# Widgets
st.header('Inputs')

select_option = st.selectbox('Pick one', ['Encrypt', 'Decrypt'])


# Create a file uploader widget
if select_option:
    if select_option == 'Encrypt':
        uploaded_file = st.file_uploader("Choose a file", type=None)
    elif select_option == 'Decrypt':
        uploaded_file = st.file_uploader("Choose a file", type=['.enc'])
    else:
        pass

btn_disabled = True
Has_file = False
Has_key = False
Except_file =".enc"



# Check if a file has been uploaded
file_name = ""
if uploaded_file is not None:
    file_contents = uploaded_file.read()
    file_name = uploaded_file.name
    st.write(f"Filename: {file_name}")
    st.write(f"File size: {len(file_contents)} bytes")
    Has_file = True

key = st.text_input("KEY: ")
if key != "":
    Has_key = True
if Has_key and Has_file:
    btn_disabled = False

btn_submit = st.button(f'{select_option}', disabled = btn_disabled)

if select_option:
    if btn_submit:
        file_output =""
        st.write(f"Filename: {file_name}")
        st.write(f"key {key}")
        if select_option == "Encrypt":
            file = XOR_encryption(file_contents, key)
            file_output = file_name+".enc"
        if select_option == "Decrypt":
            file = XOR_decryption(file_contents, key)
            file_output = "decrypted_"+file_name[:-4]

        # Convert bytearray to BytesIO object
        file = BytesIO(file)

        # Set the file name
        file_name_output = file_output

        # Create a download button
        st.download_button(label='Download File', data=file, file_name=file_name_output, mime='application/octet-stream')

# phrase = st.text_input("FILE: ")
# shift_dir = st.selectbox("Shift direction: ", ('Forward', 'Backward'))
# shift_no = st.number_input("Shift Amount: ", min_value=1)

