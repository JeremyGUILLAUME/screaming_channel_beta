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

## ARGUMENTS:
parser = argparse.ArgumentParser()
parser.add_argument("--parameters_file", "-p", help="Select the file with parameters", default="config.txt")
parser.add_argument("--profile", help="Enter the number of profiling traces to collect", default=0)
parser.add_argument("--attack" , help="Enter the number of attack traces to collect", default=0)
parser.add_argument("--plot", help="Select the shift value to aling patterns", default=0)
parser.add_argument("--time_div" , help="Enter the number of attack traces to collect", default=None)
parser.add_argument("--dataset_name" , help="Enter the number of attack traces to collect", default=None)
args = parser.parse_args()
## END ARGUMENTS

#Load parameters
parameters_file = str(args.parameters_file)
try:	parameters = json.load(open(parameters_file, "r"))
except:	print(" Could not open config file: %s !"%parameters_file) 
data_directory     	= parameters["collection"]["data_directory"]
dataset_name    	= parameters["collection"]["dataset_name"] if args.dataset_name == None else str(args.dataset_name)
data_input     		= parameters["collection"]["data_input"]
pattern_name  		= parameters["collection"]["pattern_name"]
USRP_address  		= parameters["collection"]["USRP_address"]
sampling_rate 		= parameters["collection"]["sampling_rate"]
target_freq   		= parameters["collection"]["target_freq"]
implementation		= parameters["collection"]["implementation"]
CP_length     		= parameters["collection"]["CP_length"]
time_div    		= parameters["collection"]["time_div"] if args.time_div == None else int(args.time_div)
nb_traces		= parameters["collection"]["nb_traces"]
## END PARAMETERS

#Configure setup: SDR and Board
drop_start=50e-3
time_div_board = max(10, int(1.2*time_div))
collection_time = CP_length * time_div_board + 0.005
num_samps = int( (drop_start + collection_time) * sampling_rate)

usrp_ 	= uhd.usrp.MultiUSRP()
SDR =  usrp.usrp_init(usrp_, target_freq, sampling_rate)
BOARD 	= pca10040.init_PCA10040(time_div = time_div_board, power=0, plot_=True)



#Load pattern for pattern recognition
if pattern_name != "": pattern = np.load(data_directory+"PATTERNS/"+pattern_name+".npy")
else: pattern = np.load("LIB/src/Patterns/pattern_%d.npy"%target_freq)



#Data input
if not os.path.exists(data_directory+"TRACES/"+dataset_name+"/"): os.makedirs(data_directory+"TRACES/"+dataset_name+"/")
if data_input == "S": 
        plaintexts, key = data.create_static_data(nb_traces)
elif data_input == "R": 
        plaintexts, key = data.create_random_data(nb_traces)
data.save_data(data_directory+"TRACES/"+dataset_name+"/", plaintexts, key)



#Traces dataset collection
pca10040.send_PCA10040_param(BOARD, 'K', key)
with click.progressbar(range(nb_traces)) as bar:
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
                break
                
            if int(args.plot)!=0:
                plt.subplot(2,1,1)
                plt.title("Pattern")
                plt.plot(pattern)
                plt.subplot(2,1,2)
                plt.title("Trace")
                plt.plot(trace)
                plt.show()
            
            np.save(data_directory+"TRACES/"+dataset_name+"/"+ "trace_%d_%d_%d.npy"%(target_freq, time_div, index), trace)

pca10040.close_PCA10040(BOARD)













