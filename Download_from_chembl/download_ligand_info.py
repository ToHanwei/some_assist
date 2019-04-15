from chembl_webresource_client.new_client import new_client
import pandas as pd
import numpy as np


target = new_client.target
activity = new_client.activity

gene_name = "ADORA2A"
target_dict = target.filter(target_synonym__icontains=gene_name)

target_df = pd.DataFrame.from_dict(target_dict)
target_human = target_df[target_df['tax_id']==9606]

result_df = pd.DataFrame()
for target_id in target_human['target_chembl_id']:
	ki_dict = activity.filter(target_chembl_id=target_id, assay_type='B').filter(standard_type='Ki')
	ki_df = pd.DataFrame.from_dict(ki_dict)
	result_df = result_df.append(ki_df, ignore_index=True)
print(result_df)
result_df.to_excel("ADOARA2A.xlsx", sheet_name="ADOARA2A")

