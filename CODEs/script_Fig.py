import numpy as np
from matplotlib import pyplot as plt
import argparse
import json
import os, sys


## ARGUMENTS:
parser = argparse.ArgumentParser()
parser.add_argument("--parameters_file", "-p", help="Select the file with parameters", default="config.txt")
args = parser.parse_args()
## END ARGUMENTS


## PARAMETERS:
parameters_file = str(args.parameters_file)
try:	parameters = json.load(open(parameters_file, "r"))
except:	
    print(" Could not open parameters file: %s !"%parameters_file) 
    sys.exit()
data_directory     	= parameters["collection"]["data_directory"]
dataset_name    	= parameters["collection"]["dataset_name"] 
target_freq   		= parameters["collection"]["target_freq"]
nb_traces		= parameters["collection"]["nb_traces"]

res_nb_traces      	= parameters["analysis"]["res_nb_traces"]
nb_attacks      	= parameters["analysis"]["nb_attacks"]
## END PARAMETERS

if not os.path.exists(data_directory): 
    print("Directory: %s does not exist !"%data_directory )
    sys.exit()

nb_traces_attacks = nb_traces // nb_attacks
range_nbTraces = list(range( max(3, res_nb_traces), nb_traces_attacks, res_nb_traces )) +  [nb_traces_attacks]


KeyRanks = []
KeyRanks.append( np.load(data_directory+"KRs/KeyRanks_%s_%dattacks.npy"%(dataset_name,nb_attacks))   )

labelsize = 30
tickssize = 25

fig = plt.figure(figsize=(25,14))
ax = fig.add_subplot(111)
ax.set_xlabel("Number of traces", size=labelsize)
ax.set_ylabel("GE = Log2(Key Rank)", size=labelsize)

ax.set(xlim=(0, nb_traces_attacks+1), xticks=range(0, nb_traces_attacks+1, nb_traces_attacks//5),
       ylim=(0, 129), yticks=range(0,129, 16))
ax.tick_params(labelsize=tickssize)


plt.plot([0] + range_nbTraces, np.average( KeyRanks[0], axis=0), 'k', label=str(target_freq)+" Hz")

plt.axhline(y=39, color='m', linestyle='--', linewidth=3, label="GE = 39")
plt.axhline(y=35, color='b', linestyle='--', linewidth=3, label="GE = 35")
plt.axhline(y=32, color='g', linestyle='--', linewidth=3, label="GE = 32")

plt.legend(loc="upper right")

if not os.path.exists(data_directory+"FIGs/"): os.makedirs(data_directory+"FIGs/")
plt.savefig(data_directory+"FIGs/GEs_%s_%dattacks"%(dataset_name,nb_attacks), bbox_inches='tight')


plt.show()
