from requests import HTTPError
from deriva.core import DerivaServer, ErmrestCatalog, get_credential
from deriva.core.ermrest_model import Table, Column, Key, builtin_types
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('hostname')
parser.add_argument('catalog_number')
args = parser.parse_args()


hostname = args.hostname
catalog_number = args.catalog_number

credential = get_credential(hostname)
server = DerivaServer('https', hostname, credential)
catalog = ErmrestCatalog('https', hostname, catalog_number, credential)

model_root = catalog.getCatalogModel()

schema = 'public'
schema = model_root.schemas[schema]

table_list = ['Step_Input_File'
              ,'Step_Output_File'
              ,'Step_Program'
              ,'Step'
              ,'Instance_Keywords'
              ,'Instance'
              ,'File_Metadata'
              ,'File'
              ]

for i in range(len(table_list)):
    if table_list[i] in schema.tables.keys():
        tab = schema.tables[table_list[i]]
        tab.delete(catalog)
        print('table deleted: %s',table_list[i])
    else:
        print('table not exist: %s',table_list[i])

catalog = ErmrestCatalog('https', hostname, catalog_number, credential)
model_root = catalog.getCatalogModel()
schema = 'public'
schema = model_root.schemas[schema]
for t in schema.tables:
    if t<>'ermrest_client':
        print('other table to deleted: %s',t)
        tab = schema.tables[t]
        tab.delete(catalog)
    else:
        continue


table_list = [
              'Domain',
              'Step_Type',
              'Keywords',
              'Metadata',
              'File_Category',
              'Instance_Level'
              ]
schema = 'Vocab'
schema = model_root.schemas[schema]
for i in range(len(table_list)):
    if table_list[i] in schema.tables.keys():
        tab = schema.tables[table_list[i]]
        tab.delete(catalog)
        print('table deleted: %s',table_list[i])
