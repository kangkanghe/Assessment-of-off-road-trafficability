import numpy as np


def factor_num(data_all):
    # 初始化因子编号
    hazard_label = {'类别': 2, 'value': [0, 1], 'label': [1, 2], 'IC': [9, 1], 'weight': [0.2807]}

    slope_label = {'类别': 6, 'value': [[0, 7], [7, 14], [14, 21], [21, 28], [28, 35], [35, 90]], 'label': [1, 2, 3, 4, 5, 6], 'IC': [9, 8, 6, 5, 3, 1], 'weight': [0.1401]}

    land_label = {'类别': 11, 'value': [10, 9, 80, 79, 50, 49, 90, 89, 40, 30, 60], 'label': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], 'IC': [2, 5, 2, 5, 1, 5, 3, 6, 8, 6, 8], 'weight': [0.1273]}

    twi_label = {'类别': 3, 'value': [[-998, -9.646480643], [-9.646480643, -1.20733932], [-1.20733932, 100]], 'label': [1, 2, 3], 'IC': [9, 6, 2], 'weight': [0.1043]}

    RCI_label = {'类别': 9, 'value': [126, 86, 46, 145, 109, 73, 111, 57, 3], 'label': [1, 2, 3, 4, 5, 6, 7, 8, 9], 'IC': [9, 9, 2, 9, 9, 9, 9, 6, 1], 'weight': [0.0835]}

    rocksoil_label = {'类别': 4, 'value': [1, 2, 3, 4], 'label': [1, 2, 3, 4], 'IC': [8, 4, 5, 7], 'weight': [0.0808, 0.0203]}

    tpi_label = {'类别': 4, 'value': [[-998, -24.23928462], [-24.23928462, 13.59426437], [13.59426437, 60.32982489], [60.32982489, 360]], 'label': [1, 2, 3, 4], 'IC': [7, 2, 9, 2], 'weight': [0.0672]}

    struct_label = {'类别': 3, 'value': [1, 2, 3], 'label': [1, 2, 3], 'IC': [8, 6, 3], 'weight': [0.0360]}

    spi_label = {'类别': 2, 'value': [[-998, -13.35234833], [-13.35234833, 100]], 'label': [1, 2], 'IC': [8, 4], 'weight': [0.0303]}

    DEM_label = {'类别': 2, 'value': [[-998, 2000], [2000, 10000]], 'label': [1, 2], 'IC': [8, 5], 'weight': [0.0295]}

    data_label = {'hazard_label':hazard_label, 'slope_label': slope_label, 'land_label': land_label, 'twi_label': twi_label, 'RCI_label': RCI_label, 'rocksoil_label': rocksoil_label, 'tpi_label': tpi_label, 'struct_label': struct_label, 'spi_label': spi_label, 'DEM_label': DEM_label}
    hazard_IC = np.zeros(np.shape(data_all['hazard_data']))
    slope_IC = np.zeros(np.shape(data_all['slope_data']))
    land_IC = np.zeros(np.shape(data_all['slope_data']))
    twi_IC = np.zeros(np.shape(data_all['slope_data']))
    RCI_IC = np.zeros(np.shape(data_all['slope_data']))
    rocksoil_IC = np.zeros(np.shape(data_all['slope_data']))
    tpi_IC = np.zeros(np.shape(data_all['slope_data']))
    struct_IC = np.zeros(np.shape(data_all['slope_data']))
    spi_IC = np.zeros(np.shape(data_all['slope_data']))
    DEM_IC = np.zeros(np.shape(data_all['slope_data']))

    data_IC = {'hazard_IC': hazard_IC,'slope_IC': slope_IC, 'land_IC': land_IC, 'twi_IC': twi_IC, 'RCI_IC': RCI_IC, 'rocksoil_IC': rocksoil_IC, 'tpi_IC': tpi_IC, 'struct_IC': struct_IC, 'spi_IC': spi_IC, 'DEM_IC': DEM_IC}
    data_label1 = {'hazard_IC': hazard_IC,'slope_IC': slope_IC, 'land_IC': land_IC, 'twi_IC': twi_IC, 'RCI_IC': RCI_IC, 'rocksoil_IC': rocksoil_IC, 'tpi_IC': tpi_IC, 'struct_IC': struct_IC, 'spi_IC': spi_IC, 'DEM_IC': DEM_IC}

    for i in zip (data_all, data_label, data_IC, data_label1):
        value = data_label[i[1]]['value']
        label = data_label[i[1]]['label']
        IC = data_label[i[1]]['IC']
        number = np.zeros(np.shape(data_all[i[0]]))
        for j in range(len(value)):
            if np.size(value[j]) == 1:
                number[np.where(data_all[i[0]] == value[j])] = label[j]
                data_IC[i[2]][np.where(data_all[i[0]] == value[j])] = IC[j]
                data_label1[i[3]][np.where(data_all[i[0]] == value[j])] = label[j]
            elif np.size(value[j]) == 2:
                number[np.where((data_all[i[0]] >= value[j][0]) & (data_all[i[0]] < value[j][1]))] = label[j]
                data_IC[i[2]][np.where((data_all[i[0]] >= value[j][0]) & (data_all[i[0]] < value[j][1]))] = IC[j]
                data_label1[i[3]][np.where((data_all[i[0]] >= value[j][0]) & (data_all[i[0]] < value[j][1]))] = label[j]
        # data_all[i[0]] = number

    return data_all, data_IC, data_label, data_label1