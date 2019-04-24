#!codeing:utf-8

from chembl_webresource_client.new_client import new_client
import pandas as pd
import numpy as np
import argparse

def Dict_to_data(target_dict, activity, tax_id):
	target_df = pd.DataFrame.from_dict(target_dict)
	#Filter tax id is 9606, it's mean that the result is a human
	target_human = target_df[target_df['tax_id']==tax_id]
	
	#From ChEMBL obtain data
	result_df = pd.DataFrame()
	for target_id in target_human['target_chembl_id']:
		ki_dict = activity.filter(target_chembl_id=target_id)
		ki_df = pd.DataFrame.from_dict(ki_dict)
		result_df = result_df.append(ki_df, ignore_index=True)
	return result_df


def ligand_info(input_name, tax_id, search_type):
	"""
	INFOMATION:
	Given a gene name as function input
	Download ligand infomation
	
	PARAMETERS:
	input_name: input argument name;you can input gene name, uniport id
				default is uniport id
	"""
	target = new_client.target
	activity = new_client.activity

	assert search_type in ["GENE_NAME", "UNIPROT_ID"], "Input Error!"
	if search_type == "UNIPROT_ID":
		uniprot_id = input_name
		print(uniprot_id)
		#From uniport id map to target ChEMBL ID
		target_dict = target.filter(target_components__accession=uniprot_id)
		print(len(target_dict))
		try:
			assert len(target_dict)!=0
			result_df = Dict_to_data(target_dict, activity, tax_id)
			assert len(result_df) != 0
		except AssertionError:
			print("Exception")
			return None
	else: # Input is GENE_NAME
		gene_name = input_name
		print(gene_name)
		#From gene name map to target ChEMBL ID
		target_dict = target.filter(target_synonym__icontains=gene_name)
		print(len(target_dict))
		try:
			assert len(target_dict)!=0
			result_df = Dict_to_data(target_dict, activity, tax_id)
			assert len(result_df) != 0
		except AssertionError:
			return None

	#Filter out key records
	pKi = result_df[result_df['type']=='pKi']
	Ki = result_df[result_df['type']=='Ki']
	pEC50 = result_df[result_df['type']=='pEC50']
	EC50 = result_df[result_df['type']=='EC50']
	
	#Append data of the same type
	Ki_data = pKi.append(Ki)
	EC50_data = pEC50.append(EC50)
	#Merge data as "target_chemal_id" and "molecule_chembl_id"
	info_data = Ki_data.merge(EC50_data, left_on=["target_chembl_id", 
				"molecule_chembl_id"], right_on=["target_chembl_id", 
				"molecule_chembl_id"], suffixes=("_Ki", "_EC50"))
	#Filter out key fields
	info_data = info_data[['target_chembl_id', 'molecule_chembl_id', 
						'standard_value_Ki', 'standard_units_Ki',  
						'standard_value_EC50', 'standard_units_EC50', 
						'canonical_smiles_Ki']]
	#Filter None record
	info_data = info_data.dropna()
	#Transfor data type
	info_data = info_data.astype({'standard_value_Ki':float, 'standard_value_EC50':float})
	#Groupby data
	info_data = info_data[['standard_value_Ki', 'standard_units_Ki', 
						  'standard_value_EC50', 'standard_units_EC50', 
						  'canonical_smiles_Ki']].groupby((info_data['target_chembl_id'], 
						  info_data['molecule_chembl_id'])).min()
	#Colculate pKi and pEC50, add as columns
	try:
		info_data['pKi'] = 9-np.log10(info_data['standard_value_Ki'])
		info_data['pEC50'] = 9-np.log10(info_data['standard_value_EC50'])
	except KeyError as e:
		print("Key Error")
		return None

	return info_data
	#result_df.to_excel("ADOARA2A.xlsx", sheet_name="ADOARA2A")


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


def Comendline():
	parser = argparse.ArgumentParser(description="Parser comend line")
	parser.add_argument("-f", "--filename", help="input file name that save input name list, line by line")
	parser.add_argument("-t", "--tax_id", help="a number, tax id. default=9606(human)", default=9606)
	parser.add_argument("-s", "--search_type", default="UNIPROT_ID")
	parser.add_argument("-o", "--output", help="outfile name, excel file", default="ChEMBLdata.xlsx")
	args = parser.parse_args()
	return args

def main():
	#gene_name_list = ["P29274"]
	args = Comendline()
	FILENAME = args.filename
	TAX_ID = args.tax_id
	SEARCH_TYPE = args.search_type
	OUTFILE = args.output
	COUNT = 0	

	input_name_list = Get_uniprot(FILENAME)
	LENGTH = len(input_name_list) - 1
	with pd.ExcelWriter(OUTFILE) as writer:
		for names in input_name_list[1:]:
			input_name = names[0]
			sheet_name = names[1]
			data = ligand_info(input_name, TAX_ID, SEARCH_TYPE)
			if data is not None:
				data.to_excel(writer, sheet_name=sheet_name)
			COUNT += 1
			print(sheet_name + " is OVER! done %d/%d" % (COUNT, LENGTH))

if __name__ == "__main__":
	main()
