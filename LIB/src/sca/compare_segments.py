import numpy as np
from scipy.stats import pearsonr

import tools as tools


def dist_segments(data, signal_length, offset, sampling_rate, num_traces_per_point):
    trace_A, trace_B = cut_segments(data, signal_length, offset, sampling_rate, num_traces_per_point)
    diff = compute_dist(trace_A, trace_B)
    return diff

def corr_segments(data, signal_length, offset, sampling_rate, num_traces_per_point):
    trace_A, trace_B = cut_segments(data, signal_length, offset, sampling_rate, num_traces_per_point)
    r, p = pearsonr(trace_A, trace_B)
    return r

def cut_segments(data, signal_length, offset, sampling_rate, num_traces_per_point):
    trace_length = (signal_length + offset) * sampling_rate

    trace_A = []
    trace_B = []
    for i in range(num_traces_per_point):
        start = int(i*trace_length)
        stop  = start + int(trace_length)
        if stop < len(data):
            if i%2 == 0:
                trace_A.append(data[start:stop])
            else:
                trace_B.append(data[start:stop])
        else:
            print(" Trace too short ! ")
            break

    trace_A = np.average(trace_A, axis=0)
    trace_A = tools.normalize_trace(trace_A)
    trace_B = np.average(trace_B, axis=0)
    trace_B = tools.normalize_trace(trace_B)
    return trace_A, trace_B

def compute_dist(trace_A, trace_B):
    diff = np.absolute(trace_A - trace_B)
    diff = sum(diff)
    return diff / len(trace_A) #* 100
