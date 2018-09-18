# -*- coding: utf-8 -*-
"""
Created on Mon Jul 30 12:30:13 2018

@author: qingj
"""


from deriva.core import DerivaServer, get_credential
from deriva.core.ermrest_model import Table, Column, Key, builtin_types,ForeignKey,builtin_types as typ
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
  Column.define("Sequence", typ.int8),   
  Column.define("Name", typ.text),  
  Column.define("Description", typ.text), 
  Column.define("Instruction", typ.text), 
  Column.define("Step_Type_ID", typ.text),
  Column.define("Program_ID", typ.text),
  Column.define("Instance_RID", typ.text), 
]
key_defs = [
  Key.define(
    ["Instance_RID","Name"], # this is a list to allow for compound keys
    constraint_names=[ [schema_name, "Instance_RID_Step_Name_key"] ],
    comment="Instance plus step name must be distinct.",
    annotations={},
  ),Key.define(
    ["Instance_RID","Sequence"], # this is a list to allow for compound keys
    constraint_names=[ [schema_name, "Instance_RID_Step_Sequence_key"] ],
    comment="Instance plus step sequence must be distinct.",
    annotations={},
    ),
]

fkey_defs = [
  ForeignKey.define(
    ["Instance_RID"], # this is a list to allow for compound foreign keys
    "public",
    "Instance",
    ["RID"], # this is a list to allow for compound keys
    on_update='CASCADE',
    on_delete='SET NULL',
    constraint_names=[ [schema_name, "Step_Instance_RID_fkey"] ],
    comment="Instance_RID must be a valid reference value from the Instance table.",
    acls={},
    acl_bindings={},
    annotations={},
  ),
  ForeignKey.define(
    ["Step_Type_ID"], # this is a list to allow for compound foreign keys
    "Vocab",
    "Step_Type",
    ["id"], # this is a list to allow for compound keys
    on_update='CASCADE',
    on_delete='SET NULL',
    constraint_names=[ [schema_name, "Step_Steptype_ID_fkey"] ],
    comment="Step_Type_ID must be a valid reference value from the Step Type table.",
    acls={},
    acl_bindings={},
    annotations={},
  ),
  ForeignKey.define(
    ["Program_ID"], # this is a list to allow for compound foreign keys
    "Vocab",
    "Program",
    ["id"], # this is a list to allow for compound keys
    on_update='CASCADE',
    on_delete='SET NULL',
    constraint_names=[ [schema_name, "Step_Program_ID_fkey"] ],
    comment="Program_ID must be a valid reference value from the Program table.",
    acls={},
    acl_bindings={},
    annotations={},
  )
]

table_def = Table.define(
  "Step",
  column_defs,
  key_defs=key_defs,
  fkey_defs=fkey_defs,
  comment="Step information of the instance",
  acls={},
  acl_bindings={},
  annotations={},
  provide_system=True,
)

new_table = schema.create_table(catalog, table_def)