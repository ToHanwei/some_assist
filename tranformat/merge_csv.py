#!coding:utf-8

import os
import pandas as pd


def transformat(input_dir, outfile):
	if "." not in outfile:
		outfile = outfile + ".xlsx"
	data_out = pd.DataFrame()
	names = []
	files_list = os.listdir(input_dir)
	files_list.sort()
	for one_file in files_list:
		name = one_file.split(".")[0]
		names.append(name)
		one_file = input_dir+"/"+one_file
		data = pd.read_table(one_file, encoding="utf-16-le", header=None)
		data_out = data_out.append(data[1])
	data_out.index = names
	data_out = data_out.T	
	data_out.to_excel(outfile)
