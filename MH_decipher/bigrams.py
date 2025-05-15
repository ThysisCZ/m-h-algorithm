import numpy as np
text = "COCONUT"

#funkce pro ziskani bigramu z textu
def get_bigrams(txt):
    n = len(txt)
    return [txt[i:i+2] for i in range(0, n - 1)]

bigrams = get_bigrams(text)
print(bigrams)

alphabet = list("CONUT")

#funkce pro vytvoreni prechodove matice
def transition_matrix(bigrams):
    n = len(alphabet)
    #matice vyplnena nulami
    TM = np.zeros((n, n))

    #vypocet vyskytu po sobe jdoucich znaku
    for bigram in bigrams:
        c1 = bigram[0]
        c2 = bigram[1]
        i = alphabet.index(c1)
        j = alphabet.index(c2)
        TM[i][j] += 1
    
    #nahrazeni vsech nul jednickou
    TM[TM == 0] = 1

    #deleni hodnot poctem bigramu
    TM /= len(bigrams)
    
    return TM

print(transition_matrix(bigrams))