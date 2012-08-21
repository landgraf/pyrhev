#!/bin/env python
# -*- coding: utf-8 -*-
import sys
import xml.dom.minidom
from xml.dom.minidom import getDOMImplementation
from rhev_connection import *
import libxml2

def get_dc_data(dc_name,data):
    clusters = rhev_get("/api/datacenters")
    doc = libxml2.parseDoc(clusters)
    ctxt = doc.xpathNewContext()
    res = ctxt.xpathEval("/data_centers/data_center[name [position()=1]= '"+ dc_name + "']")
    for i in res:
        print i.prop(data)
        return i.prop(data)

def create_vlan_xml(name,description,vlan,stp="true"):
    dom = getDOMImplementation()
    document = dom.createDocument(None, "network", None)
    topElement = document.documentElement
    nameElement = document.createElement("name")
    vlanElement = document.createElement("vlan")
    vlanElement.setAttribute("id",vlan)
    stpElement = document.createElement("stp")
    dcElement = document.createElement("data_center")
    dcElement.setAttribute('id',get_dc_data("IIC_Projects","id"))
    dcElement.setAttribute('href',get_dc_data("IIC_Projects","href"))
    descriptionElement = document.createElement("description")
    topElement.appendChild(nameElement)
    topElement.appendChild(descriptionElement)
    topElement.appendChild(dcElement)
    topElement.appendChild(vlanElement)
    topElement.appendChild(stpElement)
    nameNode = document.createTextNode(name)
    descriptionNode = document.createTextNode(description)
    stpNode = document.createTextNode("true")
    nameElement.appendChild(nameNode)
    stpElement.appendChild(stpNode)
    descriptionElement.appendChild(descriptionNode)
    print document.toxml()
    return document.toxml()

def create_vlan(name, description,vlan):
    print rhev_post("/api/networks", create_vlan_xml(name,description,vlan))

if __name__ == '__main__':
    if len(sys.argv) != 4: sys.exit(1)
    vlanname = sys.argv[1]
    vlandescr = sys.argv[2]
    vlanid = sys.argv[3]
    create_vlan(vlanname,vlandescr,vlanid)
