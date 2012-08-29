#!/bin/env python
# -*- coding: utf-8 -*-
import sys,os
from xml.dom.minidom import getDOMImplementation
from optparse import OptionParser
#os.path.append("../pyrheviic/")
from rhev_connection import *
import rhev_settings

class NoSuchAttr(Exception):
    def __init__(self, m):
        self.message = m
    def __str__(self):
        return self.message

class NotImplementedYet(Exception):
    def __init__(self, m):
        self.message = m
    def __str__(self):
        return self.message



#################################################
##############  VM XML ##########################
#################################################
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
    memoryNode = document.createTextNode(str(int(memory)*(1024**2)))
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

def createVmXml(vmname,vmdescription,clustername,memory,osparam = None):
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
    if osparam: topElement.appendChild(createOsElement(document,osparam))
    return document.toxml()

######################################################
################# DISK XML ###########################
######################################################
def createDiskXML(amount,disktype):
    """ create XML for attaching disk
    """
    dom = getDOMImplementation()
    document = dom.createDocument(None, "disk", None)
    topElement = document.documentElement
    sdElement = document.createElement("storage_domains")
    sdIdElement = document.createElement("storage_domain")
    sdIdElement.setAttribute("id","FUCK")
    sdElement.appendChild(sdIdElement)
    topElement.appendChild(sdElement)
    sizeElement = document.createElement("size")
    sizeNode = document.createTextNode(str(int(amount)*(1024**3)))
    sizeElement.appendChild(sizeNode)
    topElement.appendChild(sizeElement)
    typeElement = document.createElement("type")
    typeNode = document.createTextNode(disktype)
    typeElement.appendChild(typeNode)
    topElement.appendChild(typeElement)
    formatElement = document.createElement("format")
    formatElement.appendChild(document.createTextNode("cow"))
    topElement.appendChild(formatElement)
    bootableElement = document.createElement("bootable")
    bootableNode = document.createTextNode("true")
    bootableElement.appendChild(bootableNode)
    topElement.appendChild(bootableElement)
    print document.toprettyxml()


    

    """
    <disk>
        <storage_domains>
            <storage_domain id="fabe0451-701f-4235-8f7e-e20e458819ed"/>
        </storage_domains>        
        <size>8589934592</size>
        <type>system</type>
        <interface>virtio</interface>
        <format>cow</format>
        <bootable>true</bootable>
    </disk>
    """
def createVm(vmname,clustername,memory,vmdescription,osparam):
    vmXML = createVmXml(vmname = vmname,
            clustername = clustername,
            memory = memory,
            vmdescription = vmdescription,
            osparam = osparam)
    print vmXML
    #print rhevPost("/api/vms",vmXML)

def testAction():
    osparam = {}
    osparam["bootdev"] = "hd"
    osparam["kernel"] = "/mnt/share/rhel56/x68_64/vmlinuz"
    osparam["initrd"] = "/mnt/share/rhel56/x68_64/initrd.img"
    osparam["cmdline"] = "ip=192.168.0.1 netmask=255.255.255.0 gateway=192.168.0.1 ks=ftp://172.17.211.94/rhelks/some.ks "
    createVm(vmname = "vmname" ,
            clustername = rhev_settings.CLUSTER,
            #memory = str(536870912),
            memory = str(1024*(1024**2)),
            vmdescription = "vmDescription",
            osparam = osparam)

if __name__=="__main__":
    parser = OptionParser()
    parser.add_option("--action","-a",dest="action",help="Action to do: create, test, console,delete,list,adddisk,addnic",)
    parser.add_option("--name","-n",dest="vmname",help="Name of VM")
    parser.add_option("--memory","-m",dest="memory",help="Memory in MB")
    parser.add_option("--description","-d",dest="description",help = "Description of VM")
    parser.add_option("--template","-t",dest="template",help="Template for VM")
    parser.add_option("--disk","-c",dest="hd",help="Ammount of attached disk")
    parser.add_option("--disktype",dest="disktype",help="Type of attached disk (system,data)")
    (options, args) = parser.parse_args()
    if not options.action: 
        print "You MUST specify action"
        sys.exit(1)
    if options.action == "create":
        print "Creating Virutal Machine"
        if not options.vmname:
            print "Name of virtual machine is mandatory"
            sys.exit(1)
        vmname = options.vmname
        if options.memory:
            memory = options.memory
        else:
            memory = 512
        if options.template:
            raise NotImplementedYet("Template option not implemented yet, using Blank")
        description = "Autogenerated VM"
        if options.description:
            description = options.description
        createVm(
                vmname = vmname,
                clustername = rhev_settings.CLUSTER,
                memory = memory,
                vmdescription = description,
                osparam = None
                )
    if options.action == "ticket":
         raise NotImplementedYet("Not implemented yet")
    if options.action == "list":
        if options.vmname:
            getListOfVMs(options.vmname)
        else:
            getListOfVMs()
    if options.action == "adddisk":
        if not options.hd:
            print "Please specify amount of attached dist (-c option)"
            sys.exit(1)
        disktype = "data"
        if options.disktype == "system":
            disktype = "system"
        createDiskXML(options.hd,disktype)
        ## attachDisk(createDiskXML(ammount))
        sys.exit(0)
    if options.action == "test":
        testAction()

