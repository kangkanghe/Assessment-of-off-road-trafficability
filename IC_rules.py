import numpy as np

def IC_rules(rules, data_label):
    # rules = np.delete(rules, np.s_[np.where(np.all(rules[:, :] == np.zeros((1,10)), axis=1))[0][0]:], axis=0)
    rules_IC = np.zeros((np.shape(rules)[0],1))
    i = 0
    for x in rules:
        for y, element in enumerate(data_label):
            if y == 5 and x[y] == 7:
                rules_IC[i] = rules_IC[i] + x[y] * data_label[element]['weight'][1]
            else:
                rules_IC[i] = rules_IC[i] + x[y] * data_label[element]['weight'][0]
        i += 1

    return rules_IC
