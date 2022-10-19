"""
Created on Thu Oct 28 21:34:41 2021
@author: He Kang
############################多属性叠加###################################
"""
import os
import pandas as pd
import numpy as np
from osgeo import gdal,osr
import argparse
from IC_rules import IC_rules
import os
from filter import filter
from AHP_weight import AHP_weight
from record_tif import record_tif
from density import density
from load_tif import load_tif
from dataset_clip import dataset_clip
from factor_num import factor_num
from IC_data import IC_data
from traff_relus import traff_relus
import jenkspy
import scipy.io as sio
import h5py

def Traff_SUM(args):
	#-999用来替换无效栅格
	# 把所有数据保存在元组，共9类，缺少地质灾害
	data_all, px, py = dataset_clip(args, 'first_RCI_data1.npy')

	# record_tif(data_all['land_data'], px, py, args.output_land_map)
	# record_tif(data_all['rocksoil_data'], px, py, args.output_rocksoil_map)
	# record_tif(data_all['RCI_data'], px, py, args.output_RCI_map)
	# struct_data1 = np.zeros(np.shape(data_all['struct_data']))
	# struct_data1[np.where(data_all['struct_data'] < np.max(data_all['struct_data']))] = 1
	# record_tif(struct_data1, px, py, args.output_struct_map)

	################################通行准则################################
	# 1.计算植被、水体、建筑、湿地的密集性；植被(9,10)、水体(79,80)、建筑物（49,50）、湿地（89,90），低值表示稀疏、高值表示密集;
	var_data = {'density_tree':np.where(data_all['land_data'] == 10), 'density_built':np.where(data_all['land_data'] == 50), 'density_water':np.where(data_all['land_data'] == 80), 'wetland':np.where(data_all['land_data'] == 90)}   #保存索引
	var_num = {'density_tree': 10, 'density_built': 50, 'density_water': 80, 'wetland':90}
	data_all['land_data'] = density(data_all['land_data'], var_data, var_num, "first_land_data1.npy")

	# 2.计算节理密集度
	data_all['struct_data'][np.where((data_all['struct_data'] >= 1) & (data_all['struct_data'] < np.max(data_all['struct_data'])))] = 3
	data_all['struct_data'][np.where(data_all['struct_data'] == np.max(data_all['struct_data']))] = 1
	var_data = {'density_struct':np.where(data_all['struct_data'] == 3)}   #保存索引
	var_num = {'density_struct': 3}
	data_all['struct_data'] = density(data_all['struct_data'], var_data, var_num, "first_struct_data1.npy")

	# 2.制定履带车辆越野通行准则，根据因素表执行,通行能力Ⅰ，Ⅱ，Ⅲ，Ⅳ，依次变弱
	#,2.1 AHP Weight计算权重
	weight = AHP_weight(args.input_AHP_JM)
	# 2.2 各因子分配编号
	data_all, data_IC, data_label, data_label1 = factor_num(data_all)

	# 2.3 计算通行规则
	# rules = traff_relus(data_label1, data_label, 'first1.npy')
	rules = traff_relus(data_IC, data_label, 'first1.npy')
	rules_IC = IC_rules(rules, data_label)
	Traffic_levels = jenkspy.jenks_breaks(rules_IC, nb_class = 4)   #分类阈值

	# 2.4计算各栅格综合量化信息
	IC, Capacity_map, proportion = IC_data(data_all, data_IC, data_label, Traffic_levels)

	# 2.5输出为tif文件
	record_tif(IC, px, py, args.output_IC)
	record_tif(Capacity_map, px, py, args.output_Capacity_map)
	# 2.6滤波
	Capacity_data = np.loadtxt(r"D:\MATLAB代码\first.txt")
	DEM_data, px_rocksoil, py_rocksoil = load_tif(args.input_DEM)
	px, py = np.meshgrid(px_rocksoil, py_rocksoil)
	record_tif(Capacity_data, px, py, args.output_Capacity_filter)

	# hazard_data = np.loadtxt(r"D:\Users\kang_\Desktop\CNN_Traff\CNN_Traff\hazard_first.txt", dtype=np.float32)
	# hazard_data = hazard_data.reshape(np.shape(data_all['land_data']))
	# record_tif(hazard_data, px, py, args.output_hazard_map)
	# 3.制定轮式车辆越野通行准则，根据因素表执行


