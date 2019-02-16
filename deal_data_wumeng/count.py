#!codeing:utf-8

from sys import argv
import numpy as np

infile = argv[1]

rang = range(-20, 22, 2)
rang = zip(rang[:-1], rang[1:])

with open(infile, mode='r') as open_data:
	data = [line.split(',') for line in open_data]

data_dict = {key:[] for key in range(len(data))}

for i in range(len(data)):
	line = data[i]
	line_dict = {key:0 for key in rang}
	for str_num in line[:-1]:
		num = float(str_num)
		for ran in rang:
			if ran[0] <= num < ran[1]:
				line_dict[ran] = line_dict[ran] + 1
	data_dict[i] = line_dict

res_dict = {key:[] for key in rang}
for ran in rang:
	res_list = []
	for key in data_dict.keys():
		dic = data_dict[key]
		res_list.append(dic[ran])
	res_dict[ran] = res_list

print("ran",",","mean",",","std",",","var")
for ran in rang:
	arry = np.array(res_dict[ran])
	mean = np.mean(arry)
	std = np.std(arry)
	var = np.var(arry)
	print(ran,',',mean,',',std,',',var)
