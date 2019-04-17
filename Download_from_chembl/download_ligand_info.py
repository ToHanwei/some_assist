#!codeing:utf-8

from chembl_webresource_client.new_client import new_client
import pandas as pd
import numpy as np


def ligand_info(gene_name):
	"""
	INFOMATION:
	Given a gene name as function input
	Download ligand infomation
	
	PARAMETERS:
	gene_name: input argument gene name
	"""
	target = new_client.target
	activity = new_client.activity

	#From gene name map to target ChEMBL ID
	target_dict = target.filter(target_synonym__icontains=gene_name)
	target_df = pd.DataFrame.from_dict(target_dict)
	#Filter tax id is 9606, it's mean that the result is a human
	target_human = target_df[target_df['tax_id']==9606]
	
	#From ChEMBL obtain data
	result_df = pd.DataFrame()
	for target_id in target_human['target_chembl_id']:
		ki_dict = activity.filter(target_chembl_id=target_id)
		ki_df = pd.DataFrame.from_dict(ki_dict)
		result_df = result_df.append(ki_df, ignore_index=True)
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
						'standard_value_EC50', 'standard_units_EC50']]
	#Filter None record
	info_data = info_data.dropna()
	#Transfor data type
	info_data = info_data.astype({'standard_value_Ki':float, 'standard_value_EC50':float})
	#Groupby data
	info_data = info_data[['standard_value_Ki', 'standard_units_Ki', 
						  'standard_value_EC50', 'standard_units_EC50'
						  ]].groupby((info_data['target_chembl_id'], 
						  info_data['molecule_chembl_id'])).min()
	#Colculate pKi and pEC50, add as columns
	info_data['pKi'] = 9-np.log10(info_data['standard_value_Ki'])
	info_data['pEC50'] = 9-np.log10(info_data['standard_value_EC50'])

	return info_data
	#result_df.to_excel("ADOARA2A.xlsx", sheet_name="ADOARA2A")


def main():
	gene_name_list = ["ADORA2A"]
	writer = pd.ExcelWriter("ChEMBLdata.xlsx")
	for gene_name in gene_name_list:
		data = ligand_info(gene_name)
		data.to_excel(writer, sheet_name=gene_name)
	writer.close()

if __name__ == "__main__":
	main()
