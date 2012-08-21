#!/bin/env python


import sys,os,httplib
from xml.dom.minidom import getDOMImplementation
import base64
import string
import rhev_settings

def create_tag_xml(tagname):
    dom = getDOMImplementation()
    document = dom.createDocument(None, "tag", None)
    topElement = document.documentElement
    firstElement = document.createElement("name")
    topElement.appendChild(firstElement)
    textNode = document.createTextNode(tagname)
    firstElement.appendChild(textNode)
    xmlString = document.toprettyxml(" " * 4)
    return  xmlString


def get_cluster_uuid(cluster_name):
    conn.request("GET","/api/clusters",None,headers)
    r = conn.getresponse()
    print  r.status, r.reason

def rhev_post(xml):
    conn.request("POST", "/", params, headers)
    pass 

if __name__ == '__main__':
    tagname = sys.argv[1]
    ## TODO Move this staff to untracked file
    userid = rhev_settings.USERNAME
    passwd = rhev_settings.PASSWORD
    rhev = rhev_settings.HOST_PORT
    auth = base64.encodestring("%s:%s" % (userid, passwd))
    conn = httplib.HTTPSConnection(rhev)
    headers = {"Content-type": "application/xml",
                     "Accept": "application/xml",
                     "Authorization" : "Basic %s" % auth}
    get_cluster_uuid("Projects")
    #print create_tag_xml(tagname)


