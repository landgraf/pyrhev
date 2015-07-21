#!/bin/env python
# -*- coding: utf-8 -*-
import httplib,urllib
import base64,sys
import string
import libxml2
import rhev_settings

def numberOfDisks(vmid):
    disks = rhevGet("/api/vms/" + vmid + "/disks")
    doc = libxml2.parseDoc(disks)
    ctxt = doc.xpathNewContext()
    res = ctxt.xpathEval("/disks/disk")
    return len(res)


def getHeaders():
    """ get headers for HTTPS connection
    """
    userid = rhev_settings.USERNAME
    passwd = rhev_settings.PASSWORD
    # base64.encodestring adds trailing \n. 
    auth = base64.encodestring("%s:%s" % (userid, passwd)).rstrip("\n")
    headers = {"Content-Type": "application/xml",
                     "Accept": "application/xml",
                     "Accept-Charset": "utf-8",
                     "Authorization" : ("Basic %s" % auth)}
    return headers

def getTagData(tagname,data):
    """ Get properties of tag
        return property for parent tag
    """
    tags = rhevGet("/api/tags")
    doc = libxml2.parseDoc(tags)
    ctxt = doc.xpathNewContext()
    res = ctxt.xpathEval("/tags/tag[name[position()=1]= '" + tagname + "']")
    return res[0].prop(data)

def getClusterData(clusterName,data):
    """ Get properties of cluster
    """
    clusters = rhevGet("/api/clusters")
    doc = libxml2.parseDoc(clusters)
    ctxt = doc.xpathNewContext()
    res = ctxt.xpathEval("/clusters/cluster[name [position()=1]= '"+ clusterName + "']")
    return res[0].prop(data)

def getNetworkData(name,data):
    networks = rhevGet("/api/networks")
    doc = libxml2.parseDoc(networks)
    ctxt = doc.xpathNewContext()
    res = ctxt.xpathEval("/networks/network[name [position()=1]= '"+ name + "']")
    return res[0].prop(data)

def getListOfVMs(name = None,selector = None):
    """ get getListOfVMs 
    if name is specified search by name
    """
    if name:
        vms = rhevGet("/api/vms?search=name%3D*" + name + "*")
    else:
        vms = rhevGet("/api/vms")
    doc = libxml2.parseDoc(vms)
    ctxt = doc.xpathNewContext()
    res = ctxt.xpathEval("/vms/vm[cluster/@id='"+ getClusterData(rhev_settings.CLUSTER ,"id") + "']")
    if not selector:
        for vm in res:
            print "Name %s\t\t\t\t\tID: %s"%(vm.firstElementChild().get_content(),vm.prop("id"))
        return None
    vms = []
    for v in res:
        vm = {}
        vm["name"] = v.firstElementChild().get_content()
        vm["id"] = v.prop("id")
        vms.append(vm)
    return vms

def getListOfSDs(name = None,selector = None):
    """ Get list of storage domains for DC specified in rhev_settings """
    sds = rhevGet("/api/datacenters/%s/storagedomains"%getDcData(rhev_settings.DC,"id"))
    doc = libxml2.parseDoc(sds)
    ctxt = doc.xpathNewContext()
    res = ctxt.xpathEval("/storage_domains/storage_domain")
    sdlist = []
    for sd in res:
        sdin = {}
        sdin["name"] = sd.firstElementChild().get_content()
        sdin["id"] = sd.prop("id")
        sdlist.append(sdin)
    result = []
    if name:
        result = [sdin for sdin in sdlist if sdin["name"].find(name) != -1]
    return result or sdlist

