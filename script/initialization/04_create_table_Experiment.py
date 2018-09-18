# -*- coding: utf-8 -*-
"""
Created on Wed Aug  1 15:54:12 2018

@author: qingj
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Jul 30 12:30:13 2018

@author: qingj
"""


from deriva.core import DerivaServer, get_credential
from deriva.core.ermrest_model import Table, Column, Key, ForeignKey,builtin_types as typ
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
  Column.define("Description", typ.text), 
  Column.define("Subdomain_ID", typ.text), 
]
key_defs = [
  Key.define(
    ["Name"], # this is a list to allow for compound keys
    constraint_names=[ [schema_name, "Instance_Name_key"] ],
    comment="Instance name must be distinct.",
    annotations={},
  )
]

fkey_defs = [
  ForeignKey.define(
    ["Subdomain_ID"], # this is a list to allow for compound foreign keys
    "Vocab",
    "Subdomain",
    ["id"], # this is a list to allow for compound keys
    on_update='CASCADE',
    on_delete='SET NULL',
    constraint_names=[ [schema_name, "Instance_Subdomain_RID_fkey"] ],
    comment="Subdomain_RID must be a valid reference value from the Subdomain table.",
    acls={},
    acl_bindings={},
    annotations={},
  )
]

table_def = Table.define(
  "Instance",
  column_defs,
  key_defs=key_defs,
  fkey_defs=fkey_defs,
  comment="an instance information under one subdomain",
  acls={},
  acl_bindings={},
  annotations={},
  provide_system=True,
)

new_table = schema.create_table(catalog, table_def)