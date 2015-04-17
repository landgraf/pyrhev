#!/bin/env python
# -*- coding: utf-8 -*-

import httplib,urllib
import base64,sys
import string
import libxml2


### CHANGE LINES BELOW
username = "admin@internal"
password = "secret"
host = "rhevm.example.com"
storage_domain = "ee1e63fc-ec4a-4b34-ae37-c2afc15bcbfa"
### CHANGE LINES ABOVE


def rhevConnect():
    """ Just connect to RHEVM using HTTPS
        HTTP not supported yet
    """
    rhev = host
    conn = httplib.HTTPSConnection(rhev)
    return conn

def getHeaders():
    """ get headers for HTTPS connection
    """
    userid = username
    passwd = password
    # base64.encodestring adds trailing \n. 
    auth = base64.encodestring("%s:%s" % (userid, passwd)).rstrip("\n")
    headers = {"Content-Type": "application/xml",
                     "Accept": "application/xml",
                     "Accept-Charset": "utf-8",
                     "Authorization" : ("Basic %s" % auth)}
    return headers

def rhevGet(url):
    """ Make GET request
    """
    conn = rhevConnect()
    conn.request("GET",url,None,getHeaders())
    r = conn.getresponse()
    return r.read()

def rhevPost(url,data):
    """ Make POST request, send data
    """
    conn = rhevConnect()
    conn.request("POST", url, body = data.encode('utf-8'), headers = getHeaders())
    print url
    r = conn.getresponse()
    ## DEBUG 
    ## TODO: check status 
    status = r.read()
    print r.status,r.reason
    if int(r.status)>=400:
        print r.reason
        print status
    return status

def getIds (disks_xml):
    disks = []
    doc = libxml2.parseDoc(disks_xml)
    ctxt = doc.xpathNewContext()
    res = ctxt.xpathEval("/disks/disk[@id]")
    for disk in res:
      disks.append(disk.prop("id"))
      print disk.prop ("id")
    return disks

def register (disks_array):
    for disk in disks_array:
      data = '<disk id="%s"></disk>' %disk
      url = "/api/storagedomains/%s/disks;unregistered=true" %storage_domain
      print "registering disk %s using data %s" %(disk, data)
      rhevPost(url, data)

if __name__=="__main__":
  unregistered_disks = rhevGet("/api/storagedomains/%s/disks;unregistered=true" %storage_domain)
  ids = getIds(unregistered_disks)
  print ids
  register(ids)
