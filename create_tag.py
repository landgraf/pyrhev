#!/bin/env python


import sys,os,httplib
from xml.dom.minidom import getDOMImplementation

def create_tag_xml(tagname):
    dom = getDOMImplementation()
    document = dom.createDocument(None, "tag", None)
    topElement = document.documentElement
    firstElement = document.createElement("name")
    topElement.appendChild(firstElement)
    textNode = document.createTextNode(tagname)
    firstElement.appendChild(textNode)
    xmlString = document.toprettyxml(" " * 4)
    return xmlString


def get_cluster_uuid(cluster_name):
    conn.request("GET","/api/clusters")
    r = conn.getresponse()
    print r.status, r.reason

def rhev_post(xml):
    conn.request("POST", "/", params, headers)
    pass

if __name__ == '__main__':
    tagname = sys.argv[1]
    conn = httplib.HTTPSConnection("172.17.193.70:8443")
    headers = {"Content-type": "application/xml",
                     "Accept": "application/xml"}
    get_cluster_uuid("Projects")
    #print create_tag_xml(tagname)


