# Copyright - Chase Kidder 2019
# inf_img_mgmt - crypt.py
# Cryptography Functions File

from Crypto.Cipher import AES
from Crypto import Random
import config as cfg
import sys
import socket
import hashlib



def get_id():
    # Generate an encryption key from the hostname
    hname = socket.gethostname()
    md5 = hashlib.md5(hname.encode('utf-8')).hexdigest()
    
    return md5


def encrypt(data):

    #Generate a unique hash key
    key = get_id()
    #print("Hash Key: " + key)

    iv = Random.get_random_bytes(16)
    

    # Create an encrypted file containing the API key and secret
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(data)

    # Write the hash to file as bytes with a newline
    file_out = open("api.key", "wb")
    file_out.write(iv)
    file_out.write(b"\n")
    file_out.write(ciphertext)

    #print(sys.getsizeof(iv))
    #print("IV_e: " + str(iv))
    #print("Data_e: " + str(ciphertext))

    return 0


def get_api_secret():

    key = get_id()

    file_in = open("api.key", "rb")

    # Read in the hash and iv from the file and strip the newline
    iv = file_in.readline().strip(b"\n")
    encr_data = file_in.readline()

    #print(sys.getsizeof(iv))
    #print("IV_u: " + str(iv))
    #print("Data_u: " + str(encr_data))

    cipher = AES.new(key, AES.MODE_CBC, iv)

    return cipher.decrypt(encr_data).decode("utf-8")

