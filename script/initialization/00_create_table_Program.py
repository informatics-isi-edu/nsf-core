from deriva.core import DerivaServer, get_credential
from deriva.core.ermrest_model import Table, Column, Key,ForeignKey,builtin_types as typ
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('hostname')
parser.add_argument('catalog_number')
parser.add_argument('schema_name')
args = parser.parse_args()


hostname = args.hostname
schema_name = args.schema_name
catalog = args.catalog_number

credential = get_credential(hostname)
server = DerivaServer('https', hostname, credential)
catalog = server.connect_ermrest(catalog)
model = catalog.getCatalogModel()
schema = model.schemas[schema_name]
config = catalog.getCatalogConfig()


column_defs = [ 
  Column.define("Name", typ.text), 
  Column.define("Algorithm", typ.text), 
  Column.define("Description", typ.text), 
  Column.define("Code_Reference", typ.text), 
  Column.define("Version", typ.text), 
  Column.define("Environment", typ.text), 
]
key_defs = [
  Key.define(
    ["Name"], # this is a list to allow for compound keys
    constraint_names=[ [schema_name, "Program_RID_Name_key"] ],
    comment="program name must be distinct.",
    annotations={},
  )  
]

fkey_defs = [
]


table_def = Table.define(
  "Program",
  column_defs,
  key_defs=key_defs,
  fkey_defs=fkey_defs,
  comment="program information",
  acls={},
  acl_bindings={},
  annotations={},
  provide_system=True,
)

new_table = schema.create_table(catalog, table_def)