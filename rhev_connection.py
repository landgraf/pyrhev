#!/bin/env python
# -*- coding: utf-8 -*-
import httplib,urllib
import base64
import string
import libxml2
import rhev_settings
def get_headers():
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

def get_tag_data(tagname,data):
    """ Get properties of tag
        return property for parent tag
    """
    tags = rhev_get("/api/tags")
    doc = libxml2.parseDoc(tags)
    ctxt = doc.xpathNewContext()
    res = ctxt.xpathEval("/tags/tag[name[position()=1]= '" + tagname + "']")
    for i in res:
        return i.prop(data)

def get_cluster_data(cluster_name,data):
    """ Get properties of cluster
    """
    clusters = rhev_get("/api/clusters")
    doc = libxml2.parseDoc(clusters)
    ctxt = doc.xpathNewContext()
    res = ctxt.xpathEval("/clusters/cluster[name [position()=1]= '"+ cluster_name + "']")
    for i in res:
        return i.prop(data)

def get_dc_data(dc_name,data):
    """ Get properties of data_center
    """
    clusters = rhev_get("/api/datacenters")
    doc = libxml2.parseDoc(clusters)
    ctxt = doc.xpathNewContext()
    res = ctxt.xpathEval("/data_centers/data_center[name [position()=1]= '"+ dc_name + "']")
    for i in res:
        print i.prop(data)
        return i.prop(data)

def get_all_hosts(cluster):
    """ get "rhev_settings.NIC"  hrefs for attaching project networks
    """
    nics = []
    hosts = rhev_get("/api/hosts")
    doc = libxml2.parseDoc(hosts)
    ctxt = doc.xpathNewContext()
    res = ctxt.xpathEval("/hosts/host[cluster[@id='" + get_cluster_data(cluster ,"id")  + "']]")
    for i in res:
        #hrefs.append(i.prop("href"))
        nic = rhev_get(i.prop("href")+"/nics")
        nicdoc = libxml2.parseDoc(nic)
        ctxt = nicdoc.xpathNewContext()
        res = ctxt.xpathEval("/host_nics/host_nic[name='eth1']")
        for i in res:
            print i.prop("href")
            nics.append(i.prop("href"))
    return nics

def rhev_connect():
    """ Just connect to RHEVM using HTTPS
        HTTP not supported yet
    """
    rhev = rhev_settings.HOST_PORT
    conn = httplib.HTTPSConnection(rhev)
    return conn

def rhev_get(url):
    """ Make GET request
    """
    conn = rhev_connect()
    conn.request("GET",url,None,get_headers())
    r = conn.getresponse()
    return r.read()

def rhev_post(url,data):
    """ Make POST request, send data
    """
    conn = rhev_connect()
    conn.request("POST", url, body = data.encode('utf-8'), headers = get_headers())
    r = conn.getresponse()
    ## DEBUG 
    print r.status, r.reason
    return r.read()
