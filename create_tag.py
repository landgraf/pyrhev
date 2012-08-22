#!/bin/env python
# -*- coding: utf-8 -*-

import sys
import xml.dom.minidom
from xml.dom.minidom import getDOMImplementation
from rhev_connection import *
import rhev_settings

def createTagXml(tagname,parenttag):
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


def createTag(tagname,parenttag):
    print rhevPost("/api/tags", createTagXml(tagname,parenttag))

if __name__ == '__main__':
    if len(sys.argv) != 2: 
        print "USAGE:\n./createTag <tagName>"
    tagname = sys.argv[1]
    createTag(tagname,getTagData(rhev_settings.TAG,"id"))


