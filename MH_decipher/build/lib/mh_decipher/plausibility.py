import numpy as np
from .bigrams import get_bigrams

default_alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ_")
alphabet_index = {char: idx for idx, char in enumerate(default_alphabet)}

def plausibility(text, TM_ref, alphabet_param=None):
    """
    Counts plausability which means how the text (decrypted by some key) corresponds with transition matrix, the higher the better.

    Parameters:
    -----------
    text : string
        decrypted text
    TM_ref : two_dimensional array
        transition matrix to compare decrypted text with
    alphabet_param : string, optional
        alphabet to use
    Returns:
    --------
    decimal
         plausability as a decimal number from interval <0,1>
    """
    if alphabet_param is None:
        alphabet_param = default_alphabet

    bigrams = get_bigrams(text)
    if not bigrams:
        return float('-inf')  # text bez bigramů

    # Prepočítaj referenčnú maticu na NumPy a zaisti log(0) ochranu
    TM_ref_np = np.array(TM_ref)
    TM_ref_np[TM_ref_np == 0] = 1e-12  # veľmi malá pravdepodobnosť

    log_likelihood = 0.0
    for a, b in bigrams:
        if a in alphabet_index and b in alphabet_index:
            i, j = alphabet_index[a], alphabet_index[b]
            log_likelihood += np.log(TM_ref_np[i][j])
        else:
            log_likelihood += np.log(1e-8)  # penalizuj cudzie znaky

    return float(log_likelihood)


def plausibility_normalized(text, TM_ref, alphabet_param=None):
    """
    Pomocná funkcia len na zobrazovanie výsledkov.
    Vráti priemernú log-likelihood na bigram.
    """
    total_plausibility = plausibility(text, TM_ref, alphabet_param)
    if total_plausibility == float('-inf'):
        return float('-inf')
    
    bigrams = get_bigrams(text)
    if not bigrams:
        return float('-inf')
    
    return total_plausibility / len(bigrams)