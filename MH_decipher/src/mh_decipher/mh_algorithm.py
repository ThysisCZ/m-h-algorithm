import re

import unicodedata

from .substitute_decrypt import substitute_decrypt
from .plausibility import plausibility
from .bigrams import transition_matrix, get_bigrams
from .mutate_key import mutate_key
import random
import math

#zasifrovany text
input = "NGQIWFNTQNXWEQNLNILPNFXWNRWIMNTQNCWPBUNNILCEGWYLNPWNBLJNJVTUNGHZLGQNXWRQNGYWGQNBWTUNSWNJQXWCNHBLYNPWNBMPWNHQJUGYLNEYLGQVNBWTUNSWNJQXWCNQBWGZWYNTGMZJLNGUPJQCMYNINGQIVNLNHQPBLGMYNPWNHZWTNJQYLNSWTNZWJYNCEZLHBMGWNHQSWTWPNHZWPWNFXWNVSWYLNPNGQIWFNTGLNJZQJUNIHWBNHQSTNFVPMFWNTLYNTQGWIVNBWNLPHQXNRYMINJNEZLXMCMFNJLFNCECWPNIHLBJUNPJZMHWYNIVRUNIHLBJUNPNBWRQVNPWNFXQVNXWXMNLXMNTQHZWTVNLXMNIHLBJUNCQHLJNFMNXWZQIVFMPNFVPMFNBQNVTWYLBNLRUPNGMTWYNLRUNRUYQNSMPBQNIWNSPWFNBWNFWYLNZLTLNFUPYMPNIWNRUCENFQEYLNSWPBWNSWTXQVNPYUPWBLNBQNSPWFNFUPYWYLNIWNRUCENPYLNPNBWRQVNTQHZWTVNTQGWTYLNRUCENBQNTQGWTYLNRUCENBQNSMPBWNLYWNNBUNSPMNBLFNXWJTWNILPXQVRWXNSTMNJNXMNEYWTNXMJTUNFWNXWXLHLTYQNHBLBNPWNBWNXLNBQNJTUINSWNCYQGWJNHZMXCWIXLNFUPYMNPMNIWNSWNXLNPGWBWNPLFNFLPNSMNZLTNHQEYWTYNXLNXMNVBZUIXWXUFLNQCMFLNHZWCWNSWXNXWTQGWTYNILHZMBNNBLJNGMTMPNGUTWCEYLNBUNXWVFMPNLXMNYELBNBUNFMYUNLYWNHQCEQHNJTUINSPWFNPMNBQNHLJ"

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
    # odstraní ze znaků veškerou diakritiku
    text = ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')
    text = text.replace(' ', '_')  # nahradí mezery podtržítky
    # odstraní všechny znaky, které nejsou velké písmeno nebo podtržítku, tj. všechny znaky které nejsou v uvažované abecedě
    text = re.sub(r'[^A-Z_]', '', text)
    # nahrazení více podtržítek jedním, nepoužito, vstupní text může obsahovat více mezer za sebou a stejně tak text k dešifrování
    # text = re.sub(r'_+', '_', text)
    return text


#text z knihy
input_text_filename="../../krakatit.txt"
file=open(input_text_filename,"r",encoding="utf-8")
book=file.read()
file.close()

book=normalize_text_to_alphabet(book) # remove diacritics and non letter characters


#abeceda pismen
alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ_")

#bigramy nezasifrovaneho textu
bigrams = get_bigrams(book)

#matice nezasifrovaneho textu
matrix_ref = transition_matrix(bigrams, alphabet)

#nahodne vygenerovany pocatecni klic
start = random.sample(alphabet, 27)

#pocet iteraci algoritmu
iterations = 20000

def mh_algorithm(text, TM_ref, iter, start_key):
    """
    Funkce, která konverguje k nejlepšímu klíči podle výsledné pravděpodobnosti.
    
    Args:
        text: Vstupní zašifrovaný text
        TM_ref: Referenční matice bigramů sestrojená z nezašifrovaného textu
        iter: Počet iterací algoritmu
        start_key: Náhodně vygenerovaný počáteční klíč
    
    Returns:
        Nejlepší klíč a dešifrovaný text jako datový typ string
    """
    current_key = start_key
    decrypted_current = substitute_decrypt(text, current_key)

    #verohodnost aktualniho klice
    p_current = plausibility(decrypted_current, TM_ref)

    best_key=current_key
    p_best=p_current

    for i in range(1, iter):
        #prohozeni dvou znaku
        candidate_key = mutate_key(current_key)
        decrypted_candidate = substitute_decrypt(text, candidate_key)
        
        #verohodnost kandidatniho klice
        p_candidate = plausibility(decrypted_candidate, TM_ref)

        #vypocet pravdepodobnosti prijeti noveho klice
        q = math.exp(p_candidate - p_current)

        #kriterium pro prijeti klice
        accept = False

        #klic prijmeme vzdy pokud je q > 1
        if q > 1:
            accept = True
        #nebo kdyz je nahodne cislo < 0.0005
        elif random.uniform(0, 1) < 0.0005:
            accept = True
        
        if accept:
            current_key = candidate_key
            p_current = p_candidate

        # pokud je klíč lepší než nejlepší zatím nalezený, je označen jako nejlepší
        if p_current / p_best > 1:
            best_key = current_key
            p_best = p_current

        if i % 50 == 0:
            print(f"Iteration: {i}, Plausibility: {p_current}")
    
    best_decrypted_text = substitute_decrypt(text, best_key)
    return (f"Key: {''.join(best_key)}\nDecrypted text: {best_decrypted_text}")



print(mh_algorithm(input, matrix_ref, iterations, start))