#!codeing:utf-8

"""
使用环境:python3
使用方式：python mutation.py 1.csv
"""

from sys import argv
import pandas as pd
from collections import defaultdict

#filename为standard genetic code表的文件名，该文件是一个CSV文件，第一列为密码子，第二列为该密码子编译的氨基酸
filename = argv[1]
#pandas中read_csv函数读取CSV文件。data为一个二维表,第一列为密码子，第二列为该密码子编译的氨基酸
data = pd.read_csv(filename, header=None)

#字典解析式将二维表转换为字典，密码子为key, 氨基酸名为value
dicts = {row[1][0]: row[1][1].upper() for row in data.iterrows()}
#将字典转换为元组，并排序。目的是防止字典的无序性而造成的潜在威胁
tuples = sorted(dicts.items(), key=lambda x:x[0])
#创建一个字典，储存结果；该字典的特点是当无key值时会创建新的key
result = defaultdict(list)

def Hamming(str1, str2):
	"""
	该函数接收两个密码子，计算hamming距离
	返回hamming距离，和差异字符，例如("C", "T"),其含义为C突变为T
	"""
	d, diff = 0, []
	for char1, char2 in zip(str1, str2):
		#对应位置字符相等则，跳过本次循环进行
		if char1 == char2: continue
		d += 1
		diff.append((char1, char2))
	return d, diff

#两层循环，遍历所有可能
#tuples的结构为元组，每个元素为一个两个值的元组，第一个值为密码子， 第二个值为氨基酸
for i in range(len(tuples)):
	for j in range(len(tuples)):
		#氨基酸名相等，代表没有发生氨基酸突变
		if tuples[i][1] == tuples[j][1]: continue
		d, diff = Hamming(tuples[i][0], tuples[j][0])
		#过滤掉hamming不是1的情况；拓展题里这个值需要设置为2
		if d != 1: continue
		#构造一个key，目的是储存结果
		key = diff[0][0] + diff[0][1]
		result[key].append((tuples[i][1], tuples[j][1]))
#打印出需要的结果
print("CT", len(result["CT"]))
print("CG", len(result["CG"]))
print("CA", len(result["CA"]))
print("AG", len(result["AG"]))
print("AC", len(result["AC"]))
print("AT", len(result["AT"]))

