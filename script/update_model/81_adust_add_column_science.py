from requests import HTTPError
from deriva.core import DerivaServer, ErmrestCatalog, get_credential
from deriva.core.ermrest_model import Table, Column, Key, builtin_types, ForeignKey
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
  "Science_ID",
  builtin_types.text,
  nullok=True,
  comment=""
)
table = model_root.table('Core', 'Instance')
# new_column = table.create_column(catalog, column_def)

new_fkey_def = ForeignKey.define(
    ["Science_ID"], # this is a list to allow for compound foreign keys
    "Vocab",
    "Science",
    ["ID"], # this is a list to allow for compound keys
    on_update='CASCADE',
    on_delete='SET NULL',
    constraint_names=[ ['Core', 'Instance_Science_ID_fkey'] ],
    comment="",
    acls={},
    acl_bindings={},
    annotations={},
  )

table.create_fkey(catalog, new_fkey_def)