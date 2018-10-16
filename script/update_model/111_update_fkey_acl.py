from deriva.core import DerivaServer, ErmrestCatalog, HatracStore, AttrDict,get_credential
from deriva.core.ermrest_model import builtin_types, Table, Column, Key, ForeignKey

# replace this with your real server FQDN
servername = "leo.isrd.isi.edu"
credentials = get_credential(servername)
catalog_number = 1

# replace these with your real group IDs
#"curator": "https://auth.globus.org/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
server = DerivaServer('https', servername, credentials)
catalog = ErmrestCatalog('https', servername, catalog_number, credentials)


grps = AttrDict({
  "admin":   "https://auth.globus.org/80af39fa-9503-11e8-88d8-0a7d99bc78fe",
  "writer":  "https://auth.globus.org/72bdb36c-9503-11e8-8c03-0e847f194132",
  "reader":  "https://auth.globus.org/5bd8b30e-9503-11e8-ba34-0e5b3fbbcf14"
})

model = catalog.getCatalogModel()

print catalog._catalog_id

schema_name = 'Core'
schema = model.schemas[schema_name]

child_table = schema.tables['Step']

child_fkey = child_table.foreign_keys[
  (schema_name, "Step_Instance_RID_fkey")
]

child_fkey.acls.update({
  "insert": [],
  "update": [],
})

child_fkey.acl_bindings.update({
  "self_linkage": {
    "types": ["insert", "update"],
    "projection": ["RCB"],
    "projection_type": "acl",
  }
})


# apply these local config changes to the server
model.apply(catalog)