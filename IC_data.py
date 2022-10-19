import os
import pandas as pd
import numpy as np
from osgeo import gdal,osr
import argparse
import os
from AHP_weight import AHP_weight
from record_tif import record_tif
from density import density
from load_tif import load_tif
from dataset import dataset
from factor_num import factor_num
import jenkspy
def IC_data(*args):
    if len(args) == 3:
        data_all = args[0]
        data_IC = args[1]
        data_label = args[2]
        IC = np.zeros(np.shape(data_all['land_data']))
        for i in zip(data_IC, data_label, data_all):
            if np.size(data_label[i[1]]['weight']) > 1:
                data_IC[i[0]][np.where(data_all[i[2]] < -998)] = 0
                data_IC[i[0]][np.where((data_IC[i[0]] == 8) | (data_IC[i[0]] == 4) | (data_IC[i[0]] == 5))] = data_IC[i[0]][np.where((data_IC[i[0]] == 8) | (data_IC[i[0]] == 4) | (data_IC[i[0]] == 5))] * data_label[i[1]]['weight'][0]
                data_IC[i[0]][np.where(data_IC[i[0]] == 7)] = data_IC[i[0]][np.where(data_IC[i[0]] == 7)] * data_label[i[1]]['weight'][1]
            else:
                data_IC[i[0]][np.where(data_all[i[2]] < -998)] = 0
                data_IC[i[0]][np.where(data_all[i[2]] > -999)] = data_IC[i[0]][np.where(data_all[i[2]] > -999)] * data_label[i[1]]['weight']
            IC = IC + data_IC[i[0]]
    elif len(args) == 4:
        data_all = args[0]
        data_IC = args[1]
        data_label = args[2]
        Traffic_levels = args[3]

        IC = np.zeros(np.shape(data_all['land_data']))
        for i in zip(data_IC, data_label, data_all):
            if np.size(data_label[i[1]]['weight']) > 1:
                data_IC[i[0]][np.where(data_all[i[2]] < -998)] = 0
                data_IC[i[0]][np.where((data_IC[i[0]] == 8) | (data_IC[i[0]] == 4) | (data_IC[i[0]] == 5))] = data_IC[i[0]][np.where((data_IC[i[0]] == 8) | (data_IC[i[0]] == 4) | (data_IC[i[0]] == 5))] * data_label[i[1]]['weight'][0]
                data_IC[i[0]][np.where(data_IC[i[0]] == 7)] = data_IC[i[0]][np.where(data_IC[i[0]] == 7)] * data_label[i[1]]['weight'][1]
            else:
                data_IC[i[0]][np.where(data_all[i[2]] < -998)] = 0
                data_IC[i[0]][np.where(data_all[i[2]] > -999)] = data_IC[i[0]][np.where(data_all[i[2]] > -999)] * data_label[i[1]]['weight']
            IC = IC + data_IC[i[0]]

        Capacity_map = np.zeros(np.shape(IC))
        proportion = np.zeros((len(Traffic_levels)-1, 2))

        for i in range(len(Traffic_levels)-1):
            Capacity_map[np.where((IC >= Traffic_levels[i]) & (IC <= Traffic_levels[i+1]))] = len(Traffic_levels)-1-i
            proportion[len(Traffic_levels)-2-i,:] = [len(np.where(Capacity_map == len(Traffic_levels)-1-i)[0])/np.size(IC),len(Traffic_levels)-1-i]
    return IC, Capacity_map, proportion