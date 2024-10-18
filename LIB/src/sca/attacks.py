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


def pges(knownkey, LOG_PROBA, num_key_bytes=16):
    pges = []
    for byt in range(num_key_bytes):
        proba_order = np.argsort(LOG_PROBA[byt])[::-1]
        pges.append( list(proba_order).index(knownkey[byt]) )
    return pges



"""
def profiled_corr_attack(TRACES, PLAINTEXTS, PROFILE, guess_range="", variable="p_xor_k", mask=0xff, num_key_bytes=16, nb_traces=0):
    if nb_traces == 0:
        nb_traces = len(TRACES)
    TRACES_REDUCED = att_tls.reduce_trace(TRACES, PROFILE, num_key_bytes) 
    if guess_range == "":
        guess_range = range(256)

    LOG_PROBA = [[0 for r in range(256)] for byt in range(num_key_bytes)]

    for byt in range(num_key_bytes):
        for guess in guess_range:
            #clas = att_tls.compute_variable(PLAINTEXTS, guess, byt, variable)  #compute_variables(PLAINTEXTS, kguess, variable, mask, num_key_bytes):
            clas = classify.compute_variables(PLAINTEXTS, [guess], variable=variable, mask=mask, range_key_bytes=[byt])[0]
            leaks = np.asarray( [PROFILE[byt][clas[j]] for j in range(nb_traces) ]) 

            r,p = pearsonr(leaks[:nb_traces], TRACES_REDUCED[byt][:nb_traces])
            LOG_PROBA[byt][guess] = r

    return LOG_PROBA 

def profiled_corr_attack(TRACES_REDUCED, PLAINTEXTS, PROFILE, start, stop, range_n, variable="p_xor_k", mask=0xff, num_key_bytes=16, nb_traces=0):

    LOG_PROBA = [[[0 for r in range(256)] for byt in range(num_key_bytes)] for n in range(len(range_n))]

    for byt in range(num_key_bytes):
        for guess in range(256):
            clas = att_tls.compute_variable(PLAINTEXTS[start:stop], guess, byt, variable)  #compute_variables(PLAINTEXTS, kguess, variable, mask, num_key_bytes):
            leaks = np.asarray( [PROFILE[byt][clas[j]] for j in range(nb_traces) ]) 
            for rg, n in zip(range_n, range(len(range_n))):
                r,p = pearsonr(leaks[:rg], TRACES_REDUCED[byt][start:start+rg])
                LOG_PROBA[n][byt][guess] = r
    return LOG_PROBA 
"""


