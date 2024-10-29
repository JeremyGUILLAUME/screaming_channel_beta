import numpy as np

import sca.filters as filters


def normalize_trace(trace):
    mu  = np.average(trace)
    std = np.std(trace)
    if std != 0:
        trace = (trace - mu) / std
    else:
        trace =  trace - mu
    return trace



def shift_trace(trace, shift):
    trace_aligned = list(trace[shift:]) + list(trace[:shift])
    return trace_aligned



def preprocess_traces(TRACES, SOI_start=1000, SOI_stop=1150, cutoff=550e3, sampling_rate=5e6, order=5):
    traces = []
    for i in range(len(TRACES)):
        traces.append( filters.butter_lowpass_filter( TRACES[i], cutoff, sampling_rate, order)[SOI_start : SOI_stop] )
    return traces
