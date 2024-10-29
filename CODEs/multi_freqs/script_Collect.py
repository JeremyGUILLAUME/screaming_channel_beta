import numpy as np
from matplotlib import pyplot as plt
import argparse
import json
import os, sys
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
parser.add_argument("--plot", help="!= 0 to plot the pattern and the collected trace", default=0)
parser.add_argument("--dataset_name" , help="Enter the name of the trace dataset to collect", default=None)
parser.add_argument("--data_input" , help="Enter the type of input plaintexts (Standart or Random)", default=None)
parser.add_argument("--nb_traces" , help="Enter the number of traces to collect", default=None)
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
data_input     		= parameters["collection"]["data_input"] 	if args.data_input == None else str(args.data_input)
nb_traces		= parameters["collection"]["nb_traces"] 	if args.nb_traces == None else int(args.nb_traces)
time_div    		= parameters["collection"]["time_div"] 		if args.time_div == None else int(args.time_div)

USRP_address  		= parameters["collection"]["USRP_address"]
sampling_rate 		= parameters["collection"]["sampling_rate"]
target_freq   		= parameters["collection"]["target_freq"]
implementation		= parameters["collection"]["implementation"]
CP_length     		= parameters["collection"]["CP_length"]
pattern_name  		= parameters["collection"]["pattern_name"]
## END PARAMETERS



if not os.path.exists(data_directory): 
    print("Directory: %s does not exist !"%data_directory )
    sys.exit()



#Configure setup: SDR and Board
time_div_board = max(10, int(1.2*time_div))
drop_start=50e-3 #Time for the SDR to start the collection properly
collection_time = CP_length * time_div_board + 0.005
num_samps = int( (drop_start + collection_time) * sampling_rate)

usrp_1 = uhd.usrp.MultiUSRP("addr="+USRP_address[0])
usrp_2 = uhd.usrp.MultiUSRP("addr="+USRP_address[1])
SDR_1     = usrp.usrp_init(usrp_1, target_freq[0], sampling_rate)
SDR_2     = usrp.usrp_init(usrp_2, target_freq[1], sampling_rate)
BOARD 	= pca10040.init_PCA10040(time_div = time_div_board, power=0, plot_=True)



#Load pattern for pattern recognition
if pattern_name[0] != "": pattern_1 = np.load(data_directory+"PATTERNS/"+pattern_name[0]+".npy")
else: pattern_1 = np.load("LIB/src/Patterns/pattern_%d.npy"%target_freq[0])
if pattern_name[1] != "": pattern_2 = np.load(data_directory+"PATTERNS/"+pattern_name[1]+".npy")
else: pattern_2 = np.load("LIB/src/Patterns/pattern_%d.npy"%target_freq[1])



#Data input
if not os.path.exists(data_directory+"TRACES/"+dataset_name+"/"): os.makedirs(data_directory+"TRACES/"+dataset_name+"/")
if   data_input == "S":	plaintexts, key = data.create_static_data(nb_traces)
elif data_input == "R": plaintexts, key = data.create_random_data(nb_traces)
data.save_data(data_directory+"TRACES/"+dataset_name+"/", plaintexts, key)



#Traces dataset collection
pca10040.send_PCA10040_param(BOARD, 'K', key)
with click.progressbar(range(nb_traces)) as bar:
        for index in bar:
            pca10040.send_PCA10040_param(BOARD, 'P', plaintexts[index])

            while True:
                usrp.usrp_start(SDR_1)
                usrp.usrp_start(SDR_2)
                time.sleep(drop_start)
                BOARD.write(str(implementation).encode())
                time.sleep(collection_time)
                usrp.usrp_stop(SDR_1)
                usrp.usrp_stop(SDR_2)

                rawTrace_1 = usrp.usrp_get_data(SDR_1, num_samps, int(drop_start * sampling_rate) )
                rawTrace_2 = usrp.usrp_get_data(SDR_2, num_samps, int(drop_start * sampling_rate) )
                trace_1 = extraction.extract_trace(rawTrace_1, CP_length, "pattern_recognition", time_div=time_div, pattern=pattern_1, sampling_rate=sampling_rate)
                trace_2 = extraction.extract_trace(rawTrace_2, CP_length, "pattern_recognition", time_div=time_div, pattern=pattern_2, sampling_rate=sampling_rate)
                break
                
            if int(args.plot)!=0:
                plt.subplot(3,1,1)
                plt.title("Pattern")
                plt.plot(pattern)
                plt.subplot(3,1,2)
                plt.title("Trace 1")
                plt.plot(trace_1)
                plt.subplot(3,1,3)
                plt.title("Trace 2")
                plt.plot(trace_2)
                plt.show()
            
            np.save(data_directory+"TRACES/"+dataset_name+"/"+ "trace_%d_%d_%d.npy"%(target_freq[0], time_div, index), trace_1)
            np.save(data_directory+"TRACES/"+dataset_name+"/"+ "trace_%d_%d_%d.npy"%(target_freq[1], time_div, index), trace_2)

pca10040.close_PCA10040(BOARD)













