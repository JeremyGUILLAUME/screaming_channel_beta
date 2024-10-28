import numpy as np
from matplotlib import pyplot as plt
import argparse
import json
import click
import os

import sca.load as load
import sca.preprocess as preprocess
import sca.classify as classify
import sca.find_pois as find_pois
import sca.profile_ as profile_
import sca.attacks as attacks
import sca.bruteforce as bruteforce

import sca.filters as filters
def preprocess_traces(TRACES, SOI_start=1000, SOI_stop=1150, cutoff=550e3, sampling_rate=5e6, order=5):
    traces = []
    for i in range(len(TRACES)):
        try:
            traces.append( filters.butter_lowpass_filter( TRACES[i], cutoff, sampling_rate, order)[SOI_start : SOI_stop] )
        except:
            print(i)
    return traces

## ARGUMENTS:
parser = argparse.ArgumentParser()
parser.add_argument("--parameters_file", "-p", help="Select the file with parameters", default="config.txt")
parser.add_argument("--profile", help="Enter the number of profiling traces to collect", default=False)
parser.add_argument("--plot", help="Select the shift value to aling patterns", default=False)
parser.add_argument("--save", help="Select the shift value to aling patterns", default=False)
args = parser.parse_args()
## END ARGUMENTS


## PARAMETERS:
#Default parameters
"""
{
    "collection" : {
        "data_path" : "data/",
        "pattern_name" : "pattern.npy",
        "USRP_address" : "192.168.10.109",
        "target_freq" : 2.528e9,
        "sampling_rate" : 5e6,
        "implementation" : "S",
        "CP_length" : 894.416e-6,
        "trace_name" : "trace",
        "time_div" : 10
        },

    "analysis": {
        "nb_traces_profile" : 5000,
        "nb_traces_attacks" : 1500,
        "nb_attacks" 	    : 1
}	}
"""

#Load parameters
parameters_file = str(args.parameters_file)
try:	parameters = json.load(open(parameters_file, "r"))
except:	print(" Could not open config file: %s !"%parameters_file) 
data_directory     	= parameters["collection"]["data_directory"]
dataset_name    	= parameters["collection"]["dataset_name"] 
data_input     		= parameters["collection"]["data_input"]
pattern_name  		= parameters["collection"]["pattern_name"]
USRP_address  		= parameters["collection"]["USRP_address"]
sampling_rate 		= parameters["collection"]["sampling_rate"]
target_freq   		= parameters["collection"]["target_freq"]
implementation		= parameters["collection"]["implementation"]
CP_length     		= parameters["collection"]["CP_length"]
time_div    		= parameters["collection"]["time_div"] 
nb_traces		= parameters["collection"]["nb_traces"]

res_nb_traces      	= parameters["analysis"]["res_nb_traces"]
profile_name      	= parameters["analysis"]["profile_name"]
save_name	      	= parameters["analysis"]["save_name"]
SOI_start     		= parameters["analysis"]["SOI_start"]
SOI_stop      		= parameters["analysis"]["SOI_stop"]
cutoff      		= parameters["analysis"]["cutoff"]
variable      		= parameters["analysis"]["variable"]
nb_attacks      	= parameters["analysis"]["nb_attacks"]
## END PARAMETERS


nb_traces_attacks = nb_traces // nb_attacks

FREQs = target_freq
if SOI_stop==None: SOI_stop = int(CP_length*sampling_rate)
range_nbTrc = list(range( max(3, res_nb_traces), nb_traces_attacks, res_nb_traces )) +  [nb_traces_attacks]


phase = "attack" if args.profile==False else "profile"


if phase == "profile":
        plaintexts, key, traces = load.load_all( data_path + phase + "/", "plaintext", "key", "%s_%d"%(trace_name, target_freq), nb_traces_profile)
        traces = preprocess.preprocess_traces(traces, SOI_start=SOI_start, SOI_stop=SOI_stop, cutoff=cutoff, sampling_rate=sampling_rate, order=5)

        SETS, CLASSES = classify.classify(traces, plaintexts, key, variable)
        POIS = find_pois.find_pois(SETS, CLASSES, False) 
        PROFILE = profile_.build_profile(SETS, CLASSES, POIS)
        profile_.save_profile("DATA/" + profile_name + "%dMHz"%target_freq, PROFILE)




elif phase == "attack": 
        if not os.path.exists(data_directory+"LOGs/"): os.makedirs(data_directory+"LOGs/") 
        if not os.path.exists(data_directory+"KRs/"): os.makedirs(data_directory+"KRs/") 
        KeyRanks = []
        LOG_PROBAs = []
        plaintexts, key, traces = load.load_all( data_directory+"TRACES/"+dataset_name+"/", "plaintext", "key", "trace_%d_%d"%(target_freq, time_div), nb_traces)

        traces = preprocess_traces(traces, SOI_start=SOI_start, SOI_stop=SOI_stop, cutoff=cutoff, sampling_rate=sampling_rate, order=5)
	
        #PROFILE = profile_.load_profile("DATA/" + profile_name+ "%dMHz"%target_freq)
        if profile_name != "": PROFILE = profile_.load_profile(data_directory+"PROFILES/"+profile_name) 
        else: PROFILE = profile_.load_profile("LIB/src/Profiles/PROFILE_%d"%target_freq)

        for attck in range(nb_attacks):

            start = attck * nb_traces_attacks
            stop  = start + nb_traces_attacks
            LOG_PROBAs.append(attacks.profiled_corr_attack(traces[start:stop], plaintexts[start:stop], PROFILE, range_nbTrc=range_nbTrc, variable=variable))
            KeyRanks.append( [128] + [bruteforce.complexity(plaintexts, key, LOG_PROBAs[-1][i]) for i in range(len(LOG_PROBAs[-1]))] )  

        np.save(data_directory+"LOGs/LOG_PROBAs_%d"%target_freq, LOG_PROBAs) 
        np.save(data_directory+"KRs/KeyRanks_%d"%target_freq, KeyRanks) 

#plt.plot(traces[-1])
#plt.show()
