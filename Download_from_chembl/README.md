# 从ChEMBL下载数据

## TIME：20190423
## Auther: ToHanwei
## Mail: hanwei@shangahitech.edu.cn


脚本中提供和两中输入数据，分别是genename和uniprot id</br>
---------------------------------------------------------
## 脚本框架
1. 从输入uniprot id（genenane)获取targe chembl id
2. 由target chembl id 获取数据，这里的数据是ChEMBL数据图提供的所有数据
3. 从获得的全部信息过滤出需要的信息:target chembl id, molecule chembl id, Ki/pKi, EC50/pEC50, units
4. 以target chembl id, molecule chembl id为条件merge数据（只获取同时具有Ki/pKi, EC50/pEC50的记录
5. 通过计算，添加pKi, pEC50列
6. 保存数据；所有数据保存在一个Excel文件中，每个target信息保存为一个sheet

## 输入文件
* 期待的输入文件有两列， 第一列为uniprot id(genename), 第二列为保存Excel文件的sheet name
* 每一列需要一个header, 列分隔符为空格
* 第一列的数据需要是合法的uniprot id 或者 genename, 第二列任意

## 使用举例
获取帮助信息</br>
`python download_ligand_info.py --help`

使用uniport id下载数据</br>
`python download_ligand_info.py -f uniprot_id.txt -s UNIPROT_ID -t 9606 -o ChEMBLdata.xlsx`

使用genename下载数据</br>
`python download_ligand_info.py -f genename.txt -s GENE_NAME -t 9606 -o ChEMBLdata.xlsx`


