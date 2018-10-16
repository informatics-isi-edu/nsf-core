from requests import HTTPError
from deriva.core import DerivaServer, ErmrestCatalog, get_credential
from deriva.core.ermrest_model import Table, Column, Key, builtin_types
import deriva.core.ermrest_model as em
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

schema = 'Core'
schema = model_root.schemas[schema]

model = catalog.getCatalogModel()

column_def = em.Column.define(
  "Sequence",
  builtin_types.text,
  nullok=True,
  comment=""
)
table = model_root.table('Core', 'Step')
new_column = table.create_column(catalog, column_def)