def getListOfVlans(search=None,selector = None):
    """ get list of dictionaries of networks """
    networksxml = rhevGet("/api/networks")
    doc = libxml2.parseDoc(networksxml)
    ctxt = doc.xpathNewContext()
    res = ctxt.xpathEval("/networks/network/data_center[@id='"  + getDcData(rhev_settings.DC ,"id") + "']/../*[self::name or self::vlan/@id]")
    vlans = []
    for i in res:
        if i.get_name() == "name":
            vlan = {}
            vlan["name"] = i.get_content()
        if i.get_name() == "vlan":
            vlan["vlanid"] = i.prop("id")
            vlans.append(vlan)
            vlan = None
    if not selector:
        for vlan in vlans: 
            if not search:
                print "Name: %s\t\t\t\tVLAN ID: %s" %(vlan["name"],vlan["vlanid"])
            else:
                try:
                    if int(vlan["vlanid"]) == int(search):
                        print "Name: %s\t\t\t\tVLAN ID: %s" %(vlan["name"],vlan["vlanid"])
                except:
                    if vlan["name"].find(search) != -1 :
                        print "Name: %s\t\t\t\tVLAN ID: %s" %(vlan["name"],vlan["vlanid"])
    result = []
    if not search:
        return vlans
    for vlan in vlans:
            try:
                if int(vlan["vlanid"]) == int(search):
                    result.append(vlan)
            except:
                if vlan["name"].find(search) != -1 :
                    result.append(vlan)
    return result


def getDcData(dcName,data):
    """ Get properties of dataCenter
    """
    clusters = rhevGet("/api/datacenters")
    doc = libxml2.parseDoc(clusters)
    ctxt = doc.xpathNewContext()
    res = ctxt.xpathEval("/data_centers/data_center[name [position()=1]= '"+ dcName + "']")
    return res[0].prop(data)

def getTicketValue(xml):
    """ Get value of ticket """
    doc = libxml2.parseDoc(xml)
    ctxt = doc.xpathNewContext()
    res = ctxt.xpathEval("//ticket/value")
    if len(res) == 1:
        for i in res:
            return i.getContent()
    else:
        return None

def getPort(xml,secure = None):
    doc = libxml2.parseDoc(xml)
    ctxt = doc.xpathNewContext()
    if not secure :
        res = ctxt.xpathEval("//display/port")
    else :
        res = ctxt.xpathEval("//display/secure_port")
    if len(res) == 1:
        for i in res:
            return i.getContent()
    else:
        return None

def getVmHost(xml):
    doc = libxml2.parseDoc(xml)
    ctxt = doc.xpathNewContext()
    res = ctxt.xpathEval("//host")
    if len(res) == 1:
        for i in res:
            hosthref = i.prop("href")
    hostxml = rhevGet(hosthref)
    doc = libxml2.parseDoc(hostxml)
    ctx = doc.xpathNewContext()
    res = ctx.xpathEval("/host/address")
    return res[0].getContent()



def getAllHosts(cluster):
    """ get "rhev_settings.NIC"  hrefs for attaching project networks
    """
    nics = []
    hosts = rhevGet("/api/hosts")
    doc = libxml2.parseDoc(hosts)
    ctxt = doc.xpathNewContext()
    res = ctxt.xpathEval("/hosts/host[cluster[@id='" + getClusterData(cluster ,"id")  + "']]")
    for i in res:
        #hrefs.append(i.prop("href"))
        nic = rhevGet(i.prop("href")+"/nics")
        nicdoc = libxml2.parseDoc(nic)
        ctxt = nicdoc.xpathNewContext()
        res = ctxt.xpathEval("/host_nics/host_nic/name[text() = '%s']/parent::*" %rhev_settings.NIC)
        for i in res:
            nics.append(i.prop("href"))
    return nics

def rhevConnect():
    """ Just connect to RHEVM using HTTPS
        HTTP not supported yet
    """
    rhev = rhev_settings.HOST_PORT
    conn = httplib.HTTPSConnection(rhev)
    return conn

def rhevGet(url):
    """ Make GET request
    """
    conn = rhevConnect()
    conn.request("GET",url,None,getHeaders())
    r = conn.getresponse()
    return r.read()

def rhevPost(url,data):
    """ Make POST request, send data
    """
    conn = rhevConnect()
    conn.request("POST", url, body = data.encode('utf-8'), headers = getHeaders())
    print url
    r = conn.getresponse()
    ## DEBUG 
    ## TODO: check status 
    status = r.read()
    print r.status,r.reason
    if int(r.status)>=400:
        print r.reason
        print status
    return status
    ## return r.read()
