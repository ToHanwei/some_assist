import sys
import pandas as pd

def Get_uniprot(filename):
	"""
	INFORMATION:
	From file obtain imput names
	input names must be first column
	
	PARAMETERS:
	file_name: input filename
	"""
	with open(filename, mode='r') as files:
		input_name_list = [(line.split()[0], line.split()[1]) for line in files]
	return input_name_list


filename = sys.argv[1]
names = Get_uniprot(filename)
key = names[0]
value = names[1:]
data = dict(value)

data = pd.DataFrame.from_dict(data, orient="index")
data.to_csv("uniport_names.txt", sep='\t', index=True, header=False)


uniport = [line[0]+"\n" for line in value]
with open("uniprot_only.txt", mode="w") as filew:
	filew.writelines(uniport)

