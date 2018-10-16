from requests import HTTPError
from deriva.core import DerivaServer, ErmrestCatalog, get_credential
from deriva.core.ermrest_model import Table, Column, Key, builtin_types


hostname = 'leo.isrd.isi.edu'
catalog_number = 1

credential = get_credential(hostname)
server = DerivaServer('https', hostname, credential)
catalog = ErmrestCatalog('https', hostname, catalog_number, credential)

model_root = catalog.getCatalogModel()


print("Catalog ID: {}".format(catalog._catalog_id))


schema = 'Core'
schema = model_root.schemas[schema]

table_list = ['Step_Input_File','Step_Output_File','Step_Program','Instance','Step','Program','File','Instance_Keywords']
    
self_service_policy = {
  "self_service": {
    "types": ["update", "delete"],
    "projection": ["RCB"],
    "projection_type": "acl"
                 }
  }
  
for i in range(len(table_list)):
    if table_list[i] in schema.tables.keys():
        tab = schema.tables[table_list[i]]
        tab.acl_bindings.update(self_service_policy)
        print('table acl updated: %s',table_list[i])
    else:
        print('table not exist: %s',table_list[i])
        

# apply these local config changes to the server
model_root.apply(catalog)