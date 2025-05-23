import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

text = "ABM_DEAOMARDHMAVA_VNAERDALD_UAOMAZDNYPAA_VZHBDSVANDAYVWAWIOPABCKVBMARDLMABSDBMAYDOPAXDAWMRDZACYVSANDAYUNDACMWPBSV" \
"AHSVBMIAYDOPAXDAWMRDZAMYDBKDSAOBUKWVABPNWMZUSA_ABM_IAVACMNYVBUSANDACKDOAWMSVAXDOAKDWSAZHKVCYUBDACMXDODNACKDNDAER" \
"DAIXDSVANABM_DEAOBVAWKMWPA_CDYACMXOAEINUEDAOVSAOMBD_IAYDAVNCMRALSU_AWAHKVRUZUEAWVEAZHZDNA_CVYWPANWKUCDSA_ILPA_CVYWPA" \
"NAYDLMIANDAERMIARDRUAVRUAOMCKDOIAVRUA_CVYWPAZMCVWAEUARDKM_IEUNAEINUEAYMAIODSVYAVLPNABUODSAVLPALPSMAXUNYMA_DAXNDEAYDAE" \
"DSVAKVOVAEPNSUNA_DALPZHAEMHSVAXDNYDAXDORMIANSPNDYAZMNAEUAKDWSA_CVYWPARDEI_DNALIOALPNAEINDSABPOVYAYMAZMARDZHZDNAVARDNEU" \
"NARDLMALPAYDAMOBD_SUAVAXVAANCINYUSVAKIZDAOMAWSURVABUOUNAUARVAYMAXNDEAEPNSDSVA_DALPZHANSVANAYDLMIAOMCKDOIAOMBDOSVALPZH" \
"AYMAOMBDOSVALPZHAYMAXUNYDAVSDAAYPAXNUAYVEARDWODA_VNRMILDRAXOUAWARUAHSDOARUWOPAEDARDRVCVOSMACYVYANDAYDARVAYMAWOP_AX" \
"DAZSMBDWACKURZD_RVAEPNSUANUA_DAXDARVANBDYDANVEAEVNAXUAKVOACMHSDOSARVARUAIYKP_RDRPEVAMZUEVACKDZDAXDRARDOMBDOSA_VCKUYAA" \
"YVWABUOUNABPODZHSVAYPARDIEUNAVRUASHVYAYPAEUSPAVSDACMZHMCAWOP_AXNDEANUAYMACVW"

#funkce pro ziskani bigramu z textu
def get_bigrams(txt):
    n = len(txt)
    return [txt[i:i+2] for i in range(0, n - 1)]

bigrams = get_bigrams(text)
print(bigrams)

alphabet = list("VLZODTQHUXWSERMCFKNYIBJGP_A")

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

plt.figure(figsize=(10, 8))
sns.heatmap(transition_matrix(bigrams), xticklabels=alphabet, yticklabels=alphabet, cmap='viridis')
plt.title("Relativní přechodová matice bigramů")
plt.show()