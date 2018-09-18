# -*- coding: utf-8 -*-
"""
Created on Thu Aug  2 16:09:42 2018

@author: qingj
"""

from deriva.core import HatracStore, ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('hostname')
parser.add_argument('catalog_number')
parser.add_argument('schema_name')
args = parser.parse_args()


hostname = args.hostname
schema_name = args.schema_name
catalog_number = args.catalog_number

term_table = 'Subdomain'
term_comment = 'subdomain'

credential = get_credential(hostname)
catalog = ErmrestCatalog('https', hostname, catalog_number, credentials=credential)

def create_vocabulary_table(catalog,term_table, term_comment):
    model_root = catalog.getCatalogModel()
    new_vocab_table = \
        model_root.schemas[schema_name].create_table(catalog, em.Table.define_vocabulary(term_table,'CORE:{RID}',comment=term_comment)
)
        

create_vocabulary_table(catalog,term_table,term_comment)

#create new column
column_def = em.Column.define(
  "Domain_ID",
  em.builtin_types.text,
  nullok=False,
  comment="A column reference to Domain table",
  annotations={},
  acls={},
  acl_bindings={},
)

model_root = catalog.getCatalogModel()
table = model_root.table(schema_name, term_table)
new_column = table.create_column(catalog, column_def)

#create new foreign key
fkey_def =  em.ForeignKey.define(
    ["Domain_ID"], # this is a list to allow for compound foreign keys
    "Vocab",
    "Domain",
    ["id"], # this is a list to allow for compound keys
    on_update='CASCADE',
    on_delete='SET NULL',
    constraint_names=[ [schema_name, "Subdomain_Domain_ID_fkey"] ],
    comment="Domain_ID must be a valid reference value from the Domain table.",
    acls={},
    acl_bindings={},
    annotations={},
  )

table.create_fkey(catalog, fkey_def)

#HTTPError: 409 Client Error: Conflict for url: https://leo.isrd.isi.edu/ermrest/catalog/3/schema/vocab/table details: b'409 Conflict\nThe request conflicts with the state of the server. Unsupported type "ermrest_curie"\n'

#https://github.com/informatics-isi-edu/deriva-py/commit/998af940c99ebacecc1a5e55327607f0c4472bf1