if __name__ == '__main__':
	#通行能力图
	parser = argparse.ArgumentParser(description='通行能力图')
	# 单独土地利用
	parser.add_argument('--input_土地利用', type=str, default=r'D:\Users\kang_\Desktop\CNN_Traff\data_all\first\土地利用.tif', help='输入地貌')
	# 土体、水分、坡度+DEM综合
	parser.add_argument('--input_slope', type=str, default=r'D:\Users\kang_\Desktop\CNN_Traff\data_all\first\坡度.tif', help='输入坡度')
	parser.add_argument('--input_DEM', type=str, default=r'D:\Users\kang_\Desktop\CNN_Traff\data_all\first\DEM.tif', help='输入DEM')
	parser.add_argument('--input_rocksoil', type=str, default=r'D:\Users\kang_\Desktop\CNN_Traff\data_all\first\岩土体10万.tif', help='输入土体')
	parser.add_argument('--input_湿度', type=str, default=r'D:\Users\kang_\Desktop\CNN_Traff\data_all\first\地形湿度指数.tif', help='输入湿度')
	# 额外附加几种，坡位指数、水流力指数、地质灾害、
	parser.add_argument('--input_地质灾害', type=str, default=r'D:\Users\kang_\Desktop\CNN_Traff\data_all\first\hazard_map1.tif', help='输入地质灾害')
	parser.add_argument('--input_坡位指数', type=str, default=r'D:\Users\kang_\Desktop\CNN_Traff\data_all\first\坡位指数.tif', help='输入坡位指数')
	parser.add_argument('--input_水流力指数', type=str, default=r'D:\Users\kang_\Desktop\CNN_Traff\data_all\first\水流力指数.tif', help='输入水流力指数')
	# parser.add_argument('--input_地质灾害', type=str, default=r'D:\Users\kang_\Desktop\卷积神经网络越野通行能力评价\数据\吉布提\地质灾害.tif', help='输入地质灾害')
	parser.add_argument('--input_节理构造', type=str, default=r'D:\Users\kang_\Desktop\CNN_Traff\data_all\first\节理构造.tif', help='输入节理构造')
	parser.add_argument('--input_AHP_JM', type=str, default=r'D:\Users\kang_\Desktop\CNN_Traff\CNN_Traff\AHPcode\AHP判断矩阵.xlsx', help='层次分析法权重矩阵')
	parser.add_argument('--output_IC', type=str, default=r'D:\Users\kang_\Desktop\CNN_Traff\data_all\first\first_IC1.tif', help='IC数据文件保存路径')
	parser.add_argument('--output_Capacity_map', type=str, default=r'D:\Users\kang_\Desktop\CNN_Traff\data_all\first\Capacity_map11.tif', help='Capacity_map数据文件保存路径')
	parser.add_argument('--output_land_map', type=str, default=r'D:\Users\kang_\Desktop\CNN_Traff\data_all\first\land_map1.tif', help='land_map数据文件保存路径')
	parser.add_argument('--output_rocksoil_map', type=str, default=r'D:\Users\kang_\Desktop\CNN_Traff\data_all\first\rocksoil_map1.tif', help='rocksoil_map数据文件保存路径')
	parser.add_argument('--output_RCI_map', type=str, default=r'D:\Users\kang_\Desktop\CNN_Traff\data_all\first\RCI_map1.tif', help='RCI_map数据文件保存路径')
	parser.add_argument('--output_struct_map', type=str, default=r'D:\Users\kang_\Desktop\CNN_Traff\data_all\first\struct_map1.tif', help='struct_map数据文件保存路径')
	parser.add_argument('--output_hazard_map', type=str, default=r'D:\Users\kang_\Desktop\CNN_Traff\data_all\first\hazard_map1.tif', help='struct_map数据文件保存路径')
	parser.add_argument('--output_Capacity_filter', type=str, default=r'D:\Users\kang_\Desktop\CNN_Traff\data_all\first\Capacity_filter.tif', help='struct_map数据文件保存路径')

	args = parser.parse_args()
	Traff_SUM(args)