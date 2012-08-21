#!/bin/env python
# -*- coding: utf-8 -*-

import sys
import xml.dom.minidom
from xml.dom.minidom import getDOMImplementation
from rhev_connection import *
import libxml2

def create_tag_xml(tagname):
    dom = getDOMImplementation()
    document = dom.createDocument(None, "tag", None)
    topElement = document.documentElement
    firstElement = document.createElement("name")
    parentElement = document.createElement("parent")
    parentidElement = document.createElement('tag id="00000000-0000-0000-0000-000000000000"')
    parentElement.appendChild(parentidElement)
    topElement.appendChild(firstElement)
    topElement.appendChild(parentElement)
    textNode = document.createTextNode(tagname)
    firstElement.appendChild(textNode)
    return document.toxml()

def get_cluster_href(cluster_name):
    clusters = rhev_get("/api/clusters")
    doc = libxml2.parseDoc(clusters)
    ctxt = doc.xpathNewContext()
    res = ctxt.xpathEval("/clusters/cluster[name [position()=1]= '"+ cluster_name + "']")
    for i in res:
        return i.prop('href')

def create_tag(tagname):
    print rhev_post("/api/tags", create_tag_xml(tagname))

if __name__ == '__main__':
    tagname = sys.argv[1]
    conn = rhev_connect()
    create_tag(tagname)
    #print create_tag_xml(tagname)


