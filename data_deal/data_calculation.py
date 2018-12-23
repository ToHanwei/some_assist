#!coding:utf-8

from numpy import array
from pandas import DataFrame
from pandas import read_excel
from collections import defaultdict

"""
This script is write for shu.
processing experimental data 
The way of this script in "calculation.jpg" file
"""

__author__ = "Wei"
__tate__ = "20181221"
__mail__ = "hanwei@shanghaitech.edu.cn"


def data_conduct(input_file, outfile, inter):
	#determine the file name
	if not outfile.endswith(".xlsx"):
		outfile = outfile.split(".")[0] + ".xlsx"
	data = read_excel(input_file, header=0, dtypes="float64")
	group = set(list(data["Sample Name"]))
	diff_dict = defaultdict(array)
	#group the data
	for key in group:
		target_bool = (data["Target Name"] == inter)
		sample_bool = (data["Sample Name"] == key)
		value_bool = (target_bool & sample_bool)
		value = array(data.loc[sample_bool, "CT"]) - array(data.loc[value_bool, "CT"])
		diff_dict[key] = value
	#calculate the experimental data
	out_dict = defaultdict(array)
	for key in list(group):
		contrast = array(diff_dict["nc"], dtype="float64")
		gene = array(diff_dict[key], dtype="float64")
		out_dict[key] = pow(2, contrast - gene)
	#output the data
	data_out, res, j = [], "", 0
	for key in data["Sample Name"]:
		i = 0
		if key == res: continue
		data_out.extend(list(out_dict[key]))
		res = key
	data_out = DataFrame(array(data_out), columns=["RQ"])
	data = data.join(data_out)
	data.to_excel(outfile, index=False)
	
	
if __name__ == "__main__":
	#some test file
	inter = "hprt"
	input_file = "test.xlsx"
	outfile = "test_deal.xlsx"
	#call the function
	data_conduct(input_file, outfile, inter)