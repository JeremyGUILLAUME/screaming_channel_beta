import numpy as np
from matplotlib import pyplot as plt
import argparse
import json
import click
import os, sys

import sca.load as load
import sca.preprocess as preprocess
import sca.classify as classify
import sca.find_pois as find_pois
import sca.profile as profile
import sca.attacks as attacks
import sca.bruteforce as bruteforce



## ARGUMENTS:
parser = argparse.ArgumentParser()
parser.add_argument("--parameters_file", "-p", help="Select the file with parameters", default="config.txt")
parser.add_argument("--profile", help="!= 0 to collect profiling traces", default=0)
parser.add_argument("--plot", help="!= 0 to plot the profiling steps: POIs identification and built profile", default=0)
parser.add_argument("--plot_pges", help="!= 0 to plot the Partial Guessing Entropy (PGEs)", default=0)
parser.add_argument("--bruteforce", help="!= 0 to bruteforce the AES key", default=0)
parser.add_argument("--dataset_name" , help="Enter the name of the trace dataset to collect", default=None)
parser.add_argument("--nb_traces" , help="Enter the number of traces to analyze", default=None)
parser.add_argument("--nb_attacks" , help="Enter the number of attack to realize", default=None)
parser.add_argument("--time_div" , help="Enter the time diversity order of the collected traces", default=None)
args = parser.parse_args()
## END ARGUMENTS



## PARAMETERS:
parameters_file = str(args.parameters_file)
try:	parameters = json.load(open(parameters_file, "r"))
except:	
    print(" Could not open parameters file: %s !"%parameters_file)
    sys.exit() 
data_directory     	= parameters["collection"]["data_directory"]
dataset_name    	= parameters["collection"]["dataset_name"] 	if args.dataset_name == None else str(args.dataset_name)
nb_traces		= parameters["collection"]["nb_traces"]		if args.nb_traces == None else int(args.nb_traces)
time_div    		= parameters["collection"]["time_div"] 		if args.time_div == None else int(args.time_div)

sampling_rate 		= parameters["collection"]["sampling_rate"]
target_freq   		= parameters["collection"]["target_freq"]
CP_length     		= parameters["collection"]["CP_length"]

profile_name      	= parameters["analysis"]["profile_name"]
variable      		= parameters["analysis"]["variable"]
nb_attacks      	= parameters["analysis"]["nb_attacks"]		if args.nb_attacks == None else int(args.nb_attacks)
res_nb_traces      	= parameters["analysis"]["res_nb_traces"]
cutoff      		= parameters["analysis"]["cutoff"]
SOI_start     		= parameters["analysis"]["SOI_start"]
SOI_stop      		= parameters["analysis"]["SOI_stop"]
## END PARAMETERS

if not os.path.exists(data_directory):
    print("Directory: %s does not exist !"%data_directory )
    sys.exit()


nb_traces_attacks = nb_traces // nb_attacks
if SOI_stop==None: SOI_stop = int(CP_length*sampling_rate)
range_nbTraces = list(range( max(3, res_nb_traces), nb_traces_attacks, res_nb_traces )) +  [nb_traces_attacks]



if args.profile!=0:
        plaintexts, key, traces = load.load_all( data_directory+"TRACES/"+dataset_name+"/", "plaintexts", "key", "trace_%d_%d"%(target_freq, time_div), nb_traces)
        traces = preprocess.preprocess_traces(traces, SOI_start=SOI_start, SOI_stop=SOI_stop, cutoff=cutoff, sampling_rate=sampling_rate, order=5)

        SETS, CLASSES = classify.classify(traces, plaintexts, key, variable)
        POIS = find_pois.find_pois(SETS, CLASSES, int(args.time_div)!=0 )
        PROFILE = profile.build_profile(SETS, CLASSES, POIS)
        if int(args.time_div)!=0: profile.plot_profile(PROFILE)
        if not os.path.exists(data_directory+"PROFILES/"): os.makedirs(data_directory+"PROFILES/")
        profile.save_profile(data_directory+"PROFILES/"+profile_name, PROFILE)


else: 
        if not os.path.exists(data_directory+"LOGs/"): os.makedirs(data_directory+"LOGs/")
        if not os.path.exists(data_directory+"KRs/"):  os.makedirs(data_directory+"KRs/")
        KeyRanks = []
        LOG_PROBAs = []

        if profile_name != "": PROFILE = profile.load_profile(data_directory+"PROFILES/"+profile_name)
        else: 
            PROFILE = profile.load_profile("LIB/src/Profiles/PROFILE_%d"%target_freq)
            SOI_start = 1000
            SOI_stop  = 1500
            
        plaintexts, key, traces = load.load_all(data_directory+"TRACES/"+dataset_name+"/", "plaintexts", "key", "trace_%d_%d"%(target_freq, time_div), nb_traces)
        traces = preprocess.preprocess_traces(traces, SOI_start=SOI_start, SOI_stop=SOI_stop, cutoff=cutoff, sampling_rate=sampling_rate, order=5)

        for attck in range(nb_attacks):

            start = attck * nb_traces_attacks
            stop  = start + nb_traces_attacks
            LOG_PROBAs.append(attacks.profiled_corr_attack(traces[start:stop], plaintexts[start:stop], PROFILE, range_nbTrc=range_nbTraces, variable=variable))
            KeyRanks.append( [128] + [bruteforce.complexity(plaintexts, key, LOG_PROBAs[-1][i]) for i in range(len(LOG_PROBAs[-1]))] )
            
            if int(args.plot_pges)!=0: 
                attacks.print_pges(key, LOG_PROBAs[-1][-1])
                attacks.print_stats(key, LOG_PROBAs[-1][-1])
            if int(args.bruteforce)!=0: bruteforce.attack(plaintexts, key, LOG_PROBAs[-1][-1], bit_bound_end=int(args.bruteforce))
            
        np.save(data_directory+"LOGs/LOG_PROBAs_%s_%dattacks"%(dataset_name,nb_attacks), LOG_PROBAs)
        np.save(data_directory+"KRs/KeyRanks_%s_%dattacks"%(dataset_name,nb_attacks), KeyRanks)
        







