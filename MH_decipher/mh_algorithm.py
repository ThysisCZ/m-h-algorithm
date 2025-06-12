from .substitute_decrypt import substitute_decrypt
from .plausibility import plausibility
from .bigrams import transition_matrix, get_bigrams
from .mutate_key import mutate_key
import random
import math

#zasifrovany text
input = "NGQIWFNTQNXWEQNLNILPNFXWNRWIMNTQNCWPBUNNILCEGWYLNPWNBLJNJVTUNGHZLGQNXWRQNGYWGQNBWTUNSWNJQXWCNHBLYNPWNBMPWNHQJUGYLNEYLGQVNBWTUNSWNJQXWCNQBWGZWYNTGMZJLNGUPJQCMYNINGQIVNLNHQPBLGMYNPWNHZWTNJQYLNSWTNZWJYNCEZLHBMGWNHQSWTWPNHZWPWNFXWNVSWYLNPNGQIWFNTGLNJZQJUNIHWBNHQSTNFVPMFWNTLYNTQGWIVNBWNLPHQXNRYMINJNEZLXMCMFNJLFNCECWPNIHLBJUNPJZMHWYNIVRUNIHLBJUNPNBWRQVNPWNFXQVNXWXMNLXMNTQHZWTVNLXMNIHLBJUNCQHLJNFMNXWZQIVFMPNFVPMFNBQNVTWYLBNLRUPNGMTWYNLRUNRUYQNSMPBQNIWNSPWFNBWNFWYLNZLTLNFUPYMPNIWNRUCENFQEYLNSWPBWNSWTXQVNPYUPWBLNBQNSPWFNFUPYWYLNIWNRUCENPYLNPNBWRQVNTQHZWTVNTQGWTYLNRUCENBQNTQGWTYLNRUCENBQNSMPBWNLYWNNBUNSPMNBLFNXWJTWNILPXQVRWXNSTMNJNXMNEYWTNXMJTUNFWNXWXLHLTYQNHBLBNPWNBWNXLNBQNJTUINSWNCYQGWJNHZMXCWIXLNFUPYMNPMNIWNSWNXLNPGWBWNPLFNFLPNSMNZLTNHQEYWTYNXLNXMNVBZUIXWXUFLNQCMFLNHZWCWNSWXNXWTQGWTYNILHZMBNNBLJNGMTMPNGUTWCEYLNBUNXWVFMPNLXMNYELBNBUNFMYUNLYWNHQCEQHNJTUINSPWFNPMNBQNHLJ"

#text z knihy
book = "_VOZEM_DO_NEHO_A_ZAS_MNE_BEZI_DO_CESTY__ZACHVELA_SE_TAK_KUDY_VPRAVO_NEBO_VLEVO_TEDY_JE_KONEC_PTAL_SE_TISE_POKYVLA_HLAVOU_TEDY" \
"_JE_KONEC_OTEVREL_DVIRKA_VYSKOCIL_Z_VOZU_A_POSTAVIL_SE_PRED_KOLA_JED_REKL_CHRAPTIVE_POJEDES_PRESE_MNE_UJELA_S_VOZEM_DVA_KROKY_ZPE" \
"T_POJD_MUSIME_DAL_DOVEZU_TE_ASPON_BLIZ_K_HRANICIM_KAM_CHCES_ZPATKY_SKRIPEL_ZUBY_ZPATKY_S_TEBOU_SE_MNOU_NENI_ANI_DOPREDU_ANI_ZP" \
"ATKY_COPAK_MI_NEROZUMIS_MUSIM_TO_UDELAT_ABYS_VIDEL_ABY_BYLO_JISTO_ZE_JSEM_TE_MELA_RADA_MYSLIS_ZE_BYCH_MOHLA_JESTE_JEDNOU_SLYSET" \
"A_TO_JSEM_MYSLELA_ZE_BYCH_SLA_S_TEBOU_DOPREDU_DOVEDLA_BYCH_TO_DOVEDLA_BYCH_TO_JISTE_ALE__TY_JSI_TAM_NEKDE_ZASNOUBEN_JDI_K_NI_HL" \
"ED_NIKDY_ME_NENAPADLO_PTAT_SE_TE_NA_TO_KDYZ_JE_CLOVEK_PRINCEZNA_MYSLI_SI_ZE_JE_NA_SVETE_SAM_MAS_JI_RAD_POHLEDL_NA_NI_UTRYZNENYM" \
"A_OCIMA_PRECE_JEN_NEDOVEDL_ZAPRIT__TAK_VIDIS_VYDECHLA_TY_NEUMIS_ANI_LHAT_TY_MILY_ALE_POCHOP_KDYZ_JSEM_SI_TO_PAK"

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
    current_key = start_key
    decrypted_current = substitute_decrypt(text, current_key)

    #verohodnost aktualniho klice
    p_current = plausibility(decrypted_current, TM_ref)
    
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
        
        if i % 50 == 0:
            print(f"Iteration: {i}, Plausibility: {p_current}")
    
    best_decrypted_text = substitute_decrypt(text, current_key)
    return (f"Key: {''.join(current_key)}\nDecrypted text: {best_decrypted_text}")

print(mh_algorithm(input, matrix_ref, iterations, start))