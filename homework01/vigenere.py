import string


def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    ciphertext = ""
    alph_up = string.ascii_uppercase
    alph_low = string.ascii_lowercase

    for i, letter in enumerate(plaintext):
        if letter.isupper():
            index = alph_up.index(letter)
            keyword_index = alph_up.index(keyword[i % len(keyword)].upper())
            index = (index + keyword_index) % len(alph_up)
            ciphertext += alph_up[index]
        elif letter.islower():
            index = alph_low.index(letter)
            keyword_index = alph_low.index(keyword[i % len(keyword)].lower())
            index = (index + keyword_index) % len(alph_low)
            ciphertext += alph_low[index]
        else:
            ciphertext += letter
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    plaintext = ""
    alph_up = string.ascii_uppercase
    alph_low = string.ascii_lowercase

    for i, letter in enumerate(ciphertext):
        if letter.isupper():
            index = alph_up.index(letter)
            keyword_index = alph_up.index(keyword[i % len(keyword)].upper())
            index = (index - keyword_index) % len(alph_up)
            plaintext += alph_up[index]
        elif letter.islower():
            index = alph_low.index(letter)
            keyword_index = alph_low.index(keyword[i % len(keyword)].lower())
            index = (index - keyword_index) % len(alph_low)
            plaintext += alph_low[index]
        else:
            plaintext += letter
    return plaintext
