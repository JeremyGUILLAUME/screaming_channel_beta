import numpy as np
from scipy.stats import pearsonr

#import attack_tools as att_tls
import sca.classify as classify


def reduce_trace(TRACES, PROFILE, num_key_bytes=16):
    TRACES_REDUCED = []
    for byt in range(num_key_bytes):
        TRACES_REDUCED.append([])
        for trc in range(len(TRACES)):
            TRACES_REDUCED[byt].append(TRACES[trc][PROFILE[byt][-1]])
    return TRACES_REDUCED


def profiled_corr_attack(TRACES, PLAINTEXTS, PROFILE, guess_range="", variable="p_xor_k", mask=0xff, num_key_bytes=16, nb_traces=0, range_nbTrc=0):
    if nb_traces == 0:
        nb_traces = min(len(TRACES), len(PLAINTEXTS))
    TRACES_REDUCED = reduce_trace(TRACES, PROFILE, num_key_bytes)  #att_tls.
    if guess_range == "":
        guess_range = range(256)
    if range_nbTrc == 0:
        range_nbTrc = [nb_traces]

    LOG_PROBA = [[[0 for r in range(256)] for byt in range(num_key_bytes)] for n in range(len(range_nbTrc))]

    for byt in range(num_key_bytes):
        for guess in guess_range:
            clas  = classify.compute_variables(PLAINTEXTS, [guess], variable=variable, mask=mask, range_key_bytes=[byt])[0]
            leaks = np.asarray( [PROFILE[byt][clas[j]] for j in range(nb_traces) ]) 
            for rnge, rnge_index in zip(range_nbTrc, range(len(range_nbTrc))):
                r, p = pearsonr(leaks[:rnge], TRACES_REDUCED[byt][:rnge])
                LOG_PROBA[rnge_index][byt][guess] = r
            #r,p = pearsonr(leaks[:nb_traces], TRACES_REDUCED[byt][:nb_traces])
            #LOG_PROBA[byt][guess] = r

    return LOG_PROBA 



def print_pges(knownkey, LOG_PROBA, num_key_bytes=16):
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
    print("Sorted PGEs: ", np.sort(pge)[::-1] )
    print("Mean(PGEs): ", np.mean(pge) )
    print("Std(PGEs): ", np.std(pge) )

