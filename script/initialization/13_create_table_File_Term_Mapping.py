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
  Column.define("File_RID", typ.text), 
  Column.define("Metadata_RID", typ.text), 
]
key_defs = [
  Key.define(
    ["File_RID","Metadata_RID"], # this is a list to allow for compound keys
    constraint_names=[ [schema_name, "File_Metadata_RID_key"] ],
    comment="file&term must be distinct.",
    annotations={},
  )
  
]

fkey_defs = [
  ForeignKey.define(
    ["File_RID"], # this is a list to allow for compound foreign keys
    "Core",
    "File",
    ["RID"], # this is a list to allow for compound keys
    on_update='CASCADE',
    on_delete='SET NULL',
    constraint_names=[ [schema_name, "File_Metadata_Mapping_File_fkey"] ],
    comment="",
    acls={},
    acl_bindings={},
    annotations={},
  )
  ,ForeignKey.define(
    ["Metadata_RID"], # this is a list to allow for compound foreign keys
    "Vocab",
    "Metadata",
    ["id"], # this is a list to allow for compound keys
    on_update='CASCADE',
    on_delete='SET NULL',
    constraint_names=[ [schema_name, "File_Metadata_Mapping_Term_fkey"] ],
    comment="",
    acls={},
    acl_bindings={},
    annotations={},
  )
]

table_def = Table.define(
  "File_Metadata",
  column_defs,
  key_defs=key_defs,
  fkey_defs=fkey_defs,
  comment="input file information.",
  acls={},
  acl_bindings={},
  annotations={},
  provide_system=True,
)

new_table = schema.create_table(catalog, table_def)