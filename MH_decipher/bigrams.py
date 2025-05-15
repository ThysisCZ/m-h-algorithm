text = "Lorem ipsum dolor sit amet, consectetuer adipiscing elit."

#funkce pro ziskani bigramu z textu
def get_bigrams(txt):
    return [txt[i:i+2] for i in range(0, len(txt) - 1)]

print(get_bigrams(text))
