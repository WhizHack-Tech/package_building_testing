#  ==================================================================================================================================================================================================================================================
#  File Name: crypt_func.py
#  Description: Includes functions to encrypt and decrypt data.

#  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#  Item Name: Whizhack Client Dashboard
#  Author URL: https://whizhack.in

#  ==================================================================================================================================================================================================================================================

import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad

key = 'abc123fda4213dfr' #Must Be 16 char for AES128 
def encrypt(encrypt_query):
    encrypt_query = pad(encrypt_query.encode(),16)
    cipher = AES.new(key.encode('utf-8'), AES.MODE_ECB)
    return base64.b64encode(cipher.encrypt(encrypt_query))


def decrypt(decrypt_query):
    decrypt_query = base64.b64decode(decrypt_query)
    cipher = AES.new(key.encode('utf-8'), AES.MODE_ECB)
    return unpad(cipher.decrypt(decrypt_query),16)