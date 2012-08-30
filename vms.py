#!/bin/env python2
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

def exit(message):
    print message
    sys.exit(1)


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
def createDiskXML(vmid, sd, amount,disktype):
    """ create XML for attaching disk
    """
    """
    EXAMPLE:
    <disk>
    </disk>
    """
    dom = getDOMImplementation()
    document = dom.createDocument(None, "disk", None)
    topElement = document.documentElement
    """
        <storage_domains>
            <storage_domain id="fabe0451-701f-4235-8f7e-e20e458819ed"/>
        </storage_domains>        
    """
    sdElement = document.createElement("storage_domains")
    sdIdElement = document.createElement("storage_domain")
    sdIdElement.setAttribute("id",sd)
    sdElement.appendChild(sdIdElement)
    topElement.appendChild(sdElement)
    """
        <size>8589934592</size>
    """
    sizeElement = document.createElement("size")
    sizeNode = document.createTextNode(str(int(amount)*(1024**3)))
    sizeElement.appendChild(sizeNode)
    topElement.appendChild(sizeElement)
    """
        <type>system</type>
    """
    typeElement = document.createElement("type")
    typeNode = document.createTextNode(disktype)
    typeElement.appendChild(typeNode)
    topElement.appendChild(typeElement)
    """
        <interface>virtio</interface>
    """
    interfaceElement = document.createElement("interface")
    interfaceNode = document.createTextNode("virtio")
    interfaceElement.appendChild(interfaceNode)
    topElement.appendChild(interfaceElement)
    """
        <format>cow</format>
    """
    formatElement = document.createElement("format")
    formatElement.appendChild(document.createTextNode("cow"))
    topElement.appendChild(formatElement)
    """
        <bootable>true</bootable>
    """
    bootableElement = document.createElement("bootable")
    bootableNode = document.createTextNode("false")
    ## Check if first disk
    if numberOfDisks(vmid) == 0: bootableNode = document.createTextNode("true")
    bootableElement.appendChild(bootableNode)
    topElement.appendChild(bootableElement)
    return document.toxml()


###################################################################
######################## NETWORK XML ##############################
###################################################################
def createNetworkXML(name,id):
    """ Create XML for network """
    """
    <nic>
        <type>e1000</type>
        </nic>
    """
    dom = getDOMImplementation()
    document = dom.createDocument(None, "nic", None)
    topElement = document.documentElement
    """
        <name>nic2</name>
    """
    NameElement = document.createElement("name")
    NameNode = document.createTextNode(name)
    NameElement.appendChild(NameNode)
    topElement.appendChild(NameElement)
    """
        <network id="00000000-0000-0000-0000-000000000010"/>
    """
    networkElement = document.createElement("network")
    networkElement.setAttribute("id",id)
    topElement.appendChild(networkElement)
    return document.toxml()




def createVm(vmname,clustername,memory,vmdescription,osparam):
    vmXML = createVmXml(vmname = vmname,
            clustername = clustername,
            memory = memory,
            vmdescription = vmdescription,
            osparam = osparam)
    print rhevPost("/api/vms",vmXML)

def testAction():
    osparam = {}
    osparam["bootdev"] = "hd"
    osparam["kernel"] = "/mnt/share/rhel56/x68_64/vmlinuz"
    osparam["initrd"] = "/mnt/share/rhel56/x68_64/initrd.img"
    osparam["cmdline"] = "ip=192.168.0.1 netmask=255.255.255.0 gateway=192.168.0.1 ks=ftp://172.17.211.94/rhelks/some.ks "
    createVm(vmname = "vmname" ,
            clustername = rhev_settings.CLUSTER,
            #memory = str(536870912),
            memory = 1024,
            vmdescription = "vmDescription",
            osparam = osparam)

def vmSelect(name):
    selector = getListOfVMs(name,True)
    number = len(selector)
    if number == 0 :
        exit("VM not found exiting")
    if number == 1:
        print "Founded 1 VM %s, using it"%selector[0]["name"]
        return selector[0]["id"]
    print "%d VM is (are) founded please select"%int(number)
    for i in selector:
        print "%d) %s "%(selector.index(i),i["name"])
    a = input("Please specify:")
    print "VM %s selected"%selector[a]["name"]
    return selector[a]["id"]

def sdSelect(name):
    selector = getListOfSDs(name,True)
    number = len(selector)
    if number == 0 : 
        exit("SD not found exiting")
    print "%d SD is (are) founded please select"%int(number)
    for i in selector:
        print "%d) %s "%(selector.index(i),i["name"])
    a = input("Please specify:")
    print "SD %s selected"%selector[a]["name"]
    return selector[a]["id"]

def networkSelect(name):
    selector = getListOfVlans(name,True)
    number = len(selector)
    if number == 0:
        exit("Network not found, exiting")
    print "%d network(s) is (are) founded please select"%int(number)
    for i in selector:
        print "%d) %s "%(selector.index(i),i["name"])
    a = input("Please specify:")
    print "Network %s selected"%selector[a]["name"]
    return getNetworkData(selector[a]["name"],"id")

def attachDisk(vmid,diskXML):
    if not vmid:
        exit("VM not specified exiting...")
    print rhevPost("/api/vms/"+ vmid + "/disks" ,diskXML)

def set_parser():
    parser = OptionParser()
    parser.add_option("--action","-a",dest="action",help="Action to do: create, test, console,delete,list,adddisk,addnic",)
    parser.add_option("--name","-n",dest="vmname",help="Name of VM")
    parser.add_option("--memory","-m",dest="memory",help="Memory in MB")
    parser.add_option("--description","-d",dest="description",help = "Description of VM")
    parser.add_option("--template","-t",dest="template",help="Template for VM")
    parser.add_option("--disk","-c",dest="hd",help="Ammount of attached disk")
    parser.add_option("--disktype",dest="disktype",help="Type of attached disk (system,data)")
    parser.add_option("--network",dest="network",help="Name of exiting (new) network")
    parser.add_option("--vlan","-v",dest="vlan",help="VLAN ID of attaching network")
    (options, args) = parser.parse_args()
    return options

def process_create(options):
    print "Creating Virutal Machine"
    if not options.vmname:
        exit("Name of virtual machine is mandatory")
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

def processAddDisk(options):
    if not options.hd:
        exit("Please specify amount of attached dist (-c option)")
    disktype = "data"
    if options.disktype == "system":
        disktype = "system"
    vmid = vmSelect(options.vmname or "")
    sd = sdSelect(None)
    attachDisk(vmid,createDiskXML(vmid,sd,options.hd,disktype))

def processAddNIC(options):
    if not options.network and not options.vlan:
        exit("Please specify network name or part of network name")
    if options.network and options.vlan:
        a = raw_input("Ypu've specified both network and VLANID. Would you like to create new network? (y/n): " )
        if a == 'n' or "N":
            exit("Exiting")
        raise NotImplementedYet("Please create network before")
    else:
        netid = networkSelect(options.network or options.vlan)
        vmid = vmSelect(options.vmname or "")
        rhevPost("/api/vms/" + vmid + "/nics",createNetworkXML("nic1",netid))

if __name__=="__main__":
    options = set_parser()
    if not options.action:
        exit("You MUST specify action")
    if options.action == "create":
        process_create(options)
    if options.action == "addnetwork":
        processAddNIC(options)
    if options.action == "adddisk":
        processAddDisk(options)
    if options.action == "ticket":
         raise NotImplementedYet("Not implemented yet")
    if options.action == "list":
        if options.vmname:
            getListOfVMs(options.vmname)
        else:
            getListOfVMs()
    if options.action == "test":
        testAction()

