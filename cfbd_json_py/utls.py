# Creation Date: 08/30/2023 01:13 EDT
# Last Updated Date: 10/06/2023 07:54 PM EDT
# Author: Joseph Armstrong (armstrongjoseph08@gmail.com)
# File Name: utls.py
# Purpose: Houses utility functions for this python package.
####################################################################################################

import json
import os
import secrets
import logging


def reverse_cipher_encrypt(plain_text_str: str):
    """
    NOT INTENDED TO BE CALLED BY THE USER!

    Implements a reverse cipher encription to a plain text string.

    Parameters
    ----------
    `plain_text_str` (mandatory, str):
        The string you want to encrypt through reverse cipher encryption.

    Returns
    ----------
    A string encrypted through reverse cipher encryption.
    """
    translated_text = ''
    str_len = len(plain_text_str) - 1
    while str_len >= 0:
        translated_text = translated_text + plain_text_str[str_len]
        str_len = str_len - 1

    del plain_text_str

    return translated_text


def reverse_cipher_decrypt(encrypted_text_str: str):
    """
    NOT INTENDED TO BE CALLED BY THE USER!
    
    Decrypts a string that was presumed to be encrypted by a reverse cipher encryption.

    Parameters
    ----------
    `encrypted_text_str` (mandatory, str):
        The string you presume that is encrypted through reverse cipher encryption, 
        that you want decrypted.

    Returns
    ----------
    A decrypted string.

    """
    translated_text = ''
    str_len = len(encrypted_text_str) - 1

    while str_len >= 0:
        translated_text = translated_text + encrypted_text_str[str_len]
        str_len = str_len - 1

    del encrypted_text_str

    return translated_text


def get_cfbd_api_token(api_key_dir: str = None):
    """
    NOT INTENDED TO BE CALLED BY THE USER!
    
    If you've already set the API key using 
    `cfbd_json_py.utls.set_cfbd_api_token()`,
    you don't need to use this function.

    If the CFBD API key exists in the environment, 
    or is in a file, this function retrives the CFBD API key, 
    and returns it as a string.

    If this package is being used in a GitHub Actions action,
    set the key in the environment by 
    creating a repository secret nammed `CFBD_API_KEY`.

    Parameters
    ----------
    `api_key_dir` (str, optional):
        Optional argument. If `api_key_dir` is set to a non-null string, 
        `set_cfbd_api_token()` will attempt to save the key file in that directory,
        instead of this user's home directory.

    Returns
    ----------
    A CFBD API key that exists within this python environment,
    or within this computer.
    """
    # raise NotImplementedError('it ain\'t ready')

    try:
        key = os.environ['CFBD_API_KEY']
        return key
    except:
        logging.info(
            "CFBD key not found in this python environment.\nAttempting to load the API key from a file.")

    if api_key_dir != None:
        with open(f"{api_key_dir}/.cfbd/cfbd.json", "r") as f:
            json_str = f.read()

        json_data = json.loads(json_str)

        return_key = json_data['cfbd_api_token']
        return_key = reverse_cipher_decrypt(return_key)
        return_key = return_key[10:]
        return_key = return_key[:-10]

        del api_key_dir, json_str, json_data

        return return_key
    else:
        home_dir = os.path.expanduser('~')

        with open(f"{home_dir}/.cfbd/cfbd.json", "r") as f:
            json_str = f.read()

        json_data = json.loads(json_str)

        return_key = json_data['cfbd_api_token']
        return_key = reverse_cipher_decrypt(return_key)
        return_key = return_key[10:]
        return_key = return_key[:-10]

        del api_key_dir, json_str, json_data

        return return_key


def set_cfbd_api_token(api_key: str, api_key_dir: str = None):
    """
    Sets the CFBD API key into a file that exists 
    either in `{home_dir}/.cfbd/cfbd_key.json`, or in a custom directory.

    Parameters
    ----------
    `api_key` (str, mandatory):
        The CFBD API key you have. 
        DO NOT input `Bearer {your CFBD API key}`,
        this package will take care of that for you.

    `api_key_dir` (str, optional):
        Optional argument. If `api_key_dir` is set to a non-null string, 
        `set_cfbd_api_token()` will attempt to save the key file in that directory,
        instead of this user's home directory.

    Returns
    ----------
    Nothing. 
    This function only sets up the API key file that this package can reference later.
    """

    alph_letters = [
        "a",
        "b",
        "c",
        "d",
        "e",
        "f",
        "g",
        "h",
        "i",
        "j",
        "k",
        "l",
        "m",
        "n",
        "o",
        "p",
        "q",
        "r",
        "s",
        "t",
        "u",
        "v",
        "w",
        "x",
        "y",
        "z",
        "0",
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "A",
        "B",
        "C",
        "D",
        "E",
        "F",
        "G",
        "H",
        "I",
        "J",
        "K",
        "L",
        "M",
        "N",
        "O",
        "P",
        "Q",
        "R",
        "S",
        "T",
        "U",
        "V",
        "W",
        "X",
        "Y",
        "Z",
    ]

    front_hash = ''
    back_hash = ''

    for i in range(0, 10):
        r_str = secrets.choice(alph_letters)
        front_hash += r_str
        del r_str

    for i in range(0, 10):
        r_str = secrets.choice(alph_letters)
        back_hash += r_str
        del r_str

    encrypted_key = reverse_cipher_encrypt(api_key)

    json_str = f"{{\n\t\"cfbd_api_token\":\"{front_hash}{encrypted_key}{back_hash}\"\n}}"
    del encrypted_key
    # print(json_str)

    if api_key_dir != None:
        try:
            os.mkdir(f"{api_key_dir}/.cfbd")
        except:
            pass

        with open(f"{api_key_dir}/.cfbd/cfbd.json", "w+") as f:
            f.write(json_str)
    else:
        home_dir = os.path.expanduser('~')

        try:
            os.mkdir(f"{home_dir}/.cfbd")
        except:
            pass

        with open(f"{home_dir}/.cfbd/cfbd.json", "w+") as f:
            f.write(json_str)

    del json_str


# if __name__ == "__main__":
#     text = "Hello World"
#     e_text = reverse_cipher_encrypt(text)
#     ue_text = reverse_cipher_decrypt(e_text)

#     print(f"Original Text:\t{text}")
#     print(f"Encrypted Text:\t{e_text}")
#     print(f"Decrypted Text:\t{ue_text}")

#     print(f'remove first 2 characters from string: {text[2:]}')
#     print(f'remove last 2 characters from string: {text[:-2]}')

#     key = "hello world"
#     set_cfbd_api_token(key)
#     return_key = get_cfbd_api_token()
#     print(key)
#     print(return_key)
