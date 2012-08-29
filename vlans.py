#!/bin/env python
# -*- coding: utf-8 -*-
import sys
import xml.dom.minidom
from xml.dom.minidom import getDOMImplementation
from rhev_connection import *
import libxml2
from optparse import OptionParser


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
    dcElement = document.createElement("data_center")
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
    parser = OptionParser()
    parser.add_option("--action","-a",dest="action",help="Action to do",)
    parser.add_option("--projectname","-p", dest="project", help="Coded name of project")
    parser.add_option("--vlanid",dest="vlanid",help = "VLAN ID")
    (options, args) = parser.parse_args()
    if not options.action:
        print "You MUST specify action"
        sys.exit(1)
    if options.action == "list":
        if not options.vlanid and not options.project: 
            getListOfVlans()
            sys.exit(0)
        if options.vlanid:
            print "Searching by VLANID"
            getListOfVlans(options.vlanid)
        if options.project:
            print "Searching by network name"
            getListOfVlans(options.project)
        sys,exit(0)
    if options.action == "create":
        print "Create"
        if not options.project or not options.vlanid:
            print "You MUST specify both project and vlanid options"
            sys.exit(1)
        try :
            int(options.vlanid)
        except :
            print "VLANID MUST be a number"
            sys,exit(1)
        networkxml = createVlan(options.project,"VLAN" + options.vlanid.strip(), options.vlanid)
        attachToAllHosts(getNetworkId(networkxml))
        sys,exit(0)
    print "No such action %s, please read help and try again" %options.action
    sys.exit(1)


    #networkxml = createVlan(vlanname,vlandescr,vlanid)
    #attachToAllHosts(getNetworkId(networkxml))
