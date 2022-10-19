
# coding=UTF-8

import arcpy
import os
import sys

arcpy.env.workspace = "D:/Workspace"
# Clip_management (in_raster, rectangle, out_raster, {in_template_dataset}, {nodata_value}, {clipping_geometry}, {maintain_clipping_extent})
path = sys.path[0]  # 获取当前代码路径
path = "D:\\Users\\kang_\\Desktop\\CNN_Traff\\data_all\\jibuti"
path1 = "D:\\Users\\kang_\\Desktop\\CNN_Traff\\data_all\\second1"
in_template_dataset = "D:\\Users\\kang_\\Desktop\\CNN_Traff\\data_all\\jibuti\\second.shp"


tif_list = [x for x in os.listdir(path) if x.endswith(".tif")]
for num, i in enumerate(tif_list):
    arcpy.Clip_management(path + '\\' + i, "#", path1 + '\\' + i, in_template_dataset, "-999", "#", "MAINTAIN_EXTENT")


