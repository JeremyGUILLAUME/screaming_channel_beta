import numpy as np
import sca.AES as AES



def load_cp(filename, number):
    with open(filename + ".txt", "r") as f:
        data = ''
        for i in range(number):
            data += f.readline()
        if data[len(data)-1] == '\n':
             data = data[0:len(data)-1]

    #data = [[ord(c) for c in line.decode('hex')] for line in data.split('\n')]
    data = [[c for c in bytes.fromhex(line)] for line in data.split('\n')]

    cp = []
    for i in range(number):
        cp.append(data[i])
    return cp



def load_k(filename):
    with open(filename + ".txt", "r") as f:
        data = f.readline()
        if data[len(data)-1] == '\n':
             data = data[0:len(data)-1]
    #k = [ord(c) for c in data.decode('hex')] 
    k = [c for c in bytes.fromhex(data)]
    return k



def load_traces(filename, number):
    traces = []
    for i in range(number):
        trace = np.load(filename + "_%d.npy"%i)
        traces.append(trace)
    return traces



def compute_c(p, k):
    cipher = AES.myAES(k)
    c = []
    for i in range(num_traces_profile):
        c.append( cipher.encrypt(p[i]) )
    return c



def load_all(data_path, p_name, k_name, trc_name, nb_trc):
    p = load_cp(data_path + p_name, nb_trc)
    k = load_k(data_path + k_name)
    traces = load_traces(data_path + trc_name, nb_trc)
    return p, k, traces
