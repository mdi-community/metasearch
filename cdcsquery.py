#!/usr/bin/python

"""
program: query.py
description: script to execute a query on a curator.
"""
from os.path import join
from os import listdir
import requests
from pprint  import pprint
import json
import sys
import os

def do_query(username='',pwd='',url='', quer=''):
#
#Parameters:     username        - username on CDCS instance   (Note:  User must have admin privledges)
                #password        - password on CDCS instance
                #url             - url of CDCS instance
                #quer            - query string
    
    query_url = "/explore/common/rest/local-query"
    turl = url + query_url

    print 'status: Excuting Query.'

    if quer == '': 
      data = { "query": "{}" }
    else:
      data = {
               "query": "{   \
                        \"$and\": [     \
                                {     \
                                   \"$or\": [     \
                                          {     \
                                             \"dict_content.interatomic-potential.element\": \"Ag\"     \
                                          },     \
                                          {     \
                                             \"dict_content.interatomic-potential.element.#text\": \"Ag\"     \
                                          }     \
                                          ]     \
                                }     \
                               ]     \
                        }",     
                       "template": {
                          "$in": [
                             "5cb726f2d2d2054e5f1f5387"
                          ]
                       },
                       "all": "true"
                }


    print "Get:"
    response = requests.get(turl, data=data, verify=False, auth=(username, pwd))
    out = response.json()
    pprint(response)
    pprint(out)
    print "Resp: "
    print response.status_code
    response_code = response.status_code
    response_content = json.loads(response.text)

    resurl = "/explore/common/rest/result"
    turl = url + resurl

    if response_code == requests.codes.ok:
       for rec in response_content:
           pprint(rec)
    else:
        response.raise_for_status()
        raise Exception("- error: a problem occurred when uploading the schema (Error ", response_code, ")")

    print 'status: done.'



def main(argv=[]):
    if ( len(argv) != 5 ):
        print 'usage:   python bulk_upload.py <username> <password> <url> '
        print 'example: python bulk_upload.py blong my_password http://127.0.0.1:8000 '
        exit

    args=argv[1:] # skip arg[0]=bulk_upload.py

    username=args[0]
    pwd=args[1]
    url=args[2]
    quer=args[3]

    do_query(username,pwd,url,quer)

if (__name__ == '__main__' ):
    main(sys.argv)
