import numpy as np
from scipy import signal

import sca.filters as filters


#########################################################################
def virtual_trigger(data, signal_length, sampling_rate, time_div):
    trace_length = signal_length * sampling_rate

    starts = []
    traces = []
    for i in range(time_div):
        starts.append( int(i*trace_length) )

        start = starts[-1] 
        stop  = start + int(trace_length)
        if stop < len(data):
            traces.append(data[start:stop])
        else:
            print(" Trace too short ! ")
            break

    return starts, traces



#########################################################################
def pattern_recognition(data, pattern, signal_length, sampling_rate, corr_min, time_div):
    trace_length = int(signal_length * sampling_rate)

    data_lpf = filters.butter_lowpass_filter(data, sampling_rate / 4, sampling_rate)
    pattern_lpf = filters.butter_lowpass_filter(pattern, sampling_rate / 4, sampling_rate)

    trigg = signal.correlate(data_lpf, pattern_lpf)[ len(pattern) : -len(pattern) ]
    trigg_sorted = np.argsort( trigg )[::-1]
    threshold  = max( trigg ) * corr_min

    dist_before   = int(len( pattern ) / 2)
    dist_after    = int(len( pattern ) / 2)
    allowed_segmts = [0]*dist_before + [1]*len( trigg ) + [0]*dist_after 
    
    starts = []
    for trigg_index in trigg_sorted:
        if len(starts) >= time_div:
            break;

        if trigg[ trigg_index ] <= threshold:
            break;

        if allowed_segmts[ trigg_index + dist_before ] == 1:
            starts.append( trigg_index )
            allowed_segmts[ trigg_index  : dist_before + trigg_index + dist_after ] = [0]*(dist_before+dist_after) 

    starts = np.sort( starts )

    traces = []
    for start in starts:
        stop = start + trace_length
        if stop > len(data):
            break
        traces.append(data[start:stop])

    return starts, traces



#########################################################################
def freqComp_trigger(data, signal_length, sampling_rate, corr_min, time_div, bandpass_lower, bandpass_upper, lowpass_freq, pattern=None):
    trace_length = int(signal_length * sampling_rate)

    trigger = filters.butter_bandpass_filter(data, bandpass_lower, bandpass_upper, sampling_rate, 6)
    trigger = np.absolute(trigger)
    trigger = filters.butter_lowpass_filter(trigger, lowpass_freq, sampling_rate, 6)

    average = np.average(trigger)
    trigger_fn = lambda x, y: x > y

    trigger_signal = trigger_fn(trigger, average)
    starts = np.where( (trigger_signal[1:] != trigger_signal[:-1]) * trigger_signal[1:])[0] + 1 


    traces = []
    if pattern is None:
    #Create a pattern on the fly
        for start in starts:
        
            if len(traces) >= time_div:
                break

            stop = start + trace_length
            if stop > len(data):
                break
            
            trace = data[start:stop]
        
            #Align Traces with a pattern created on the fly
            if len(traces) < 1:
                traces.append(trace)
                continue
            else:
                pattern = np.average(traces, axis=0)
                pattern_lpf = filters.butter_lowpass_filter(pattern, sampling_rate / 4, sampling_rate)
                trace_lpf = filters.butter_lowpass_filter(trace, sampling_rate / 4, sampling_rate)
                correlation = signal.correlate(trace_lpf**2, pattern_lpf**2)
            
                if max(correlation) <= corr_min: 
                    continue
                
                shift = np.argmax(correlation) - (len(pattern)-1)
                traces.append(data[start+shift:stop+shift])


    else:
        pattern_lpf = filters.butter_lowpass_filter(pattern, sampling_rate / 4, sampling_rate)
        for start in starts:
        
            if len(traces) >= time_div:
                break

            stop = start + trace_length
            if stop > len(data):
                break
            
            trace = data[start:stop]
            trace_lpf = filters.butter_lowpass_filter(trace, sampling_rate / 4, sampling_rate)
            correlation = signal.correlate(trace_lpf**2, pattern_lpf**2)
        
            if max(correlation) <= corr_min: 
                continue
            
            shift = np.argmax(correlation) - (len(pattern)-1)
            traces.append(data[start+shift:stop+shift])

    return starts, traces



