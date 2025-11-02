import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

default_alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ_")

def get_bigrams(text):
    """
    Funkce pro získání bigramů z textu.

    Args:
        text: Posloupnost znaků, ze které chceme získat všechny bigramy

    Returns:
        Výpis bigramů jako list
    """
    return [text[i:i+2] for i in range(len(text) - 1)]


def transition_matrix(bigrams, alphabet=default_alphabet):
    """
    Funkce pro vytvoření relativní přechodové matice bigramů.

    Args:
        bigrams: Seznam bigramů (např. výstup z get_bigrams)
        alphabet: Abeceda použitá pro indexování znaků

    Returns:
        Relativní přechodová matice jako NumPy pole (2D)
    """
    n = len(alphabet)
    TM = np.zeros((n, n))

    for bigram in bigrams:
        if len(bigram) == 2:
            c1, c2 = bigram[0], bigram[1]
            if c1 in alphabet and c2 in alphabet:
                i = alphabet.index(c1)
                j = alphabet.index(c2)
                TM[i][j] += 1

    # Nahrazení nul jedničkami a přičtení 1 k existujícím
    TM += 1  # Každý prvok zvýšime o 1 → Laplace smoothing

    # Normalizace – celkový součet bude 1
    TM /= np.sum(TM)

    return TM


def visualize_matrix(TM, alphabet=default_alphabet):
    """
    Funkce pro vizualizaci přechodové matice pomocí heatmapy.

    Args:
        TM: Přechodová matice (NumPy array)
        alphabet: Seznam znaků, pro které se matice počítala
    """
    plt.figure(figsize=(10, 8))
    sns.heatmap(TM, xticklabels=alphabet, yticklabels=alphabet, cmap='viridis')
    plt.title("Relativní přechodová matice bigramů")
    plt.xlabel("Znak j (následuje)")
    plt.ylabel("Znak i (předchází)")
    plt.tight_layout()
    plt.show()
