#!/usr/bin/env python3

# Chase Kidder 2019
# pynf_media_manager - crypt.py
# Cryptography Function File

import Crypto

class encryptor():
    def __init__(self):
        self.hash_key = get_machine_id()

    def encrypt(self, data):
        iv = Crypto.Random.get_random_bytes(16)
        cipher = Crypto.AES.new(self.hash_key, Crypto.AES.MODE_CBC, iv)
        ciphertext = cipher.encrypt(data)
        self.__write_to_file(iv, ciphertext)

    def __write_to_file(self, iv, ciphertext):
        file_out = open("api.key", "wb")
        file_out.write(iv)
        file_out.write(b"\n")
        file_out.write(ciphertext)


class decryptor():
    def __init__(self):
        self.hash_key = get_machine_id()

    def decrypt_secret(self):
        iv, data = self.__read_file()

        cipher = Crypto.AES.new(self.hash_key, Crypto.AES.MODE_CBC, iv)

        try:
            return cipher.decrypt(data).decode("utf-8")

        except:
            pass

    def __read_file(self,):
        file = open("api.key", "rb")

        iv = file.readline().strip(b"\n")
        data = file.readline()

        return iv, data


def get_machine_id():
    """Returns Unique Machine ID From Linux System
    
    Returns:
        int: Local Machine ID
    """
    try:
        machine_id_file = open("/etc/machine-id", "r")
        if machine_id_file.mode == 'r':
            machine_id = machine_id_file.read()

    except FileNotFoundError:
        pass

    return machine_id.rstrip()


def get_api_secret():
    decrypt = decryptor()

    try:
        return decrypt.decrypt_secret()
    except:
        pass