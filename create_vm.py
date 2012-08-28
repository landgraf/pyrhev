#!/bin/env python
# -*- coding: utf-8 -*-
import sys,os
from xml.dom.minidom import getDOMImplementation
#os.path.append("../pyrheviic/")
from rhev_connection import *
import rhev_settings

class NoSuchAttr(Exception):
    def __init__(self, m):
        self.message = m
    def __str__(self):
        return self.message

def createNameElement(document,vmname):
    """
    <name>vm1</name>
    """
    nameElement = document.createElement("name")
    nameNode = document.createTextNode(vmname)
    nameElement.appendChild(nameNode)
    return nameElement

def createClusterElement(document,clustername):
    """
    <cluster>
          <name>default</name>
    </cluster>
    """
    clusterElement = document.createElement("cluster")
    clusterNameElement = document.createElement("name")
    clusterNameNode = document.createTextNode(clustername)
    clusterNameElement.appendChild(clusterNameNode)
    clusterElement.appendChild(clusterNameElement)
    return clusterElement


def createTemplateElement(document,templatename = "Blank"):
    """
    <template>
          <name>Blank</name>
    </template>
    """
    templateElement = document.createElement("template")
    nameElement = document.createElement("name")
    nameNode = document.createTextNode(templatename)
    nameElement.appendChild(nameNode)
    templateElement.appendChild(nameElement)
    return templateElement

def createMemoryElement(document,memory):
    """
      <memory>536870912</memory> 
    """
    memoryElement = document.createElement("memory")
    memoryNode = document.createTextNode(memory)
    memoryElement.appendChild(memoryNode)
    return memoryElement

def createOsElement(document,osparam):
    """
    <os>
       <boot dev="hd"/>
    </os>
    """
    osElement = None
    osElement = document.createElement("os")
    if osparam.has_key("bootdev"):
        osBootElement = document.createElement("boot")
        osBootElement.setAttribute("dev",osparam["bootdev"])
        osElement.appendChild(osBootElement)
        if osparam.has_key("kernel"):
            kernelElement = document.createElement("kernel")
            kernelNode = document.createTextNode(osparam["kernel"])
            kernelElement.appendChild(kernelNode)
            osElement.appendChild(kernelElement)
            if osparam.has_key("initrd"):
                initrdElement = document.createElement("initrd")
                initrdNode = document.createTextNode(osparam["initrd"])
                initrdElement.appendChild(initrdNode)
                osElement.appendChild(initrdElement)
                cmdlineElement = document.createElement("cmdline")
                if osparam.has_key("cmdline"):
                    cmdlineNpde = document.createTextNode(osparam["cmdline"])
                    cmdlineElement.appendChild(cmdlineNpde)
                osElement.appendChild(cmdlineElement)
    if osElement: return osElement

def createDescriptionElement(document,description):
    """
    <description>Imported with virt-v2v</description>
    """
    descriptionElement = document.createElement("description")
    descriptionNode = document.createTextNode(description)
    descriptionElement.appendChild(descriptionNode)
    return descriptionElement

def createVmXml(vmname,vmdescription,clustername,memory,osparam):
    """ 
    create network XML
    """
    dom = getDOMImplementation()
    document = dom.createDocument(None, "vm", None)
    topElement = document.documentElement
    """
    append all childs to top element
    """
    topElement.appendChild(createNameElement(document,vmname))
    topElement.appendChild(createClusterElement(document,clustername))
    topElement.appendChild(createDescriptionElement(document,vmdescription))
    topElement.appendChild(createMemoryElement(document,memory))
    topElement.appendChild(createTemplateElement(document))
    topElement.appendChild(createOsElement(document,osparam))
    print document.toprettyxml()
    return document.toxml()

def create_vm(vmname,clustername,memory,vmdescription,osparam):
    vmXML = createVmXml(vmname = vmname,
            clustername = clustername,
            memory = memory,
            vmdescription = vmdescription,
            osparam = osparam)
    print rhevPost("/api/vms",vmXML)

if __name__=="__main__":
    osparam = {}
    osparam["bootdev"] = "hd"
    osparam["kernel"] = "/mnt/share/rhel56/x68_64/vmlinuz"
    osparam["initrd"] = "/mnt/share/rhel56/x68_64/initrd.img"
    osparam["cmdline"] = "ip=192.168.0.1 netmask=255.255.255.0 gateway=192.168.0.1 ks=ftp://172.17.211.94/rhelks/some.ks "
    create_vm(vmname = "vmname" ,
            clustername = rhev_settings.CLUSTER,
            #memory = str(536870912),
            memory = str(1024*(1024**2)),
            vmdescription = "vmDescription",
            osparam = osparam)
