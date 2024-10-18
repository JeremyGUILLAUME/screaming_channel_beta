import numpy as np
from matplotlib import pyplot as plt

def saturation(raw, s):
    if raw < s:
        return raw
    else:
        return s


def plot_pge(seuil, pges_1, pges_2, pges_3, pges_4, title_1="", title_2="", title_3="", title_4="", data_path="", name_fig="", num_key_bytes=16):
    text_size = 22
    label_size = 14
    s = seuil
    length = len(pges_1)

    RESULT_1 = np.zeros((num_key_bytes,length))
    RESULT_2 = np.zeros((num_key_bytes,length))
    RESULT_3 = np.zeros((num_key_bytes,length))
    RESULT_4 = np.zeros((num_key_bytes,length))

    for i in range(length):
        for b in range(num_key_bytes):
            RESULT_1[b][i] = saturation( pges_1[i][b] , s)
            RESULT_2[b][i] = saturation( pges_2[i][b] , s)
            RESULT_3[b][i] = saturation( pges_3[i][b] , s)
            RESULT_4[b][i] = saturation( pges_4[i][b] , s)

    RESULT_1[num_key_bytes-1][0] = 0
    RESULT_1[num_key_bytes-1][1] = s
    RESULT_2[num_key_bytes-1][0] = 0
    RESULT_2[num_key_bytes-1][1] = s 
    RESULT_3[num_key_bytes-1][0] = 0
    RESULT_3[num_key_bytes-1][1] = s 
    RESULT_4[num_key_bytes-1][0] = 0
    RESULT_4[num_key_bytes-1][1] = s 

    fig, ax = plt.subplots(2,2, figsize=(14,9))

    legende_tab = [range(s+1)]
    legende_color = ax[0][0].pcolor(legende_tab, cmap= 'coolwarm')#RdYlBu
    cbar = fig.colorbar(legende_color, ax=ax.ravel().tolist(), ticks=range(s+1))
    cbar.ax.tick_params(labelsize=label_size+2)


    result_c = ax[0][0].pcolor(RESULT_1, cmap= 'coolwarm')#RdYlBu
    ax[0][0].tick_params(labelsize=label_size)

    result_c = ax[0][1].pcolor(RESULT_2, cmap= 'coolwarm')#RdYlBu
    ax[0][1].tick_params(labelsize=label_size)

    result_1 = ax[1][0].pcolor(RESULT_3, cmap= 'coolwarm')#RdYlBu
    ax[1][0].tick_params(labelsize=label_size) 

    result_1 = ax[1][1].pcolor(RESULT_4, cmap= 'coolwarm')#RdYlBu
    ax[1][1].tick_params(labelsize=label_size) 

    text_size = 20
    ax[0][0].set_xlabel('%s'%title_1, size=text_size)
    ax[0][1].set_xlabel('%s'%title_2, size=text_size)
    ax[1][0].set_xlabel('%s'%title_3, size=text_size)
    ax[1][1].set_xlabel('%s'%title_4, size=text_size)

    #ax[2][0].set_xlabel('Frequency trigger mechanism', size=text_size)
    #ax[2][1].set_xlabel('Our proposal', size=text_size)

    plt.savefig(data_path + "%s"%name_fig, bbox_inches='tight')

    plt.show()

