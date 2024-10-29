import ast
import numpy as np
import matplotlib.pyplot as plt



def build_profile(SETS, CLASSES, POIS, num_key_bytes=16):
    PROFILE = []
    for byt in range(num_key_bytes):

        PROFILE.append({})
        PROFILE[byt][-1] = POIS[byt]

        for cls, index in zip(CLASSES[byt], range(len(CLASSES[byt]))):
            PROFILE[byt][cls] = np.average(SETS[byt][index],axis=0)[POIS[byt]]

    return PROFILE



def save_profile(save_file, PROFILE):
    save_file = open(save_file + ".txt","w")
    save_file.write(str(PROFILE))
    save_file.close()



def load_profile(load_file):
    with open(load_file + '.txt') as f:
        data = f.read()
    PROFILE = ast.literal_eval(data)
    return PROFILE



def plot_profile(PROFILE, num_key_bytes=16, save=False, title=""):
    for byt in range(num_key_bytes):
        x = []
        y = []
        for i in range(256):
            if i in PROFILE[byt]:
                x.append(i)
                y.append(PROFILE[byt][i])
        plt.plot(x, y)

    if save != False:
        data_path = save
        plt.savefig(data_path + 'Profile_%s'%title, bbox_inches='tight')

    plt.show()
