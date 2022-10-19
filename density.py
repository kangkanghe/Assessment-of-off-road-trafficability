import numpy as np
import os

# 1.计算植被、水体、建筑、湿地的密集性；植被(9,10)、水体(79,80)、建筑物（49,50）湿地（89,90），低值表示稀疏、高值表示密集;
def density(data, var_data, var_num, name):
    if os.path.isfile(name):
        data = np.load(name)
    else:
        for i in var_data:
                var1 = np.array([var_data[i][0],var_data[i][1]]).transpose()
                for j in var1:
                    try:
                        var2 = data[j[0] - 1:j[0] + 2, j[1] - 1:j[1] + 2]
                        if (np.size(np.where(var2 == var_num[i])[0]) + np.size(np.where(var2 == var_num[i]-1)[0])) <= 3:
                            data[j[0], j[1]] = var_num[i]-1
                    except:
                        continue
        np.save(name, data)
    return data