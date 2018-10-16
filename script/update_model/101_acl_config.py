from deriva.core import DerivaServer, ErmrestCatalog, HatracStore, AttrDict,get_credential
from deriva.core.ermrest_model import builtin_types, Table, Column, Key, ForeignKey

# replace this with your real server FQDN
servername = "leo.isrd.isi.edu"
servername = "hdsca.isrd.isi.edu"
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

print(catalog._catalog_id)

model.acls.update({
  "owner": [grps.admin],
  "insert": [grps.writer],
  "update": [],
  "delete": [],
  "select": [grps.writer, grps.reader],
  "enumerate": ["*"],
})

#schema = model.schemas['Core']
schema = model.schemas['public']
tab_list = ['ermrest_client']
for tab_name in tab_list:
    tab = schema.tables[tab_name]
    tab.acls.update({
      "owner": [grps.admin],
      "insert": [grps.writer],
      "update": [],
      "delete": [],
      "select": [grps.writer, grps.reader],
      "enumerate": ["*"],
    })

# apply these local config changes to the server
model.apply(catalog)