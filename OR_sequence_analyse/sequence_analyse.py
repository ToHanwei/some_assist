#coding:utf-8

"""
这个脚本用来分析OR的序列
导入的是所有人源OR
以OR5AN1为标准删除Gap
计算个位点保守程度
"""

import pymysql
import pandas as pd
import numpy as np
from sys import argv
from collections import defaultdict
from sqlalchemy import create_engine


def count(col):
	"""统计序列"""
	aa_list = list("ACDEFGHIKLMNPQRSTVWY")
	aa_dict = {a:0 for a in aa_list}
	for aa in col:
		if aa == "-": continue
		aa_dict[aa] = aa_dict[aa] + 1
	return aa_dict

def connect_db(df):
	"""将Count的数据储存到mysql数据库"""
	df = df.T
	connect_info = "mysql+pymysql://root:hanwei1@localhost:3306/Human_OR_seq"
	engine = create_engine(connect_info)
	df.to_sql(name="Q8NGI8", con=engine, if_exists='replace', index=False)


def dofile():
	ORfile = argv[1]
	seq_dict = defaultdict(list)
	with open(ORfile, mode='r') as seqfile:
		for line in seqfile:
			lines = line.split()
			if len(lines) != 2: continue
			key = lines[0].split("|")[0]
			seq = list(lines[1])
			if (key not in seq_dict):
				seq_dict[key] = seq
			else:
				seq_dict[key].extend(seq)
	seq_df = pd.DataFrame.from_dict(data=seq_dict, orient='columns')
	seq_filter = seq_df[seq_df['Q8NGI8']!='-']
	seq_filter.index = range(1, len(seq_filter)+1)
	COUNT = len(seq_filter.columns)
	NUM = len(seq_filter.T)
	acount = seq_filter.apply(count, axis=1)
	seq_data = pd.DataFrame.from_dict((dict(acount)))*100/NUM
	return seq_data, acount, seq_filter['Q8NGI8'], COUNT


def main(isave=False):
	seq_data, acount, o5an1, COUNT = dofile()
	if isave: connect_db(seq_data)
	for i in acount.index:
		seq = sorted(acount[i].items(), key=lambda x:x[1], reverse=True)
		if seq[0][1]*100/COUNT >= 0:
			print(i, o5an1[i], seq[0][0], seq[0][1]*100/COUNT)

	
if __name__ == "__main__":
	main()

