import numpy as np
from matplotlib import pyplot as plt


def find_pois(SETS, CLASSES, plot=False, num_key_bytes=16):
    POIS = []

    for byt in range(num_key_bytes):
        mean_C = []
        var_C = []
        for cl in range(len(CLASSES[byt])):
            var_C.append(np.var(SETS[byt][cl], axis=0) )
            mean_C.append(np.average(SETS[byt][cl], axis=0) )
        mean_vars = np.average(var_C, axis = 0)
        var_means = np.var(mean_C, axis = 0)

        snr = var_means / mean_vars
        POIS.append( np.argmax( snr ) )

        if plot:
            plt.plot(snr)

    if plot:
        plt.show()

    return POIS



"""
def find_pois(SETS, CLASSES, plot=False, num_key_bytes=16):
    POIS = []

    for byt in range(num_key_bytes):
        var_C = []
        for cl in range(len(CLASSES[byt])):
            var_C.append(np.var(SETS[byt][CLASSES[byt][cl]], axis=0) )
        mean_vars = np.average(var_C, axis = 0)

        mean_C = []
        for cl in range(len(CLASSES[byt])):
            mean_C.append(np.average(SETS[byt][CLASSES[byt][cl]], axis=0) )
        var_means = np.var(mean_C, axis = 0)

        snr = var_means / mean_vars
        POIS.append( np.argmax( snr ) )

        if plot:
            plt.plot(snr)

    if plot:
        plt.show()

    return POIS
"""
