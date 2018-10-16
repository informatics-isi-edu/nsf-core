from requests import HTTPError
from deriva.core import DerivaServer, ErmrestCatalog, get_credential
from deriva.core.ermrest_model import Table, Column, Key, builtin_types
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('hostname')
parser.add_argument('catalog_number')
parser.add_argument('schema_name')
parser.add_argument('table_name')
args = parser.parse_args()


hostname = args.hostname
schema_name = args.schema_name
catalog_number = args.catalog_number
table_name = args.table_name


credential = get_credential(hostname)
server = DerivaServer('https', hostname, credential)
catalog = ErmrestCatalog('https', hostname, catalog_number, credential)

model_root = catalog.getCatalogModel()

schema = model_root.schemas[schema_name]

if table_name in schema.tables.keys():
    tab = schema.tables[table_name]
    tab.delete(catalog)
    print('table deleted: %s',table_name)
else:
    print('table not exist: %s',table_name)

#catalog.delete('/entity/data_commons:cvterm').raise_for_status()