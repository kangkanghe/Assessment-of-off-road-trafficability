import numpy as np
import os

def traff_relus(data_IC, data_label, relus_name):
    if os.path.isfile(relus_name):
        rules = np.load(relus_name)
        rules = np.delete(rules, np.s_[np.where(np.all(rules[:, :] == np.zeros((1, 10)), axis=1))[0][0]:], axis=0)
    else:
        # 计算通行规则
        rules_num = 1
        # 计算有多少种通行规则
        for rule_num in data_label:
            rules_num = rules_num * data_label[rule_num]['类别']

        # 转换data_IC为三维，运算速度快
        data = np.zeros((np.shape(data_IC['land_IC'])[0], np.shape(data_IC['land_IC'])[1], len(data_label)))
        for j, element in enumerate(data_IC):
            data[:, :, j] = data_IC[element]

        # 存储通行规则
        rules = np.zeros((rules_num, len(data_label)))
        # 遍历图像，得到通行规则
        i = 0
        for x in range(np.shape(data_IC['land_IC'])[0]):
            for y in range(np.shape(data_IC['land_IC'])[1]):
                # 判断是否为新的通行规则
                if not np.any(np.where(np.all(rules[:, :] == data[x, y, :], axis=1))):
                    rules[i, :] = data[x, y, :]
                    i += 1
        np.delete(rules, np.s_[i-1:], axis=0) #删除多余的0行
        np.save(relus_name, rules)
    return rules