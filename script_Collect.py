import numpy as np
from matplotlib import pyplot as plt
import argparse
import json
import os
import time
import click

import uhd
import sca.USRP as usrp
import sca.PCA10040 as pca10040
import sca.data as data
import sca.extraction as extraction
import sca.extract_methods as extract_methods
import sca.preprocess as preprocess

## ARGUMENTS:
parser = argparse.ArgumentParser()
parser.add_argument("--parameters_file", "-p", help="Select the file with parameters", default="config.txt")
parser.add_argument("--profile", help="Enter the number of profiling traces to collect", default=0)
parser.add_argument("--attack" , help="Enter the number of attack traces to collect", default=0)
parser.add_argument("--plot", help="Select the shift value to aling patterns", default=False)
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
data_path     		= parameters["collection"]["data_path"]
pattern_name  		= parameters["collection"]["pattern_name"]
USRP_address  		= parameters["collection"]["USRP_address"]
sampling_rate 		= parameters["collection"]["sampling_rate"]
target_freq   		= parameters["collection"]["target_freq"]
implementation		= parameters["collection"]["implementation"]
CP_length     		= parameters["collection"]["CP_length"]
trace_name    		= parameters["collection"]["trace_name"]
time_div      		= parameters["collection"]["time_div"]
nb_traces_profile	= parameters["collection"]["nb_traces_profile"]
nb_traces_attacks      	= parameters["collection"]["nb_traces_attacks"]
nb_attacks      	= parameters["collection"]["nb_attacks"]
## END PARAMETERS


multiplier = 1.2

drop_start=50e-3
collection_time = CP_length * int(time_div*multiplier) + 0.005
num_samps = int( (drop_start + collection_time) * sampling_rate)
print(num_samps)

FREQs = target_freq

usrp_ 	= uhd.usrp.MultiUSRP()
SDR =  usrp.usrp_init(usrp_, (2000 + target_freq)*1e6, sampling_rate)

#BOARD 	= pca10040.init_PCA10040(time_div = int(time_div*1.2), power=0, plot_=True)
BOARD 	= pca10040.init_PCA10040(time_div = int(time_div*multiplier), power=0, plot_=True)

pattern = np.load(pattern_name + "%d.npy"%target_freq)

phases = []
if args.profile!=False: phases.append("profile")
if args.attack!=False: phases.append("attack")

for phase in phases:
    if phase == "profile": 
        num_traces = nb_traces_profile
        plaintexts, key = data.create_static_data(num_traces)
    elif phase == "attack": 
        num_traces = nb_attacks * nb_traces_attacks
        plaintexts, key = data.create_random_data(num_traces)
    if not os.path.exists(data_path+phase+"/"): os.makedirs(data_path+phase+"/")
    data.save_data(data_path+phase+"/", plaintexts, key)

    pca10040.send_PCA10040_param(BOARD, 'K', key)

    with click.progressbar(range(num_traces)) as bar:
        for index in bar:
            pca10040.send_PCA10040_param(BOARD, 'P', plaintexts[index])

            while True:
                usrp.usrp_start(SDR)
                time.sleep(drop_start)
                BOARD.write(str(implementation).encode())
                time.sleep(collection_time)
                usrp.usrp_stop(SDR)

                rawTrace = usrp.usrp_get_data(SDR, num_samps, int(drop_start * sampling_rate) )
		
                trace = extraction.extract_trace(rawTrace, CP_length, "pattern_recognition", time_div=time_div, pattern=pattern, sampling_rate=sampling_rate)
                #trace = extraction.extract_trace(rawTrace, CP_length, "virtual_trigger", time_div=time_div, sampling_rate=sampling_rate)
                """
                starts, traces = extract_methods.pattern_recognition(rawTrace, pattern=pattern, signal_length=CP_length, sampling_rate=sampling_rate, corr_min=0.6, time_div=time_div)
                print(np.shape(starts))
                print(np.shape(traces))
                #trace = np.average(traces, axis=0)
                trace = traces[0]
                print(np.shape(trace))
                trace = preprocess.normalize_trace(trace)
                """
                break
                
            if int(args.plot)==1:
                plt.subplot(2,1,1)
                plt.plot(pattern)
                plt.subplot(2,1,2)
                plt.plot(trace)
                plt.show()
            
            np.save(data_path+phase+"/"+ "%s_%d_%d.npy"%(trace_name, target_freq, index), trace)

pca10040.close_PCA10040(BOARD)


