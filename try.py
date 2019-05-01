#! /usr/bin/python3
import metasearch as ms

fed = ms.createDefaultFederation()
query = fed.createQuery()
query.add_freetext_constraint("data")
res = query.submit()

