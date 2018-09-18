# -*- coding: utf-8 -*-
"""
Created on Mon Jul 30 12:30:13 2018

@author: qingj
"""


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
  Column.define("Category_RID", typ.text), 
  Column.define("Name", typ.text), 
  Column.define("Description", typ.text), 
  Column.define("URI", typ.text), 
  Column.define("Size", typ.int4), 
  Column.define("MD5", typ.text), 
]
key_defs = [
  Key.define(
    ["Category_RID","Name"], # this is a list to allow for compound keys
    constraint_names=[ [schema_name, "File_Category_RID_Name_key"] ],
    comment="file category and file name must be distinct.",
    annotations={},
  )  
]

fkey_defs = [
  ForeignKey.define(
    ["Category_RID"], # this is a list to allow for compound foreign keys
    "Vocab",
    "File_Category",
    ["RID"], # this is a list to allow for compound keys
    on_update='CASCADE',
    on_delete='SET NULL',
    constraint_names=[ [schema_name, "File_Category_RID_fkey"] ],
    comment="Category_ID must be a valid reference value from the File_Category table.",
    acls={},
    acl_bindings={},
    annotations={},
  )
]


table_def = Table.define(
  "File",
  column_defs,
  key_defs=key_defs,
  fkey_defs=fkey_defs,
  comment="file information.",
  acls={},
  acl_bindings={},
  annotations={},
  provide_system=True,
)

new_table = schema.create_table(catalog, table_def)