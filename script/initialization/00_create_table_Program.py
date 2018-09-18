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

term_table = 'Program'
term_comment = 'program code of a step'

credential = get_credential(hostname)
catalog = ErmrestCatalog('https', hostname, catalog_number, credentials=credential)

def create_vocabulary_table(catalog,term_table, term_comment):
    model_root = catalog.getCatalogModel()
    new_vocab_table = \
        model_root.schemas[schema_name].create_table(catalog, em.Table.define_vocabulary(term_table,'CORE:{RID}',comment=term_comment)
)
        

create_vocabulary_table(catalog,term_table,term_comment)
model_root = catalog.getCatalogModel()
table = model_root.table(schema_name, term_table)

#create new column
column_def = em.Column.define(
  "Reference",
  em.builtin_types.text,
  nullok=False,
  comment="Should be a reference to a code repository",
  annotations={},
  acls={},
  acl_bindings={},
)

new_column = table.create_column(catalog, column_def)

column_def = em.Column.define(
  "Environment",
  em.builtin_types.text,
  nullok=False,
  comment="Could be a reference to container uri",
  annotations={},
  acls={},
  acl_bindings={},
)

new_column = table.create_column(catalog, column_def)

column_def = em.Column.define(
  "Version",
  em.builtin_types.text,
  nullok=True,
  comment="Program version",
  annotations={},
  acls={},
  acl_bindings={},
)
new_column = table.create_column(catalog, column_def)


#HTTPError: 409 Client Error: Conflict for url: https://leo.isrd.isi.edu/ermrest/catalog/3/schema/vocab/table details: b'409 Conflict\nThe request conflicts with the state of the server. Unsupported type "ermrest_curie"\n'

#https://github.com/informatics-isi-edu/deriva-py/commit/998af940c99ebacecc1a5e55327607f0c4472bf1