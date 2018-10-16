from deriva.core import DerivaServer, get_credential
from deriva.core.ermrest_model import Table, Column, Key, builtin_types,ForeignKey,builtin_types as typ
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('hostname')
parser.add_argument('catalog_number')
args = parser.parse_args()

hostname = args.hostname
catalog = args.catalog_number


credential = get_credential(hostname)
server = DerivaServer('https', hostname, credential)
catalog = server.connect_ermrest(catalog)
model = catalog.getCatalogModel()

path = '/entity/Domain'
data = [{"id":"CORE:{RID}","uri":"/id/{RID}","name":"Electricity Supply","description":"Electricity Supply"}]
resp = catalog.post(path, json=data)

path = '/entity/Step_Type'
data = [{"id":"CORE:{RID}","uri":"/id/{RID}","name":"SL","description":"Statistical Learning"}
,{"id":"CORE:{RID}","uri":"/id/{RID}","name":"SP","description":"stochastic programming"}
,{"id":"CORE:{RID}","uri":"/id/{RID}","name":"Validation","description":"Validation on result"}]
resp = catalog.post(path, json=data)

path = '/entity/File_Category'
data = [{"id":"CORE:{RID}","uri":"/id/{RID}","name":"Raw File","description":"Original dataset"},{"id":"CORE:{RID}","uri":"/id/{RID}","name":"Input/Output File","description":"Input file or output file"}]
resp = catalog.post(path, json=data)