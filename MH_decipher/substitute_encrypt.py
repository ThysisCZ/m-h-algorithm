default_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ_"


def substitute_encrypt(plaintext, key, alphabet=default_alphabet):
    mapping = {}
    for i in range(0, len(alphabet)):
        mapping[alphabet[i]] = key[i]
    encrypted_text = ""
    for char in plaintext:
        if char in mapping:
            encrypted_text += mapping[char]
        else:
            encrypted_text += char
    return encrypted_text
