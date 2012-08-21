#!/bin/env python
# -*- coding: utf-8 -*-

import sys
import xml.dom.minidom
from xml.dom.minidom import getDOMImplementation
from rhev_connection import *
import rhev_settings

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


def create_tag(tagname,parenttag):
    print rhev_post("/api/tags", create_tag_xml(tagname,parenttag))

if __name__ == '__main__':
    if len(sys.argv) != 2: 
        print "USAGE:\n./create_tag <tag_name>"
    tagname = sys.argv[1]
    create_tag(tagname,get_tag_data(rhev_settings.TAG,"id"))


