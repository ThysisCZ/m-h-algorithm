import re
import unicodedata
import random
import math

from .substitute_decrypt import substitute_decrypt
from .plausibility import plausibility


def normalize_text_to_alphabet(text):
    """
    Normalizes the text to contain only characters from default alphabet.
    Converts to uppercase, removes diacritics, removes numbers and other symbols, replaces space with '_'.

    Parameters:
    -----------
    text : string
        text that should be normalized

    Returns:
    --------
    string
        text containing only characters from default_alphabet
    """
    text = text.upper()
    text = ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')
    text = text.replace(' ', '_')
    text = re.sub(r'[^A-Z_]', '', text)
    return text


def mutate_key_advanced(key):
    """ Pokročilejšia mutácia kľúča — rôzne typy mutácií """
    method = random.choice(["swap", "reverse", "shift"])

    if method == "swap":
        i, j = random.sample(range(len(key)), 2)
        key[i], key[j] = key[j], key[i]
    elif method == "reverse":
        i, j = sorted(random.sample(range(len(key)), 2))
        key[i:j+1] = reversed(key[i:j+1])
    elif method == "shift":
        idx = random.randint(0, len(key) - 2)
        key = key[:idx] + [key[idx+1]] + [key[idx]] + key[idx+2:]

    return key

"""This array contains all plausabilitiest from last call of function prolom substitute, can be used as input to a graph for example."""
plausabilities = []

def prolom_substitute(text, TM_ref, iter, start_key, alphabet):
    """
    Tries to find key to decrypt entered text.
    You can see all plausabilitiest in global variable plausabilities that contains all plausabilities from last call of this function.

    Parameters:
    -----------
    text : string
        encrypted text for analysis
    TM_ref : two_dimensional array
        transition matrix used for cryptoanalysis
    iter : integer
        number of iterations (=number of tried keys)
    start_key : string
        first key used to text decryption
    alphabet : string, optional
        alphabet to use

    Returns:
    --------
    tuple (best_key, best_text, best_score)
        where best_key is found key with the best plausability, best_text is text decrypted by the best key and best_score is plausability of the best_key
    """
    current_key = start_key
    decrypted_current = substitute_decrypt(text, current_key)
    p_current = plausibility(decrypted_current, TM_ref)

    best_key = current_key[:]
    best_score = p_current

    global plausabilities
    plausabilities = []

    for i in range(1, iter + 1):
        candidate_key = mutate_key_advanced(current_key[:])
        decrypted_candidate = substitute_decrypt(text, candidate_key)
        p_candidate = plausibility(decrypted_candidate, TM_ref)

        delta = p_candidate - p_current
        q = math.exp(min(0, delta))  # prijmeme horší stav s pravdepodobnosťou exp(-Δ)

        if delta > 0 or random.uniform(0, 1) < q:
            current_key = candidate_key
            p_current = p_candidate

        if p_candidate > best_score:
            best_key = candidate_key
            best_score = p_candidate

        if i % 500 == 0 or i == 1:
            bigrams_count = max(1, len(text) - 1)
            normalized_plausibility = p_current / bigrams_count
            print(f"Iteration {i}: plausibility = {normalized_plausibility:.2f}")
            plausabilities.append(normalized_plausibility)  # uloží věrohodnost, následně je lze například zobrazit v grafu

    best_text = substitute_decrypt(text, best_key)
    return best_key, best_text, best_score
