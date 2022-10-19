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

def load_tif(tif_file):
	dataset = gdal.Open(tif_file)
	if dataset is None:
		print(tif_file + '文件无法打开')
		return
	# 栅格矩阵的列数
	im_width = dataset.RasterXSize
	# 栅格矩阵的行数
	im_height = dataset.RasterYSize
	# 获取数据，以()为读取图像的范围
	traff_data = dataset.ReadAsArray(0, 0, im_width, im_height).astype(float)
	#计算图像左上点坐标
	adfGeoTransform = dataset.GetGeoTransform()
	#x表示行，y表示列
	py = [adfGeoTransform[0] + i * adfGeoTransform[1] for i in range(im_width)]
	px = [adfGeoTransform[3] + i * adfGeoTransform[5] for i in range(im_height)]
	return traff_data, px, py