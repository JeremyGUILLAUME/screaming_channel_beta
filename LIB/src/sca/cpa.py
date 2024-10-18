
"""
def cpa(traces, p, variable="LSB")


by = 0
snrs = []
for h in range(256):
    k = [h for i in range(16)]
    IV, CLASSES = model.model(traces, p, k, variable="hw_p_xor_k") #hw_p_xor_k   #LSB
    SETS = classify.classify(traces, IV, CLASSES)

    var_C = []
    for cl in range(len(CLASSES)):
        var_C.append(np.var(SETS[by][CLASSES[cl]], axis=0) )
    mean_vars = np.average(var_C, axis = 0)

    mean_C = []
    for cl in range(len(CLASSES)):
        mean_C.append(np.average(SETS[by][CLASSES[cl]], axis=0) )
    var_means = np.var(mean_C, axis = 0)

    snrs.append(max(var_means / mean_vars))
    plt.plot(var_means / mean_vars)
    #print np.argmax(var_means / mean_vars)
    #print "%3d: %f"%(h, var_means[588] / mean_vars[588])
plt.show()

print np.argmax(snrs)
"""