"""
def freqComp_trigger(data, signal_length, sampling_rate, corr_min, time_div, bandpass_lower, bandpass_upper, lowpass_freq):
    trace_length = int(signal_length * sampling_rate)

    trigger = tools.butter_bandpass_filter(data, bandpass_lower, bandpass_upper, sampling_rate, 6)
    trigger = np.absolute(trigger)
    trigger = tools.butter_lowpass_filter(trigger, lowpass_freq, sampling_rate, 6)

    average = np.average(trigger)
    trigger_fn = lambda x, y: x > y

    trigger_signal = trigger_fn(trigger, average)
    starts = np.where( (trigger_signal[1:] != trigger_signal[:-1]) * trigger_signal[1:])[0] + 1 


    traces = []
    for start in starts:
        if len(traces) >= time_div:
            break

        stop = start + trace_length
        if stop > len(data):
            break
            
        trace = data[start:stop]

        #Align Traces with a pattern created on the fly
        if len(traces) < 1:
            traces.append(data[start:stop])
            continue
        else:
            template = np.average(traces, axis=0)
            trace_lpf = tools.butter_lowpass_filter(trace, sampling_rate / 4, sampling_rate)
            template_lpf = tools.butter_lowpass_filter(template, sampling_rate / 4, sampling_rate)
            correlation = signal.correlate(trace_lpf**2, template_lpf**2)
            if max(correlation) <= corr_min: 
                continue
            shift = np.argmax(correlation) - (len(template)-1)
            traces.append(data[start+shift:stop+shift])

    return starts, traces
"""


""" For VT
def find_start_with_var(trace, window_size=230):
    trace_extended = list(trace[ -window_size :]) + list(trace)  		#Extend trace before correlation

    var_ = []									#Find the peak in trace = moment were the variation window is at its lowest point
    for start in range(len(trace)):						#    This point will be a reference (beacause always at the same place) among all the traces 
        var_.append( np.std( trace_extended[ start: start+window_size]) )
        #            np.log2(np.std( trace_extended[ i: i+window_size]) )

    return np.argmin(var_)
"""

"""
def pattern_recognition(data, pattern, signal_length, sampling_rate, corr_min, time_div):
    trace_length = int(signal_length * sampling_rate)

    data_lpf = tools.butter_lowpass_filter(data, sampling_rate / 4, sampling_rate)
    pattern_lpf = tools.butter_lowpass_filter(pattern, sampling_rate / 4, sampling_rate)

    trigg = signal.correlate(data_lpf, pattern_lpf)[ len(pattern) : -len(pattern) ]
    trigg_sorted = np.argsort( trigg )[::-1]

    threshold  = max( trigg ) * corr_min
    dist_min   = len( pattern ) / 2
    trigg_segmts = [0]*dist_min + list( trigg ) + [0]*dist_min
    # !!! trigg_segmts = [0]*dist_min + [1]*len( trigg ) + [0]*dist_min

    starts = []
    for trigg_index in trigg_sorted:
        if len(starts) >= time_div:
            break;

        if trigg[ trigg_index ] <= threshold: #corr_min: #threshold:
            break;

        if trigg_segmts[ trigg_index + dist_min ] != 0:
            starts.append( trigg_index )
            # Here instead !!! trigg_segmts[ trigg_index: trigg_index + (dist_min*2) ] = [0]*(dist_min*2)
        trigg_segmts[ trigg_index: trigg_index + (dist_min*2) ] = [0]*(dist_min*2) 
    starts = np.sort( starts )

    traces = []
    for start in starts:
        stop = start + trace_length
        if stop > len(data):
            break
        traces.append(data[start:stop])

    return starts, traces
"""









