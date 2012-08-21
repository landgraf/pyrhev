#!/bin/env python
# -*- coding: utf-8 -*-

import sys
import xml.dom.minidom
from xml.dom.minidom import getDOMImplementation
from rhev_connection import *
import libxml2

def create_tag_xml(tagname,parenttag):
    dom = getDOMImplementation()
    document = dom.createDocument(None, "tag", None)
    topElement = document.documentElement
    firstElement = document.createElement("name")
    parentElement = document.createElement("parent")
    parentidElement = document.createElement('tag id="'+ parenttag + '"')
    parentElement.appendChild(parentidElement)
    topElement.appendChild(firstElement)
    topElement.appendChild(parentElement)
    textNode = document.createTextNode(tagname)
    firstElement.appendChild(textNode)
    return document.toxml()
def get_tag_uuid(tagname):
    tags = rhev_get("/api/tags")
    doc = libxml2.parseDoc(tags)
    ctxt = doc.xpathNewContext()
    res = ctxt.xpathEval("/tags/tag[name[position()=1]= '" + tagname + "']")
    for i in res:
        return i.prop("id")

def get_cluster_href(cluster_name):
    clusters = rhev_get("/api/clusters")
    doc = libxml2.parseDoc(clusters)
    ctxt = doc.xpathNewContext()
    res = ctxt.xpathEval("/clusters/cluster[name [position()=1]= '"+ cluster_name + "']")
    for i in res:
        return i.prop('href')

def create_tag(tagname,parenttag):
    print rhev_post("/api/tags", create_tag_xml(tagname,parenttag))

if __name__ == '__main__':
    if len(sys.argv) != 2: sys.exit(1)
    tagname = sys.argv[1]
    create_tag(tagname,get_tag_uuid("projects"))


