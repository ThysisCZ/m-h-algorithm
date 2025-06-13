import random
from typing import List

def mutate_key(key: List[str]) -> List[str]:
    """
    Vezme kľúč (zoznam znakov) a náhodne prehodí dve pozície.
    Vráti novú verziu kľúča.
    """
    new_key = key.copy()
    i, j = random.sample(range(len(new_key)), 2)
    new_key[i], new_key[j] = new_key[j], new_key[i]
    return new_key
