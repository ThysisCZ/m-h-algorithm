default_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ_"

def substitute_decrypt(ciphertext, key, alphabet=default_alphabet):
    key_array = list(key)
    mapping = {}

    for i in range(len(alphabet)):
        mapping[key_array[i]] = alphabet[i]

    decrypted_text = ""
    for char in ciphertext:
        if char in mapping:
            decrypted_text += mapping[char]
        else:
            decrypted_text += char

    return decrypted_text