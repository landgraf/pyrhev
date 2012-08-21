#!/bin/env python
# -*- coding: utf-8 -*-
import sys
import xml.dom.minidom
from xml.dom.minidom import getDOMImplementation
from rhev_connection import *
import libxml2


def create_vlan_xml(name,description,vlan,stp="true"):
    dom = getDOMImplementation()
    document = dom.createDocument(None, "network", None)
    topElement = document.documentElement
    nameElement = document.createElement("name")
    vlanElement = document.createElement("vlan")
    vlanElement.setAttribute("id",vlan)
    stpElement = document.createElement("stp")
    dcElement = document.createElement("data_center")
    dcElement.setAttribute('id',get_dc_data(rhev_settings.DC,"id"))
    dcElement.setAttribute('href',get_dc_data(rhev_settings.DC,"href"))
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

def create_action_xml(network_id):
    dom = getDOMImplementation()
    document = dom.createDocument(None, "action", None)
    topElement = document.documentElement
    netElement = document.createElement("network")
    netElement.setAttribute('id',network_id)
    topElement.appendChild(netElement)
    return document.toxml()

def create_vlan(name, description,vlan):
    print "Creating new logical network"
    networkxml = rhev_post("/api/networks", create_vlan_xml(name,description,vlan))
    print "Attaching new logical network to cluster " + rhev_settings.CLUSTER
    return rhev_post( get_cluster_data(rhev_settings.CLUSTER ,"href") + "/networks/" , networkxml)

def attach_to_all_hosts(networkid):
    action_xml =  create_action_xml(networkid)
    for host in get_all_hosts(rhev_settings.CLUSTER):
        ## Attaching network to host
        rhev_post(host + "/attach" ,action_xml)

def get_network_id(networkxml):
    doc = libxml2.parseDoc(networkxml)
    ctxt = doc.xpathNewContext()
    return ctxt.xpathEval("/network[@id]")[0].prop("id")

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print "USAGE:\n./create_vlans <VLAN name> <description> <VLAN ID>"
        sys.exit(1)
    vlanname = sys.argv[1]
    vlandescr = sys.argv[2]
    vlanid = sys.argv[3]
    networkxml = create_vlan(vlanname,vlandescr,vlanid)
    attach_to_all_hosts(get_network_id(networkxml))
