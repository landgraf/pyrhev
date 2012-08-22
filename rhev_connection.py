#!/bin/env python
# -*- coding: utf-8 -*-
import httplib,urllib
import base64
import string
import libxml2
import rhev_settings
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
    for i in res:
        return i.prop(data)

def getClusterData(clusterName,data):
    """ Get properties of cluster
    """
    clusters = rhevGet("/api/clusters")
    doc = libxml2.parseDoc(clusters)
    ctxt = doc.xpathNewContext()
    res = ctxt.xpathEval("/clusters/cluster[name [position()=1]= '"+ clusterName + "']")
    for i in res:
        return i.prop(data)

def getDcData(dcName,data):
    """ Get properties of dataCenter
    """
    clusters = rhevGet("/api/datacenters")
    doc = libxml2.parseDoc(clusters)
    ctxt = doc.xpathNewContext()
    res = ctxt.xpathEval("/dataCenters/dataCenter[name [position()=1]= '"+ dcName + "']")
    for i in res:
        print i.prop(data)
        return i.prop(data)

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
        res = ctxt.xpathEval("/hostNics/hostNic[name='eth1']")
        for i in res:
            print i.prop("href")
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
    r = conn.getresponse()
    ## DEBUG 
    print r.status, r.reason
    return r.read()
