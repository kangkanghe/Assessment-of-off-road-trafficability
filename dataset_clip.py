import os
import pandas as pd
import numpy as np
from osgeo import gdal,osr
import argparse
import os
import AHP_weight
import record_tif
import density
import jenkspy
from load_tif import load_tif

def dataset_clip(args, RCI_data_name):
    # -999用来替换无效栅格
    hazard_data = load_tif(args.input_地质灾害)[0]

    DEM_data = load_tif(args.input_DEM)[0]
    DEM_data[np.where((DEM_data > -999) & (DEM_data < 2000))] = 1
    DEM_data[np.where(DEM_data >= 2000)] = 2

    # disaster_data = load_tif(args.input_地质灾害)

    land_data = load_tif(args.input_土地利用)[0]
    land_data[np.where((land_data == 10) | (land_data == 20) | (land_data == 95))] = 10  # 林地、灌木、红树林合并为林地，总共7类

    # 岩体、土体总共12类
    rocksoil_data, px_rocksoil, py_rocksoil = load_tif(args.input_rocksoil)
    rocksoil_data[np.where((rocksoil_data == 4))] = -999
    rocksoil_data[np.where((rocksoil_data >= 5))] = 4

    struct_data = load_tif(args.input_节理构造)[0]

    twi_data = load_tif(args.input_湿度)[0]

    if os.path.isfile(RCI_data_name):
        RCI_data = np.load(RCI_data_name)
    else:
        RCI_data = load_tif(args.input_rocksoil)[0]
        RCI_data[np.where((RCI_data >= 4))] = -999
        factor = np.where(RCI_data > 0)
        for i in range(np.shape(factor)[1]):
            count = (factor[0][i], factor[1][i])
            if RCI_data[count] == 1:
                if twi_data[count] >= -998 and twi_data[count] < -9.646480643:
                    RCI_data[count] = 126
                elif twi_data[count] >= -9.646480643 and twi_data[count] < -1.20733932:
                    RCI_data[count] = 86
                elif twi_data[count] >= -1.20733932 and twi_data[count] < 100:
                    RCI_data[count] = 46
                elif twi_data[count] == -999:
                    RCI_data[count] = -999
            elif RCI_data[count] == 2:
                if twi_data[count] >= -998 and twi_data[count] < -9.646480643:
                    RCI_data[count] = 145
                elif twi_data[count] >= -9.646480643 and twi_data[count] < -1.20733932:
                    RCI_data[count] = 109
                elif twi_data[count] >= -1.20733932 and twi_data[count] < 100:
                    RCI_data[count] = 73
                elif twi_data[count] == -999:
                    RCI_data[count] = -999
            elif RCI_data[count] == 3:
                if twi_data[count] >= -998 and twi_data[count] < -9.646480643:
                    RCI_data[count] = 111
                elif twi_data[count] >= -9.646480643 and twi_data[count] < -1.20733932:
                    RCI_data[count] = 57
                elif twi_data[count] >= -1.20733932 and twi_data[count] < 100:
                    RCI_data[count] = 3
                elif twi_data[count] == -999:
                    RCI_data[count] = -999
        np.save(RCI_data_name, RCI_data)
        RCI_data = np.load(RCI_data_name)

    spi_data = load_tif(args.input_水流力指数)[0]

    slope_data = load_tif(args.input_slope)[0]
    slope_label = {'类别': 6, 'value': [7, 14, 21, 28, 35]}

    tpi_data = load_tif(args.input_坡位指数)[0]
    tpi_label = {'类别': 3, 'value': [-24.23928462, 29.17278454]}

    px, py = np.meshgrid(px_rocksoil, py_rocksoil)

    data_all = {'hazard_data': hazard_data, 'slope_data': slope_data, 'land_data': land_data, 'twi_data': twi_data, 'RCI_data': RCI_data, 'rocksoil_data': rocksoil_data, 'tpi_data': tpi_data, 'struct_data': struct_data, 'spi_data': spi_data, 'DEM_data': DEM_data}
    return data_all, px, py