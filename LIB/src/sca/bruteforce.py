import numpy as np
import sca.hel as hel

# Wrapper to call the Histogram Enumeration Library for key-enumeration
def complexity(PLAINTEXTS, KEY, LOG_PROBA, bit_bound_end=31):
    print("")
    print("Starting key enumeration using HEL")
    import ctypes
    from Crypto.Cipher import AES
   
    pt1 = np.array(PLAINTEXTS[0], dtype=ctypes.c_ubyte)
    pt2 = np.array(PLAINTEXTS[1], dtype=ctypes.c_ubyte)
 
    print("Assuming that we know two plaintext/ciphertext pairs")

    _key = bytes(KEY)
    _pt1 = bytes(pt1) 
    _pt2 = bytes(pt2) 
 
    cipher = AES.new(_key, AES.MODE_ECB)
 
    _ct1 = cipher.encrypt(_pt1)
    _ct2 = cipher.encrypt(_pt2)
    
    ct1 = [c for c in _ct1] 
    ct1 = np.array(ct1, dtype=ctypes.c_ubyte)
    ct2 = [c for c in _ct2] 
    ct2 = np.array(ct2, dtype=ctypes.c_ubyte)

    merge = 2
    bins = 512
    bit_bound_start = 0
    #bit_bound_end = 31#35

    #found = hel.bruteforce(LOG_PROBA, pt1, pt2, ct1, ct2, merge, bins, bit_bound_start, bit_bound_end)
    rank_min, rank_rounded, rank_max, time_rank = hel.rank(LOG_PROBA, KEY, merge, bins)

    return rank_rounded[0] #rank_max[0] #


def attack(PLAINTEXTS, KEY, LOG_PROBA, bit_bound_end=31):
    print("")
    print("Starting key enumeration using HEL")
    import ctypes
    from Crypto.Cipher import AES

    pt1 = np.array(PLAINTEXTS[0], dtype=ctypes.c_ubyte)
    pt2 = np.array(PLAINTEXTS[1], dtype=ctypes.c_ubyte)
 
    print("Assuming that we know two plaintext/ciphertext pairs")

    key = bytes(KEY)
    pt1 = bytes(PLAINTEXTS[0])
    pt2 = bytes(PLAINTEXTS[1])
    
    cipher = AES.new(key, AES.MODE_ECB)
    _ct1 = cipher.encrypt(pt1)
    _ct2 = cipher.encrypt(pt2)
       
    pt1 = PLAINTEXTS[0]
    pt2 = PLAINTEXTS[1]     
    ct1 = [c for c in _ct1]
    ct2 = [c for c in _ct2]

    merge = 2
    bins = 512
    bit_bound_start = 0
    #bit_bound_end = 31#35

    found = hel.bruteforce(LOG_PROBA, pt1, pt2, ct1, ct2, merge, bins, bit_bound_start, bit_bound_end)

    return found
