#!/bin/env python

import sys
from xml.dom.minidom import getDOMImplementation
from rhev_connection import *

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
    clusters = rhev_get("/api/clusters")


if __name__ == '__main__':
    tagname = sys.argv[1]
    conn = rhev_connect()
    get_cluster_uuid("Projects")
    #print create_tag_xml(tagname)


