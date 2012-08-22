#!/bin/env python
# -*- coding: utf-8 -*-
import sys
import xml.dom.minidom
from xml.dom.minidom import getDOMImplementation
from rhev_connection import *
import libxml2


def createVlanXml(name,description,vlan,stp="true"):
    """ create network XML
    """
    int(vlan)
    dom = getDOMImplementation()
    document = dom.createDocument(None, "network", None)
    topElement = document.documentElement
    nameElement = document.createElement("name")
    vlanElement = document.createElement("vlan")
    vlanElement.setAttribute("id",vlan)
    stpElement = document.createElement("stp")
    dcElement = document.createElement("dataCenter")
    dcElement.setAttribute('id',getDcData(rhev_settings.DC,"id"))
    dcElement.setAttribute('href',getDcData(rhev_settings.DC,"href"))
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

def createActionXml(networkId):
    """ create XML for attach network
        @return xml
    """
    dom = getDOMImplementation()
    document = dom.createDocument(None, "action", None)
    topElement = document.documentElement
    netElement = document.createElement("network")
    netElement.setAttribute('id',networkId)
    topElement.appendChild(netElement)
    return document.toxml()

def createVlan(name, description,vlan):
    """ create new VLAN and attach it to cluster
    """
    print "Creating new logical network"
    networkxml = rhevPost("/api/networks", createVlanXml(name,description,vlan))
    print "Attaching new logical network to cluster " + rhev_settings.CLUSTER
    return rhevPost( getClusterData(rhev_settings.CLUSTER ,"href") + "/networks/" , networkxml)

def attachToAllHosts(networkid):
    """ Attach vlan to all hosts in cluster rhev_settings.CLUSTER
    """
    actionXml =  createActionXml(networkid)
    for host in getAllHosts(rhev_settings.CLUSTER):
        ## Attaching network to host
        rhevPost(host + "/attach" ,actionXml)

def getNetworkId(networkxml):
    """ extract id from XML
    """
    doc = libxml2.parseDoc(networkxml)
    ctxt = doc.xpathNewContext()
    return ctxt.xpathEval("/network[@id]")[0].prop("id")

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print "USAGE:\n./createVlans <VLAN name> <description> <VLAN ID>"
        sys.exit(1)
    vlanname = sys.argv[1]
    vlandescr = sys.argv[2]
    vlanid = sys.argv[3]
    networkxml = createVlan(vlanname,vlandescr,vlanid)
    attachToAllHosts(getNetworkId(networkxml))
