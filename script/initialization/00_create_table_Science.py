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

term_table = 'Science'
term_comment = ''

credential = get_credential(hostname)
catalog = ErmrestCatalog('https', hostname, catalog_number, credentials=credential)

def create_vocabulary_table(catalog,term_table, term_comment):
    model_root = catalog.getCatalogModel()
    new_vocab_table = \
        model_root.schemas[schema_name].create_table(catalog, em.Table.define_vocabulary(term_table,'CORE:{RID}',comment=term_comment)
)
        

create_vocabulary_table(catalog,term_table,term_comment)

