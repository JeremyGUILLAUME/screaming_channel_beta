import numpy as np
from matplotlib import pyplot as plt


def print_result(knownkey, LOG_PROBA, num_key_bytes=16):
    pge = []
    for byt in range(num_key_bytes):
        proba_order = np.argsort(LOG_PROBA[byt])[::-1]
        pge.append( list(proba_order).index(knownkey[byt]) )

    bestguess = []
    for byt in range(num_key_bytes):
        bestguess.append( np.argmax(LOG_PROBA[byt]) )

    print("Best Key Guess: ", end=" ")
    for b in bestguess: print(" %02x "%b, end=" ")
    print("")
    
    print("Known Key:      ", end=" ")
    for b in knownkey: print(" %02x "%b, end=" ")
    print("")
    
    print("PGE:            ", end=" ")
    for b in pge: print("%03d "%b, end=" ")
    print("")

    print("SUCCESS:        ", end=" ")
    nb_byt_recovered = 0
    for g,r in zip(bestguess, knownkey):
        if(g==r):
            print("  1 ", end=" ")
            nb_byt_recovered += 1
        else:
            print("  0 ", end=" ")
    print("")
    print("NUMBER OF CORRECT BYTES: %d"%nb_byt_recovered)



def print_stats(knownkey, LOG_PROBA, num_key_bytes=16):
    pge = []
    for byt in range(num_key_bytes):
        proba_order = np.argsort(LOG_PROBA[byt])[::-1]
        pge.append( list(proba_order).index(knownkey[byt]) )

    print("")
    print(np.sort(pge)[::-1] )
    print(np.mean(pge) )
    print(np.std(pge) )









def print_result_3(byt, knownkey, foundkey, LOG_PROBA):
    cparefs = np.argsort(LOG_PROBA[byt])[::-1]
    pge_k = list(cparefs).index(knownkey)
    pge_f = list(cparefs).index(foundkey)
    return pge_k, pge_f

def print_result_4(byt, LOG_PROBA):
    pges = [0]*256
    cparefs = np.argsort(LOG_PROBA[byt])[::-1]
    for i in range(256):
        pges[i] = list(cparefs).index(i)
    return pges


def print_result_5(knownkey, LOG_PROBA):
    pges = [0]*16
    for byt in range(16):
        cparefs = np.argsort(LOG_PROBA[byt])[::-1]
        pges[byt] = list(cparefs).index(knownkey[byt])
    return pges


"""
pges = []
for i in range(256):
    pges.append([])

for i in range(1, nb_t):
    traces = []
    traces.append( preprocess.preprocess_traces(trc, start_SOI, end_SOI) )
    pge, LOG_PROBA = ta_pearsonR.run_attack_PearsonR_Multi_PGE(traces, pln, k, profiles, nb_traces = i)
    pges_ = plt_att.print_result_4(nb_byt, LOG_PROBA)
    for pg in range(256):
        pges[pg].append(255 - pges_[pg])

for i in range(256):
    plt.plot(pges[i])

plt.plot(pges[k[nb_byt]], 'b', linewidth=2)

plt.plot(pges[0xca], 'r', linewidth=2)

plt.show()
"""




