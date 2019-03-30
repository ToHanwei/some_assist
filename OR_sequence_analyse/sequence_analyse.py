#coding:utf-8

"""
这个脚本用来分析OR的序列
导入的是所有人源OR
以OR5AN1为标准删除Gap
计算个位点保守程度
"""

import pandas as pd
import numpy as np
from sys import argv
from collections import defaultdict


def count(col):
	aa_list = list("ACDEFGHIKLMNPQRSTVWY")
	aa_dict = {a:0 for a in aa_list}
	for aa in col:
		if aa == "-": continue
		aa_dict[aa] = aa_dict[aa] + 1
	return aa_dict

ORfile = argv[1]
seq_dict = defaultdict(list)

with open(ORfile, mode='r') as seqfile:
	for line in seqfile:
		lines = line.split()
		if len(lines) != 2: continue
		key = lines[0].split("|")[1]
		seq = list(lines[1])
		if (key not in seq_dict):
			seq_dict[key] = seq
		else:
			seq_dict[key].extend(seq)
		
seq_df = pd.DataFrame.from_dict(data=seq_dict, orient='columns')
b = seq_df['O5AN1']!='-'
seq_filter = seq_df[b]
seq_filter.index = range(1, len(seq_filter)+1)
a = seq_filter.apply(count, axis=1)
print(pd.DataFrame.from_dict((dict(a))))
