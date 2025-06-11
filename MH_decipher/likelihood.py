import math
from typing import List
from MH_decipher.bigrams import get_bigrams, transition_matrix

def calculate_likelihood(decrypted_text: str, reference_text: str, alphabet: List[str] = None) -> float:
    """
    Spočítá věrohodnost dešifrovaného textu porovnáním přechodových matic.
    
    Args:
        decrypted_text: Dešifrovaný text k vyhodnocení
        reference_text: Referenční text v správném jazyce
        alphabet: Seznam znaků abecedy (pokud None, použije se výchozí)
    
    Returns:
        Věrohodnost jako float hodnota (vyšší = lepší)
    """
    if alphabet is None:
        alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ_")

    decrypted_bigrams = get_bigrams(decrypted_text)
    reference_bigrams = get_bigrams(reference_text)

    decrypted_matrix = transition_matrix(decrypted_bigrams, alphabet)
    reference_matrix = transition_matrix(reference_bigrams, alphabet)

    likelihood = 0.0
    for i in range(len(alphabet)):
        for j in range(len(alphabet)):
            observed_freq = decrypted_matrix[i][j]
            reference_prob = reference_matrix[i][j]

            if observed_freq > 0 and reference_prob > 0:
                likelihood += observed_freq * math.log(reference_prob)

    return likelihood


def compare_texts_likelihood(text1: str, text2: str, reference_text: str, alphabet: List[str] = None) -> tuple:
    """
    Porovná věrohodnost dvou textů vzhledem k referenčnímu textu.
    
    Args:
        text1: První text k porovnání
        text2: Druhý text k porovnání  
        reference_text: Referenční text
        alphabet: Seznam znaků abecedy
    
    Returns:
        Tuple (likelihood1, likelihood2, better_text_index)
        better_text_index: 0 pokud je text1 lepší, 1 pokud text2
    """
    likelihood1 = calculate_likelihood(text1, reference_text, alphabet)
    likelihood2 = calculate_likelihood(text2, reference_text, alphabet)

    better_index = 0 if likelihood1 > likelihood2 else 1

    return likelihood1, likelihood2, better_index
