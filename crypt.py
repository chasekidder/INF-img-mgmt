# Chase Kidder 2019
# inf_img_mgmt - crypt.py
# Cryptography Functions File

import logging
import sys

from Crypto import Random
from Crypto.Cipher import AES

import config as cfg
import funclib


def get_machine_id():
    try:
        # Grab the unique machine ID code
        machine_id_file = open("/etc/machine-id", "r")
        if machine_id_file.mode == 'r':
            machine_id = machine_id_file.read()

    except FileNotFoundError:
        logging.critical("machine-id not found")
        logging.exception("script killed due to critical error")
        sys.exit()

    return machine_id


def encrypt(data):

    # Generate a unique hash key
    key = get_machine_id().rstrip()
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

    # print(sys.getsizeof(iv))
    #print("IV_e: " + str(iv))
    #print("Data_e: " + str(ciphertext))

    return 0


def get_api_secret():

    key = get_machine_id().rstrip()

    file_in = open("api.key", "rb")

    # Read in the hash and iv from the file and strip the newline
    iv = file_in.readline().strip(b"\n")
    encr_data = file_in.readline()

    # print(sys.getsizeof(iv))
    #print("IV_u: " + str(iv))
    #print("Data_u: " + str(encr_data))

    cipher = AES.new(key, AES.MODE_CBC, iv)

    try:
        return cipher.decrypt(encr_data).decode("utf-8")

    except UnicodeDecodeError:
        logging.error("Unable to decrypt API Secret. Running API setup.")
        funclib.init_setup()
        return get_api_secret()
