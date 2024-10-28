import numpy as np
from matplotlib import pyplot as plt
import argparse
import json


## ARGUMENTS:
parser = argparse.ArgumentParser()
parser.add_argument("--parameters_file", "-p", help="Select the file with parameters", default="config.txt")
args = parser.parse_args()
## END ARGUMENTS


## PARAMETERS:
#Load parameters
parameters_file = str(args.parameters_file)
try:	parameters = json.load(open(parameters_file, "r"))
except:	print(" Could not open config file: %s !"%parameters_file) 
target_freq   		= parameters["collection"]["target_freq"]
nb_traces_attacks      	= parameters["collection"]["nb_traces_attacks"]
result_path		= parameters["analysis"]["result_path"]
res_nb_traces      	= parameters["analysis"]["res_nb_traces"]
## END PARAMETERS

range_nbTrc = list(range( max(3, res_nb_traces), nb_traces_attacks, res_nb_traces )) +  [nb_traces_attacks]


KeyRanks = []
KeyRanks.append( np.load(result_path + "KeyRanks_%d.npy"%target_freq)  )


plt.figure(figsize=(25,14))

plt.axhline(y=0, color='w', linestyle='--', linewidth=3)

"""
plt.plot([0] + range_nbTrc, KeyRanks[0][0], 'k', label=FREQs[0]) 
plt.plot([0] + range_nbTrc, KeyRanks[1][0], 'r', label=FREQs[1]) 
plt.plot([0] + range_nbTrc, KeyRanks[2][0], 'b', label="Comb") 
#plt.plot([0] + range_nbTrc, np.average( KeyRanks[2], axis=0), 'b')
"""

plt.plot([0] + range_nbTrc, np.average( KeyRanks[0], axis=0), 'k', label=target_freq)


plt.axhline(y=39, color='m', linestyle='--', linewidth=3)
plt.axhline(y=35, color='b', linestyle='--', linewidth=3)
plt.axhline(y=32, color='g', linestyle='--', linewidth=3)

plt.legend()
plt.show()


